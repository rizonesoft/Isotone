// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include <atomic>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <deque>
#include <filesystem>
#include <functional>
#include <initializer_list>
#include <memory>
#include <mutex>
#include <span>
#include <string>
#include <string_view>
#include <utility>
#include <variant>
#include <vector>

namespace isotone::core
{

// The levels of standards/shared.md, "Logging", in rising order.
enum class LogLevel : std::uint8_t
{
    Verbose,
    Debug,
    Information,
    Warning,
    Error,
    Fatal,
};

// The level's name as it appears in a log line ("Information").
[[nodiscard]] std::string_view log_level_name(LogLevel level) noexcept;

#ifdef NDEBUG
inline constexpr bool kDebugBuild = false;
#else
inline constexpr bool kDebugBuild = true;
#endif

// A named value of an event. Strings are UTF-8.
using LogValue = std::variant<std::int64_t, std::uint64_t, double, bool, std::string>;

struct LogField
{
    // name is the placeholder the message template uses ("path" for {path}). Throws std::bad_alloc only.
    LogField(std::string field_name, LogValue field_value) : name{std::move(field_name)}, value{std::move(field_value)}
    {
    }

    std::string name;
    LogValue value;
};

// One event: when, how severe, its message template ("Saved {path} in {elapsed_ms} ms"), and its named values.
struct LogEvent
{
    std::chrono::sys_time<std::chrono::milliseconds> time;
    LogLevel level = LogLevel::Information;
    std::string message_template;
    std::vector<LogField> fields;
};

// Where events go. The file and the memory buffer by default, and the debugger output in a Debug build.
struct LogOutputs
{
    bool file = true;
    bool memory = true;
    bool debugger = kDebugBuild;
};

// Writes bytes to an open file handle; returns false when it wrote fewer than all of them. A test seam.
using LogFileWriter = std::function<bool(void* file, std::string_view bytes)>;

// One configuration per app (standards/shared.md, "Logging").
struct LogConfig
{
    // The app's name; the file name uses it in lowercase ASCII ("stilus-2026-11-13.log"). Not empty.
    std::string app_name;
    // The logs folder (AppFolders::logs); created when the first file is opened.
    std::filesystem::path folder;
    // Events below this level are dropped: Information by default, Debug in a Debug build.
    LogLevel minimum_level = kDebugBuild ? LogLevel::Debug : LogLevel::Information;
    LogOutputs outputs;
    // The memory buffer keeps the newest this many events.
    std::size_t memory_capacity = 1000;
    // A line that would take a file past this size starts a new part.
    std::uint64_t max_file_bytes = 10ULL * 1024ULL * 1024ULL;
    // The newest this many files are kept; older ones are deleted when a new file starts.
    std::size_t max_files = 7;
    // Empty: the system clock. A test passes its own.
    std::function<std::chrono::system_clock::time_point()> clock;
    // Empty: WriteFile until every byte is written. A test passes its own.
    LogFileWriter file_writer;
    // Empty: OutputDebugStringW. A test passes its own.
    std::function<void(std::wstring_view line)> debugger_writer;
};

// The structured log of one app. Create it once in the composition root and pass it down; every member function
// may be called from any thread.
class Log
{
  public:
    // Opens nothing yet: the file is opened by the first write that reaches it.
    explicit Log(LogConfig config);
    ~Log();
    Log(const Log&) = delete;
    Log& operator=(const Log&) = delete;
    Log(Log&&) = delete;
    Log& operator=(Log&&) = delete;

    // Records an event at the current time if level is at or above the minimum. Never throws: a file that cannot be
    // opened or written is counted in failures(), and the event still reaches the memory buffer and the debugger.
    void write(LogLevel level, std::string_view message_template, std::initializer_list<LogField> fields = {}) noexcept;
    void write(LogLevel level, std::string_view message_template, std::span<const LogField> fields) noexcept;

    // The memory buffer, oldest first.
    [[nodiscard]] std::vector<LogEvent> recent() const;

    // How many file opens or writes have failed since the log was created.
    [[nodiscard]] std::uint64_t failures() const noexcept;

    // The event as one JSON line without its line break:
    // {"time":"...Z","level":"...","template":"...","message":"...","fields":{...}}.
    [[nodiscard]] static std::string to_json_line(const LogEvent& event);

    // The template with each {name} replaced by its value; an unknown name stays as written, and {{ and }} are
    // literal braces.
    [[nodiscard]] static std::string render(std::string_view message_template, std::span<const LogField> fields);

  private:
    struct File;

    void write_file_locked(const LogEvent& event, const std::string& line);
    bool open_locked(std::chrono::sys_days day, std::uint64_t incoming_bytes);
    void prune_locked();

    LogConfig config_;
    std::string file_prefix_;
    mutable std::mutex mutex_;
    std::deque<LogEvent> memory_;
    std::unique_ptr<File> file_;
    std::atomic<std::uint64_t> failures_{0};
    bool needs_newline_ = false;
};

} // namespace isotone::core
