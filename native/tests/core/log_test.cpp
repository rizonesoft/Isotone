// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/log.h"
#include "temp_folder.h"

#include <atomic>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <gtest/gtest.h>
#include <iterator>
#include <mutex>
#include <regex>
#include <set>
#include <sstream>
#include <string>
#include <thread>
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

using isotone::core::Log;
using isotone::core::LogConfig;
using isotone::core::LogEvent;
using isotone::core::LogField;
using isotone::core::LogLevel;
using isotone::tests::TempFolder;
using namespace std::chrono_literals;

// A clock a test moves by hand, readable from any thread.
class TestClock
{
  public:
    explicit TestClock(std::chrono::system_clock::time_point start) : now_{start.time_since_epoch().count()}
    {
    }
    void set(std::chrono::system_clock::time_point when)
    {
        now_.store(when.time_since_epoch().count());
    }
    [[nodiscard]] std::chrono::system_clock::time_point now() const
    {
        return std::chrono::system_clock::time_point{std::chrono::system_clock::duration{now_.load()}};
    }

  private:
    std::atomic<std::chrono::system_clock::rep> now_;
};

constexpr auto kDay = std::chrono::sys_days{std::chrono::year{2026} / 11 / 13};
const auto kMorning = kDay + 5h + 44min + 35s + 123ms;

LogConfig config_for(const TempFolder& temp, const TestClock& clock)
{
    LogConfig config;
    config.app_name = "TestApp";
    config.folder = temp.path() / "logs";
    config.minimum_level = LogLevel::Information;
    config.outputs.debugger = false;
    config.clock = [&clock] { return clock.now(); };
    return config;
}

std::vector<std::string> lines_of(const std::filesystem::path& file)
{
    std::ifstream input{file, std::ios::binary};
    std::vector<std::string> lines;
    for (std::string line; std::getline(input, line);)
    {
        lines.push_back(line);
    }
    return lines;
}

std::uintmax_t size_of(const std::filesystem::path& file)
{
    std::ifstream input{file, std::ios::binary | std::ios::ate};
    return static_cast<std::uintmax_t>(input.tellg());
}

// What a logs folder holds: its complete records, files over a size, and lines that are not whole records.
struct Survey
{
    std::size_t records = 0;
    std::size_t oversized = 0;
    std::size_t malformed = 0;
};

Survey survey_folder(const std::filesystem::path& folder, std::uintmax_t max_bytes)
{
    Survey survey;
    for (const auto& entry : std::filesystem::directory_iterator{folder})
    {
        survey.oversized += size_of(entry.path()) > max_bytes ? 1U : 0U;
        for (const auto& line : lines_of(entry.path()))
        {
            const bool whole = line.starts_with("{\"time\":") && line.ends_with("}}");
            survey.records += whole ? 1U : 0U;
            survey.malformed += whole ? 0U : 1U;
        }
    }
    return survey;
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

TEST(Log, WritesOneJsonLinePerEvent)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    {
        Log log{config_for(temp, clock)};
        log.write(LogLevel::Information, "Saved {path} in {elapsed_ms} ms",
                  {LogField{"path", std::string{"C:\\a \"b\"\n\xC3\xA9"}}, LogField{"elapsed_ms", std::int64_t{12}}});
        log.write(LogLevel::Warning, "Fell back to {device}, {{literal}}",
                  {LogField{"device", std::string{"WARP"}}, LogField{"ok", false}, LogField{"ratio", 0.5}});
        log.write(LogLevel::Error, "Bad text {t}", {LogField{"t", std::string{"\xFF\x01"}}});
        EXPECT_EQ(log.failures(), 0U);
    }
    const auto lines = lines_of(temp.path() / "logs" / "testapp-2026-11-13.log");
    ASSERT_EQ(lines.size(), 3U);
    EXPECT_EQ(lines.at(0),
              "{\"time\":\"2026-11-13T05:44:35.123Z\",\"level\":\"Information\",\"template\":\"Saved {path} "
              "in {elapsed_ms} ms\",\"message\":\"Saved C:\\\\a \\\"b\\\"\\n\xC3\xA9 in 12 ms\",\"fields\":{"
              "\"path\":\"C:\\\\a \\\"b\\\"\\n\xC3\xA9\",\"elapsed_ms\":12}}");
    EXPECT_EQ(lines.at(1),
              "{\"time\":\"2026-11-13T05:44:35.123Z\",\"level\":\"Warning\",\"template\":\"Fell back to "
              "{device}, {{literal}}\",\"message\":\"Fell back to WARP, {literal}\",\"fields\":{\"device\":"
              "\"WARP\",\"ok\":false,\"ratio\":0.5}}");
    EXPECT_EQ(lines.at(2), "{\"time\":\"2026-11-13T05:44:35.123Z\",\"level\":\"Error\",\"template\":\"Bad text {t}\","
                           "\"message\":\"Bad text \xEF\xBF\xBD\\u0001\",\"fields\":{\"t\":\"\xEF\xBF\xBD\\u0001\"}}");
}

