// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/atomic_file.h"
#include "isotone/core/error.h"
#include "isotone/core/log.h"
#include "isotone/core/settings.h"
#include "temp_folder.h"

#include <chrono>
#include <cstddef>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <gtest/gtest.h>
#include <iterator>
#include <limits>
#include <memory>
#include <set>
#include <span>
#include <string>
#include <string_view>
#include <variant>
#include <vector>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>

namespace
{

using isotone::core::AtomicFileStep;
using isotone::core::Error;
using isotone::core::kSettingsMaxBytes;
using isotone::core::Log;
using isotone::core::LogConfig;
using isotone::core::LogEvent;
using isotone::core::LogLevel;
using isotone::core::Settings;
using isotone::core::SettingsDocument;
using isotone::core::SettingsLoad;
using isotone::core::SettingsOptions;
using isotone::tests::TempFolder;

constexpr std::string_view kChangedTemplate{"Setting {key} changed to {value}"};

// A log that keeps its events in memory only, so a test reads exactly what the store logged.
LogConfig memory_log(const TempFolder& temp)
{
    LogConfig config;
    config.app_name = "TestApp";
    config.folder = temp.path() / "logs";
    config.minimum_level = LogLevel::Information;
    config.outputs = {.file = false, .memory = true, .debugger = false};
    return config;
}

void put(const std::filesystem::path& file, std::string_view text)
{
    std::ofstream stream{file, std::ios::binary | std::ios::trunc};
    stream << text;
}

std::string slurp(const std::filesystem::path& file)
{
    std::ifstream stream{file, std::ios::binary};
    return {std::istreambuf_iterator<char>{stream}, std::istreambuf_iterator<char>{}};
}

std::set<std::string> names_in(const std::filesystem::path& folder)
{
    std::set<std::string> names;
    for (const auto& entry : std::filesystem::directory_iterator{folder})
    {
        names.insert(entry.path().filename().string());
    }
    return names;
}

std::vector<LogEvent> events_with(const Log& log, std::string_view message_template)
{
    std::vector<LogEvent> matching;
    for (LogEvent& event : log.recent())
    {
        if (event.message_template == message_template)
        {
            matching.push_back(std::move(event));
        }
    }
    return matching;
}

std::size_t count_level(const Log& log, LogLevel level)
{
    std::size_t count = 0;
    for (const LogEvent& event : log.recent())
    {
        count += event.level == level ? 1U : 0U;
    }
    return count;
}

// The Error a call throws. A call that throws none fails the test and gives a stand-in.
template <typename Call> Error error_of(Call&& call)
{
    try
    {
        std::forward<Call>(call)();
    }
    catch (const Error& error)
    {
        return error;
    }
    ADD_FAILURE() << "no Error was thrown";
    return Error{"nothing", 0, "no Error was thrown"};
}

// Whether a call throws an Error.
template <typename Call> bool throws_error(Call&& call)
{
    try
    {
        std::forward<Call>(call)();
    }
    catch (const Error&)
    {
        return true;
    }
    return false;
}

// 2026-11-13 10:15:00 UTC, so a file kept aside has a name a test can state.
SettingsOptions fixed_clock()
{
    using namespace std::chrono;
    SettingsOptions options;
    options.clock = [] { return system_clock::time_point{sys_days{2026y / November / 13} + 10h + 15min}; };
    return options;
}

constexpr std::string_view kAsideUnreadable{"settings.unreadable-20261113T101500Z.json"};
constexpr std::string_view kAsideNewer{"settings.newer-20261113T101500Z.json"};

SettingsDocument inspect(std::string_view text, std::string* rewritten = nullptr)
{
    return isotone::core::inspect_settings_document(std::as_bytes(std::span{text}), rewritten);
}

// A fail seam that fails nothing and counts the writes that reach the temporary file.
auto count_writes(int& writes)
{
    return [&writes](AtomicFileStep step) {
        if (step == AtomicFileStep::WriteTemporary)
        {
            ++writes;
        }
        return 0U;
    };
}

TEST(Settings, SetPersistsAndReadsBack)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    {
        Settings settings{temp.path(), log};
        EXPECT_EQ(settings.load_report().outcome, SettingsLoad::NoFile);
        EXPECT_EQ(settings.file(), temp.path() / "settings.json");
        settings.set("ui.theme", std::string{"dark"});
        EXPECT_EQ(slurp(settings.file()),
                  "{\n  \"version\": 1,\n  \"values\": {\n    \"ui.theme\": \"dark\"\n  }\n}\n");
        settings.set("canvas.zoom", 1.5);
        settings.set("recent.count", std::int64_t{12});
        settings.set("snap.enabled", true);
        settings.set("name", std::string{"Zo\xC3\xAB \"quoted\"\n"});
        EXPECT_EQ(settings.get_string("ui.theme", "light"), "dark");
        EXPECT_EQ(settings.get_int("recent.count", 0), 12);
    }
    // A new store, as the next start of the app, reads every value back from the file.
    const Settings reopened{temp.path(), log};
    EXPECT_EQ(reopened.load_report().outcome, SettingsLoad::Loaded);
    EXPECT_EQ(reopened.get_string("ui.theme", "light"), "dark");
    EXPECT_DOUBLE_EQ(reopened.get_double("canvas.zoom", 1.0), 1.5);
    EXPECT_EQ(reopened.get_int("recent.count", 0), 12);
    EXPECT_TRUE(reopened.get_bool("snap.enabled", false));
    EXPECT_EQ(reopened.get_string("name", ""), "Zo\xC3\xAB \"quoted\"\n");
    EXPECT_EQ(inspect(slurp(reopened.file())), SettingsDocument::Supported);
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"settings.json"});
}

TEST(Settings, TypedDefaults)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    put(temp.path() / "settings.json",
        R"({"version": 1, "values": {"flag": true, "count": 7, "ratio": 0.25, "text": "hi",)"
        R"( "huge": 18446744073709551615, "negative": -3}})");
    const Settings settings{temp.path(), log};
    ASSERT_EQ(settings.load_report().outcome, SettingsLoad::Loaded);

    // An absent key gives the default.
    EXPECT_TRUE(settings.get_bool("absent", true));
    EXPECT_EQ(settings.get_int("absent", 42), 42);
    EXPECT_DOUBLE_EQ(settings.get_double("absent", 2.5), 2.5);
    EXPECT_EQ(settings.get_string("absent", "fallback"), "fallback");

    // A key of another type gives the default rather than a converted value.
    EXPECT_FALSE(settings.get_bool("count", false));
    EXPECT_EQ(settings.get_int("ratio", 42), 42);
    EXPECT_EQ(settings.get_int("text", 42), 42);
    EXPECT_EQ(settings.get_int("flag", 42), 42);
    EXPECT_DOUBLE_EQ(settings.get_double("text", 2.5), 2.5);
    EXPECT_EQ(settings.get_string("count", "fallback"), "fallback");
    // A whole number past the signed range is not an int64.
    EXPECT_EQ(settings.get_int("huge", 42), 42);

    EXPECT_TRUE(settings.get_bool("flag", false));
    EXPECT_EQ(settings.get_int("count", 0), 7);
    EXPECT_EQ(settings.get_int("negative", 0), -3);
    EXPECT_DOUBLE_EQ(settings.get_double("ratio", 0.0), 0.25);
    // A whole number reads as a double too: JSON writes 7.0 as 7 in other tools.
    EXPECT_DOUBLE_EQ(settings.get_double("count", 0.0), 7.0);
    EXPECT_EQ(settings.get_string("text", ""), "hi");
}

TEST(Settings, ChangeWritesOneLogLine)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    Settings settings{temp.path(), log};

    settings.set("ui.theme", std::string{"dark"});
    auto changed = events_with(log, kChangedTemplate);
    ASSERT_EQ(changed.size(), 1U);
    EXPECT_EQ(changed.at(0).level, LogLevel::Information);
    ASSERT_EQ(changed.at(0).fields.size(), 2U);
    EXPECT_EQ(changed.at(0).fields.at(0).name, "key");
    EXPECT_EQ(std::get<std::string>(changed.at(0).fields.at(0).value), "ui.theme");
    EXPECT_EQ(changed.at(0).fields.at(1).name, "value");
    EXPECT_EQ(std::get<std::string>(changed.at(0).fields.at(1).value), "dark");
    EXPECT_EQ(Log::render(changed.at(0).message_template, changed.at(0).fields), "Setting ui.theme changed to dark");
    EXPECT_EQ(log.recent().size(), 1U);

    settings.set("recent.count", std::int64_t{3});
    changed = events_with(log, kChangedTemplate);
    ASSERT_EQ(changed.size(), 2U);
    EXPECT_EQ(std::get<std::int64_t>(changed.at(1).fields.at(1).value), 3);
    EXPECT_EQ(log.recent().size(), 2U);
}