TEST(Log, MemoryBufferIsBoundedAndOrdered)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    auto config = config_for(temp, clock);
    config.outputs.file = false;
    config.memory_capacity = 3;
    Log log{std::move(config)};
    for (std::int64_t i = 0; i < 5; ++i)
    {
        log.write(LogLevel::Information, "Event {i}", {LogField{"i", i}});
    }
    const auto recent = log.recent();
    ASSERT_EQ(recent.size(), 3U);
    for (std::size_t k = 0; k < recent.size(); ++k)
    {
        EXPECT_EQ(std::get<std::int64_t>(recent.at(k).fields.at(0).value), static_cast<std::int64_t>(k + 2));
    }
    EXPECT_FALSE(std::filesystem::exists(temp.path() / "logs"));
}

TEST(Log, SafeFromManyThreads)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    constexpr int kThreads = 8;
    constexpr int kEach = 250;
    {
        Log log{config_for(temp, clock)};
        std::vector<std::jthread> threads;
        threads.reserve(kThreads);
        for (int thread_index = 0; thread_index < kThreads; ++thread_index)
        {
            threads.emplace_back([&log, thread_index] {
                for (int i = 0; i < kEach; ++i)
                {
                    log.write(LogLevel::Information, "Thread {t} event {i}",
                              {LogField{"t", std::int64_t{thread_index}}, LogField{"i", std::int64_t{i}}});
                }
            });
        }
    }
    const auto lines = lines_of(temp.path() / "logs" / "testapp-2026-11-13.log");
    ASSERT_EQ(lines.size(), static_cast<std::size_t>(kThreads * kEach));
    const std::regex shape{R"(^\{"time":"[^"]+","level":"Information",.*"fields":\{"t":(\d+),"i":(\d+)\}\}$)"};
    std::set<std::pair<int, int>> seen;
    for (const auto& line : lines)
    {
        std::smatch match;
        ASSERT_TRUE(std::regex_match(line, match, shape)) << line;
        seen.emplace(std::stoi(match.str(1)), std::stoi(match.str(2)));
    }
    EXPECT_EQ(seen.size(), static_cast<std::size_t>(kThreads * kEach));
}

TEST(Log, BelowLevelIsDropped)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    Log log{config_for(temp, clock)};
    log.write(LogLevel::Debug, "Developer detail");
    log.write(LogLevel::Verbose, "Inner loop");
    EXPECT_TRUE(log.recent().empty());
    EXPECT_FALSE(std::filesystem::exists(temp.path() / "logs"));
}

TEST(Log, ReopenAppends)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    {
        Log first{config_for(temp, clock)};
        first.write(LogLevel::Information, "First run");
    }
    {
        Log second{config_for(temp, clock)};
        second.write(LogLevel::Information, "Second run");
    }
    const auto lines = lines_of(temp.path() / "logs" / "testapp-2026-11-13.log");
    ASSERT_EQ(lines.size(), 2U);
    EXPECT_NE(lines.at(0).find("First run"), std::string::npos);
    EXPECT_NE(lines.at(1).find("Second run"), std::string::npos);
}

TEST(Log, DateChangeStartsNewFile)
{
    const TempFolder temp;
    TestClock clock{kDay + 23h + 59min + 59s + 999ms};
    Log log{config_for(temp, clock)};
    log.write(LogLevel::Information, "Before midnight");
    clock.set(kDay + std::chrono::days{1});
    log.write(LogLevel::Information, "After midnight");
    EXPECT_EQ(names_in(temp.path() / "logs"),
              (std::set<std::string>{"testapp-2026-11-13.log", "testapp-2026-11-14.log"}));
    EXPECT_EQ(lines_of(temp.path() / "logs" / "testapp-2026-11-14.log").size(), 1U);
}

TEST(Log, SizeLimitStartsNewPart)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    auto config = config_for(temp, clock);
    config.max_file_bytes = 300;
    Log log{std::move(config)};
    for (std::int64_t i = 0; i < 7; ++i)
    {
        log.write(LogLevel::Information, "Event number {i} with some padding text", {LogField{"i", i}});
    }
    const auto names = names_in(temp.path() / "logs");
    EXPECT_TRUE(names.contains("testapp-2026-11-13.log"));
    EXPECT_TRUE(names.contains("testapp-2026-11-13.1.log"));
    const auto survey = survey_folder(temp.path() / "logs", 300);
    EXPECT_EQ(survey.records, 7U);
    EXPECT_EQ(survey.oversized, 0U);
    EXPECT_EQ(survey.malformed, 0U);
}

TEST(Log, OversizedEventIsReplaced)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    auto config = config_for(temp, clock);
    config.max_file_bytes = 600;
    Log log{std::move(config)};
    log.write(LogLevel::Information, "Imported {text}", {LogField{"text", std::string(2000, 'x')}});
    log.write(LogLevel::Information, "Small");
    EXPECT_EQ(log.failures(), 0U);
    const auto recent = log.recent();
    ASSERT_EQ(recent.size(), 2U);
    EXPECT_EQ(std::get<std::string>(recent.front().fields.at(0).value).size(), 2000U);
    const auto survey = survey_folder(temp.path() / "logs", 600);
    EXPECT_EQ(survey.records, 2U);
    EXPECT_EQ(survey.oversized, 0U);
    const auto first = lines_of(temp.path() / "logs" / "testapp-2026-11-13.log").at(0);
    EXPECT_TRUE(first.contains("exceeded the 600-byte file limit")) << first;
    EXPECT_TRUE(first.contains("Imported {text}")) << first;
}