TEST(Settings, UnchangedSetWritesNothing)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    int writes = 0;
    SettingsOptions options;
    options.seams.fail = count_writes(writes);
    Settings settings{temp.path(), log, options};

    settings.set("recent.count", std::int64_t{3});
    settings.set("canvas.zoom", 2.0);
    EXPECT_EQ(writes, 2);
    // The same values again, in this store and in a new one that read them from the file: no write, no log line.
    settings.set("recent.count", std::int64_t{3});
    settings.set("canvas.zoom", 2.0);
    Settings reopened{temp.path(), log, options};
    reopened.set({{"recent.count", std::int64_t{3}}, {"canvas.zoom", 2.0}});
    EXPECT_EQ(writes, 2);
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), 2U);

    // The same number as another type is a change: 3 is not 3.0.
    reopened.set("recent.count", 3.0);
    EXPECT_EQ(writes, 3);
    EXPECT_EQ(reopened.get_int("recent.count", -1), -1);
    EXPECT_DOUBLE_EQ(reopened.get_double("recent.count", 0.0), 3.0);
}

// A whole number the file holds past the signed range is not equal to any signed value: -1 is a change.
TEST(Settings, UnsignedValueIsNotASignedOne)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    put(temp.path() / "settings.json", R"({"version": 1, "values": {"count": 18446744073709551615, "small": 7}})");
    Settings settings{temp.path(), log};
    EXPECT_EQ(settings.get_int("count", 0), 0);

    settings.set("count", std::int64_t{-1});
    EXPECT_EQ(settings.get_int("count", 0), -1);
    EXPECT_EQ(Settings(temp.path(), log).get_int("count", 0), -1);
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), 1U);
    // A value in range that JSON stored unsigned is still the same whole number.
    settings.set("small", std::int64_t{7});
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), 1U);
}

// A key given twice in one set takes its last value: compared once with the file, logged once.
TEST(Settings, RepeatedKeyTakesItsLastValue)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    int writes = 0;
    SettingsOptions options;
    options.seams.fail = count_writes(writes);
    Settings settings{temp.path(), log, options};
    settings.set("a", std::int64_t{1});

    // Back to the value it holds: nothing is written or logged, and no value that was never saved is logged.
    settings.set({{"a", std::int64_t{2}}, {"a", std::int64_t{1}}});
    EXPECT_EQ(writes, 1);
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), 1U);

    settings.set({{"a", std::int64_t{2}}, {"b", true}, {"a", std::int64_t{3}}});
    EXPECT_EQ(writes, 2);
    const auto changed = events_with(log, kChangedTemplate);
    EXPECT_EQ(changed.size(), 3U);
    EXPECT_EQ(std::get<std::int64_t>(changed.at(1).fields.at(1).value), 3);
    EXPECT_EQ(settings.get_int("a", 0), 3);
}

TEST(Settings, SetSeveralWritesOnce)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    int writes = 0;
    SettingsOptions options;
    options.seams.fail = count_writes(writes);
    Settings settings{temp.path(), log, options};
    settings.set("b", true);
    writes = 0;

    // Three keys, one already holding its value: one write, and a log line for each of the two that changed.
    settings.set({{"a", std::int64_t{1}}, {"b", true}, {"c", std::string{"x"}}});
    EXPECT_EQ(writes, 1);
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), 3U);
    const Settings reopened{temp.path(), log};
    EXPECT_EQ(reopened.get_int("a", 0), 1);
    EXPECT_TRUE(reopened.get_bool("b", false));
    EXPECT_EQ(reopened.get_string("c", ""), "x");
}

// The store works from the defaults, and its next change writes a fresh file beside the kept one.
void expect_fresh_file_beside_the_kept_one(Settings& settings, const std::string& corrupt)
{
    const auto kept_aside = settings.load_report().kept_aside;
    // The reader says the same of the bytes on their own, which is what the fuzz target drives.
    EXPECT_EQ(inspect(corrupt), SettingsDocument::Unreadable) << corrupt.substr(0, 60);
    EXPECT_EQ(settings.get_int("a", 9), 9);
    settings.set("a", std::int64_t{1});
    EXPECT_EQ(inspect(slurp(settings.file())), SettingsDocument::Supported);
    EXPECT_EQ(slurp(kept_aside), corrupt) << corrupt.substr(0, 60);
}

// A settings file the reader refuses is kept whole under a new name, reported, and never overwritten.
void expect_kept_aside(const std::string& corrupt)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    put(temp.path() / "settings.json", corrupt);
    const std::string shown = corrupt.substr(0, 60);

    Settings settings{temp.path(), log, fixed_clock()};
    const auto report = settings.load_report();
    EXPECT_EQ(report.outcome, SettingsLoad::UnreadableKeptAside) << shown;
    EXPECT_EQ(report.kept_aside, temp.path() / kAsideUnreadable);
    EXPECT_FALSE(report.reason.empty());
    // The file is kept whole under its new name, and nothing took its place.
    EXPECT_EQ(slurp(temp.path() / kAsideUnreadable), corrupt) << shown;
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{std::string{kAsideUnreadable}}) << shown;
    EXPECT_EQ(count_level(log, LogLevel::Warning), 1U) << shown;
    expect_fresh_file_beside_the_kept_one(settings, corrupt);
}

TEST(Settings, CorruptFileKeptAndReported)
{
    // Cut off mid-value, the wrong root, no version, no values, a version below 1, a version that is not whole,
    // values that are not an object, a string that is not UTF-8, and an empty file.
    expect_kept_aside(R"({"version": 1, "values": {"a": tru)");
    expect_kept_aside("[1, 2, 3]");
    expect_kept_aside(R"({"values": {}})");
    expect_kept_aside(R"({"version": 1})");
    expect_kept_aside(R"({"version": 0, "values": {}})");
    expect_kept_aside(R"({"version": 1.5, "values": {}})");
    expect_kept_aside(R"({"version": 1, "values": []})");
    expect_kept_aside("{\"version\": 1, \"values\": {\"a\": \"\xFF\"}}");
    expect_kept_aside("");
    // Nested one level past the limit, and one byte of value past the size limit.
    expect_kept_aside(R"({"version": 1, "values": {"a": )" + std::string(63, '[') + std::string(63, ']') + "}}");
    expect_kept_aside(R"({"version": 1, "values": {"blob": ")" +
                      std::string(static_cast<std::size_t>(kSettingsMaxBytes), 'x') + R"("}})");
}

// The deepest nesting and the largest file the reader accepts are read, not kept aside.
TEST(Settings, LimitsAreInclusive)
{
    const std::string deepest =
        R"({"version": 1, "values": {"a": )" + std::string(62, '[') + std::string(62, ']') + "}}";
    EXPECT_EQ(inspect(deepest), SettingsDocument::Supported);
    const std::string head = R"({"version": 1, "values": {"blob": ")";
    const std::string tail = R"("}})";
    const auto limit = static_cast<std::size_t>(kSettingsMaxBytes);
    EXPECT_EQ(inspect(head + std::string(limit - head.size() - tail.size(), 'x') + tail), SettingsDocument::Supported);
    EXPECT_EQ(inspect(head + std::string(limit - head.size() - tail.size() + 1, 'x') + tail),
              SettingsDocument::Unreadable);
}