TEST(Log, KeepsNewestSevenFiles)
{
    const TempFolder temp;
    TestClock clock{kMorning};
    Log log{config_for(temp, clock)};
    for (int day_index = 0; day_index < 9; ++day_index)
    {
        clock.set(kMorning + std::chrono::days{day_index});
        log.write(LogLevel::Information, "Day {d}", {LogField{"d", std::int64_t{day_index}}});
    }
    const auto names = names_in(temp.path() / "logs");
    EXPECT_EQ(names.size(), 7U);
    EXPECT_FALSE(names.contains("testapp-2026-11-13.log"));
    EXPECT_FALSE(names.contains("testapp-2026-11-14.log"));
    EXPECT_TRUE(names.contains("testapp-2026-11-15.log"));
    EXPECT_TRUE(names.contains("testapp-2026-11-21.log"));
    EXPECT_EQ(log.failures(), 0U);
}

// Writes one event with the outputs given and reports where it went.
struct Delivery
{
    std::vector<std::wstring> debugger;
    std::size_t memory = 0;
    bool file = false;
};

Delivery deliver(const TempFolder& temp, const TestClock& clock, isotone::core::LogOutputs outputs)
{
    Delivery delivery;
    auto config = config_for(temp, clock);
    config.outputs = outputs;
    config.debugger_writer = [&delivery](std::wstring_view line) { delivery.debugger.emplace_back(line); };
    {
        Log log{config};
        log.write(LogLevel::Information, "Delivered");
        delivery.memory = log.recent().size();
    }
    delivery.file = std::filesystem::exists(temp.path() / "logs" / "testapp-2026-11-13.log");
    return delivery;
}

TEST(Log, OnlyEnabledOutputsReceive)
{
    const TestClock clock{kMorning};
    {
        const TempFolder temp;
        const auto only_debugger = deliver(temp, clock, {.file = false, .memory = false, .debugger = true});
        ASSERT_EQ(only_debugger.debugger.size(), 1U);
        EXPECT_TRUE(only_debugger.debugger.front().ends_with(L"\"fields\":{}}\n"));
        EXPECT_EQ(only_debugger.memory, 0U);
        EXPECT_FALSE(only_debugger.file);
    }
    {
        const TempFolder temp;
        const auto no_debugger = deliver(temp, clock, {.file = true, .memory = true, .debugger = false});
        EXPECT_TRUE(no_debugger.debugger.empty());
        EXPECT_EQ(no_debugger.memory, 1U);
        EXPECT_TRUE(no_debugger.file);
    }
}

TEST(Log, UnwritableFolderKeepsMemoryAndCounts)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    auto config = config_for(temp, clock);
    config.folder = temp.path() / "a-file";
    std::ofstream{config.folder} << "x";
    Log log{std::move(config)};
    log.write(LogLevel::Information, "Nowhere to go");
    log.write(LogLevel::Error, "Still nowhere");
    EXPECT_EQ(log.failures(), 2U);
    EXPECT_EQ(log.recent().size(), 2U);
}

// Writes half the bytes and fails the first time, then writes whole lines.
bool torn_once(bool& failed_once, void* file, std::string_view bytes)
{
    const std::string copy{bytes};
    DWORD written = 0;
    const auto count = static_cast<DWORD>(failed_once ? copy.size() : copy.size() / 2);
    const bool wrote = WriteFile(file, copy.c_str(), count, &written, nullptr) != FALSE && written == count;
    const bool first = !failed_once;
    failed_once = true;
    return wrote && !first;
}

TEST(Log, PartialWriteLeavesLaterRecordsReadable)
{
    const TempFolder temp;
    const TestClock clock{kMorning};
    auto config = config_for(temp, clock);
    bool failed_once = false;
    config.file_writer = [&failed_once](void* file, std::string_view bytes) {
        return torn_once(failed_once, file, bytes);
    };
    Log log{std::move(config)};
    log.write(LogLevel::Information, "Torn {n}", {LogField{"n", std::int64_t{1}}});
    log.write(LogLevel::Information, "Whole {n}", {LogField{"n", std::int64_t{2}}});
    log.write(LogLevel::Information, "Whole {n}", {LogField{"n", std::int64_t{3}}});
    EXPECT_EQ(log.failures(), 1U);
    const auto recent = log.recent();
    ASSERT_EQ(recent.size(), 3U);
    const auto lines = lines_of(temp.path() / "logs" / "testapp-2026-11-13.log");
    ASSERT_EQ(lines.size(), 3U);
    EXPECT_FALSE(lines.at(0).ends_with("}}")) << "the torn record is a fragment";
    EXPECT_EQ(lines.at(1), Log::to_json_line(recent.at(1)));
    EXPECT_EQ(lines.at(2), Log::to_json_line(recent.at(2)));
}

} // namespace