TEST(Settings, NewerVersionKeptAndReported)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    const std::string newer = R"({"version": 2, "values": {"a": 5}, "added": "by a later version"})";
    put(temp.path() / "settings.json", newer);
    EXPECT_EQ(inspect(newer), SettingsDocument::Newer);

    Settings settings{temp.path(), log, fixed_clock()};
    const auto report = settings.load_report();
    ASSERT_EQ(report.outcome, SettingsLoad::NewerKeptAside);
    EXPECT_EQ(report.kept_aside, temp.path() / kAsideNewer);
    EXPECT_NE(report.reason.find("version 2"), std::string::npos) << report.reason;
    EXPECT_EQ(slurp(report.kept_aside), newer);
    EXPECT_EQ(count_level(log, LogLevel::Warning), 1U);
    // Nothing of the newer file is read as this version's.
    EXPECT_EQ(settings.get_int("a", 0), 0);

    settings.set("a", std::int64_t{1});
    EXPECT_EQ(slurp(report.kept_aside), newer);
    EXPECT_EQ(names_in(temp.path()), (std::set<std::string>{"settings.json", std::string{kAsideNewer}}));
}

void expect_log_counts(const Log& log, std::size_t changes, std::size_t errors)
{
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), changes);
    EXPECT_EQ(count_level(log, LogLevel::Error), errors);
}

// A fail seam that fails the write of the temporary file with "disk full" while *disk_full is true.
auto full_disk_while(std::shared_ptr<const bool> disk_full)
{
    return [disk_full = std::move(disk_full)](AtomicFileStep step) {
        return *disk_full && step == AtomicFileStep::WriteTemporary ? static_cast<std::uint32_t>(ERROR_DISK_FULL) : 0U;
    };
}

TEST(Settings, FailedWriteKeepsMemoryAndReports)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    const auto disk_full = std::make_shared<bool>(false);
    SettingsOptions options;
    options.seams.fail = full_disk_while(disk_full);
    Settings settings{temp.path(), log, options};
    settings.set("a", std::int64_t{1});
    const std::string before = slurp(settings.file());

    *disk_full = true;
    const Error error = error_of([&settings] { settings.set({{"a", std::int64_t{2}}, {"b", true}}); });
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_DISK_FULL));
    // The file and the values in memory are as they were, with no temporary file left.
    EXPECT_EQ(slurp(settings.file()), before);
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"settings.json"});
    EXPECT_EQ(settings.get_int("a", 0), 1);
    EXPECT_FALSE(settings.get_bool("b", false));
    // The change log has only the first change, and the failure is logged once as an Error.
    expect_log_counts(log, 1U, 1U);
}

// With room on the disk again, the change that was refused goes through.
TEST(Settings, FailedWriteCanBeRetried)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    const auto disk_full = std::make_shared<bool>(true);
    SettingsOptions options;
    options.seams.fail = full_disk_while(disk_full);
    Settings settings{temp.path(), log, options};
    EXPECT_TRUE(throws_error([&settings] { settings.set({{"a", std::int64_t{2}}, {"b", true}}); }));
    EXPECT_TRUE(names_in(temp.path()).empty());
    EXPECT_EQ(count_level(log, LogLevel::Error), 1U);

    *disk_full = false;
    settings.set({{"a", std::int64_t{2}}, {"b", true}});
    EXPECT_EQ(settings.get_int("a", 0), 2);
    EXPECT_TRUE(settings.get_bool("b", false));
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), 2U);
}

TEST(Settings, TwoStoresMergeTheirChanges)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    // Two stores on one file, as two running windows of one app.
    Settings first{temp.path(), log};
    Settings second{temp.path(), log};

    first.set("a", std::int64_t{1});
    second.set("b", std::int64_t{2});
    first.set("c", std::int64_t{3});

    // Neither lost the other's setting, on disk or in memory after its own write.
    const Settings reopened{temp.path(), log};
    EXPECT_EQ(reopened.get_int("a", 0), 1);
    EXPECT_EQ(reopened.get_int("b", 0), 2);
    EXPECT_EQ(reopened.get_int("c", 0), 3);
    EXPECT_EQ(first.get_int("b", 0), 2);
    EXPECT_EQ(second.get_int("a", 0), 1);

    // A value the other store changed is not "unchanged" because this store still remembers the old one.
    second.set("a", std::int64_t{10});
    first.set("a", std::int64_t{1});
    EXPECT_EQ(Settings(temp.path(), log).get_int("a", 0), 1);
}

TEST(Settings, UnknownValuesSurviveARewrite)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    put(temp.path() / "settings.json",
        R"({"version": 1, "values": {"list": [1, 2], "nested": {"k": null}, "nothing": null, "keep": 5}})");
    Settings settings{temp.path(), log};
    ASSERT_EQ(settings.load_report().outcome, SettingsLoad::Loaded);
    // A value of a type the store does not read gives the default.
    EXPECT_EQ(settings.get_int("list", 7), 7);
    EXPECT_EQ(settings.get_string("nested", "d"), "d");

    settings.set("added", true);
    const std::string text = slurp(settings.file());
    std::string rewritten;
    ASSERT_EQ(inspect(text, &rewritten), SettingsDocument::Supported);
    // Writing a document the store accepts gives the same bytes: the file is already in its written form.
    EXPECT_EQ(rewritten, text);
    EXPECT_EQ(text, "{\n  \"version\": 1,\n  \"values\": {\n    \"added\": true,\n    \"keep\": 5,\n    \"list\": [\n"
                    "      1,\n      2\n    ],\n    \"nested\": {\n      \"k\": null\n    },\n    \"nothing\": null\n"
                    "  }\n}\n");
}

TEST(Settings, InvalidValuesAreRefused)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    Settings settings{temp.path(), log};

    EXPECT_TRUE(throws_error([&settings] { settings.set("", true); }));
    EXPECT_TRUE(throws_error([&settings] { settings.set("bad\xFFkey", true); }));
    EXPECT_TRUE(throws_error([&settings] { settings.set("text", std::string{"bad\xC3"}); }));
    EXPECT_TRUE(throws_error([&settings] { settings.set("ratio", std::numeric_limits<double>::quiet_NaN()); }));
    EXPECT_TRUE(throws_error([&settings] { settings.set("ratio", std::numeric_limits<double>::infinity()); }));
    // One bad change refuses the whole set: the good key beside it is not written either.
    EXPECT_TRUE(throws_error(
        [&settings] { settings.set({{"good", true}, {"ratio", -std::numeric_limits<double>::infinity()}}); }));

    EXPECT_FALSE(settings.get_bool("good", false));
    EXPECT_TRUE(names_in(temp.path()).empty());
    EXPECT_TRUE(log.recent().empty());
}

// A file filled to the limit exactly is written; one more setting is refused, with the file, memory, and the
// change log as they were. Returns the size of the string that filled the file.
std::size_t expect_one_store_stops_at_the_limit(const std::filesystem::path& folder, Log& log)
{
    const auto limit = static_cast<std::size_t>(kSettingsMaxBytes);
    Settings settings{folder, log};
    settings.set("blob", std::string{});
    // Every byte added to the string adds one to the file, so this string fills the file to the limit exactly.
    const std::size_t overhead = slurp(settings.file()).size();
    settings.set("blob", std::string(limit - overhead, 'x'));
    const std::string at_limit = slurp(settings.file());
    EXPECT_EQ(at_limit.size(), limit);

    const std::size_t changes_before = events_with(log, kChangedTemplate).size();
    const Error error = error_of([&settings] { settings.set("more", true); });
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_FILE_TOO_LARGE));
    EXPECT_EQ(slurp(settings.file()), at_limit);
    EXPECT_FALSE(settings.get_bool("more", false));
    EXPECT_EQ(events_with(log, kChangedTemplate).size(), changes_before);
    return limit - overhead;
}

// Two stores whose settings each fit but together do not: the merged write is refused, not saved unreadable.
void expect_merged_write_stops_at_the_limit()
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    const auto limit = static_cast<std::size_t>(kSettingsMaxBytes);
    Settings first{temp.path(), log};
    Settings second{temp.path(), log};
    first.set("first", std::string(limit / 2, 'a'));
    const std::string before = slurp(first.file());

    const Error error = error_of([&second, limit] { second.set("second", std::string(limit / 2, 'b')); });
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_FILE_TOO_LARGE));
    EXPECT_EQ(slurp(first.file()), before);
    const Settings reopened{temp.path(), log};
    EXPECT_EQ(reopened.load_report().outcome, SettingsLoad::Loaded);
    EXPECT_EQ(reopened.get_string("first", "").size(), limit / 2);
    EXPECT_EQ(reopened.get_string("second", "none"), "none");
}

TEST(Settings, OversizedWriteIsRefused)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    const std::size_t blob_size = expect_one_store_stops_at_the_limit(temp.path(), log);
    // The file at the limit is still one the next start reads.
    const Settings reopened{temp.path(), log};
    EXPECT_EQ(reopened.load_report().outcome, SettingsLoad::Loaded);
    EXPECT_EQ(reopened.get_string("blob", "").size(), blob_size);

    expect_merged_write_stops_at_the_limit();
}

TEST(Settings, NewerTargetSurvivesALeftoverBackup)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    // A newer version of the app was killed while saving: its new file is in place and its backup, which this
    // older version could read, is still beside it.
    const std::string newer = R"({"version": 3, "values": {"a": 30}})";
    put(temp.path() / "settings.json", newer);
    put(temp.path() / "settings.json.bak", R"({"version": 1, "values": {"a": 1}})");

    const Settings settings{temp.path(), log, fixed_clock()};
    const auto report = settings.load_report();
    // The newer file is kept, whole, and the older backup did not replace it or get read in its place.
    ASSERT_EQ(report.outcome, SettingsLoad::NewerKeptAside);
    EXPECT_EQ(slurp(report.kept_aside), newer);
    EXPECT_EQ(settings.get_int("a", 0), 0);
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{std::string{kAsideNewer}});
}

TEST(Settings, MoveAsideRereadsUnderTheLock)
{
    const TempFolder temp;
    Log log{memory_log(temp)};
    const auto file = temp.path() / "settings.json";
    put(file, "{ torn");
    // Between this store finding the file unusable and taking the lock, another process replaces it with a good one.
    SettingsOptions options = fixed_clock();
    options.before_move_aside = [&file] { put(file, R"({"version": 1, "values": {"a": 5}})"); };

    const Settings settings{temp.path(), log, options};
    // The good file is read, not moved aside.
    EXPECT_EQ(settings.load_report().outcome, SettingsLoad::Loaded);
    EXPECT_EQ(settings.get_int("a", 0), 5);
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"settings.json"});
    EXPECT_EQ(count_level(log, LogLevel::Warning), 0U);
}

TEST(Settings, KeptAsideNameCollisionAndRefusal)
{
    {
        // The name is taken by a file kept in the same second: the new one gets a number, and neither is lost.
        const TempFolder temp;
        Log log{memory_log(temp)};
        put(temp.path() / kAsideUnreadable, "kept earlier");
        put(temp.path() / "settings.json", "{ torn");
        const Settings settings{temp.path(), log, fixed_clock()};
        const auto report = settings.load_report();
        ASSERT_EQ(report.outcome, SettingsLoad::UnreadableKeptAside);
        EXPECT_EQ(report.kept_aside, temp.path() / "settings.unreadable-20261113T101500Z-2.json");
        EXPECT_EQ(slurp(report.kept_aside), "{ torn");
        EXPECT_EQ(slurp(temp.path() / kAsideUnreadable), "kept earlier");
    }

    // Another program holds the file so it cannot be renamed: it stays where it is, whole, and the store says so.
    const TempFolder temp;
    Log log{memory_log(temp)};
    const auto file = temp.path() / "settings.json";
    put(file, "{ torn");
    const HANDLE held = CreateFileW(file.c_str(), GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING,
                                    FILE_ATTRIBUTE_NORMAL, nullptr);
    ASSERT_NE(held, INVALID_HANDLE_VALUE);
    {
        Settings settings{temp.path(), log, fixed_clock()};
        const auto report = settings.load_report();
        EXPECT_EQ(report.outcome, SettingsLoad::Unavailable);
        EXPECT_NE(report.reason.find("could not be moved aside"), std::string::npos) << report.reason;
        EXPECT_TRUE(report.kept_aside.empty());
        EXPECT_EQ(count_level(log, LogLevel::Warning), 1U);
        // A change is refused rather than written over the file that could not be kept.
        EXPECT_TRUE(throws_error([&settings] { settings.set("a", std::int64_t{1}); }));
        EXPECT_EQ(settings.get_int("a", 0), 0);
    }
    CloseHandle(held);
    EXPECT_EQ(slurp(file), "{ torn");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"settings.json"});
}

} // namespace
