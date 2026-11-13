// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include "isotone/core/atomic_file.h"

#include <chrono>
#include <cstddef>
#include <cstdint>
#include <filesystem>
#include <functional>
#include <initializer_list>
#include <memory>
#include <span>
#include <string>
#include <string_view>
#include <utility>
#include <variant>

namespace isotone::core
{

class Log;

// The version this build writes and the newest it reads. A file of a newer version is kept aside, never overwritten.
inline constexpr std::int64_t kSettingsVersion = 1;
// The largest settings file read or written, and the deepest nesting read (standards/cpp.md, "Untrusted input").
inline constexpr std::uint64_t kSettingsMaxBytes = 4ULL * 1024ULL * 1024ULL;
inline constexpr std::size_t kSettingsMaxDepth = 64;
// The settings file's name inside the app's settings folder (AppFolders::settings).
inline constexpr std::wstring_view kSettingsFileName{L"settings.json"};

// A setting's value. Strings are UTF-8 and a double is finite. A setting never holds a credential: every change
// is logged with its value.
using SettingValue = std::variant<bool, std::int64_t, double, std::string>;

struct SettingChange
{
    // Throws std::bad_alloc only.
    SettingChange(std::string setting_key, SettingValue setting_value)
        : key{std::move(setting_key)}, value{std::move(setting_value)}
    {
    }

    std::string key;
    SettingValue value;
};

// What a run of bytes is as a settings document.
enum class SettingsDocument : std::uint8_t
{
    // {"version": 1, "values": {...}}: this build reads it.
    Supported,
    // Well formed, with a version above kSettingsVersion.
    Newer,
    // Not JSON, not that shape, over kSettingsMaxBytes, or nested deeper than kSettingsMaxDepth.
    Unreadable,
};

// Reads bytes exactly as the store reads its file, touching no file. When they are Supported and rewritten is not
// null, *rewritten receives the document as the store would write it. For the fuzz target and tests. Throws
// std::bad_alloc only. Any thread.
[[nodiscard]] SettingsDocument inspect_settings_document(std::span<const std::byte> bytes,
                                                         std::string* rewritten = nullptr);

// What the store found when it was created.
enum class SettingsLoad : std::uint8_t
{
    // No settings file yet: every get returns its default.
    NoFile,
    Loaded,
    // The file was Unreadable and was moved aside to kept_aside; the store starts from the defaults.
    UnreadableKeptAside,
    // The file was Newer and was moved aside to kept_aside; the store starts from the defaults.
    NewerKeptAside,
    // The file could not be opened, or could not be used and could not be moved aside (a folder that cannot be
    // written): it was left where it is, and the store starts from the defaults.
    Unavailable,
};

struct SettingsLoadReport
{
    SettingsLoad outcome = SettingsLoad::NoFile;
    // Where the file was moved, for the two KeptAside outcomes.
    std::filesystem::path kept_aside;
    // Why, in a sentence, for every outcome but NoFile and Loaded.
    std::string reason;
};

struct SettingsOptions
{
    // Empty: the system clock. Names a file kept aside. A test passes its own.
    std::function<std::chrono::system_clock::time_point()> clock;
    // How long a set waits for another process writing the same file.
    std::chrono::milliseconds lock_wait{2000};
    // Test seams: production code leaves them empty. before_move_aside runs after a load found the file unusable
    // and before it takes the lock to look again.
    AtomicFileSeams seams;
    std::function<void()> before_move_aside;
};

// One app's settings: a versioned JSON file, settings.json in the settings folder, read once when the store is
// created and rewritten whole through AtomicFile on every change. Create it once in the composition root and pass
// it down; every member function may be called from any thread. A set is a file write with a flush: call it when
// the user commits a value, not for every step of a drag, and change several settings with one call.
class Settings
{
  public:
    // Reads <folder>\settings.json. Never throws for a file problem: load_report() says what was found, and a file
    // that is unreadable or newer is moved aside and logged as a Warning. log must outlive the store.
    Settings(const std::filesystem::path& folder, Log& log, SettingsOptions options = {});
    ~Settings();
    Settings(const Settings&) = delete;
    Settings& operator=(const Settings&) = delete;
    Settings(Settings&&) = delete;
    Settings& operator=(Settings&&) = delete;

    // The value of key, or fallback when the key is absent or holds another type. get_double also reads an integer.
    [[nodiscard]] bool get_bool(std::string_view key, bool fallback) const;
    [[nodiscard]] std::int64_t get_int(std::string_view key, std::int64_t fallback) const;
    [[nodiscard]] double get_double(std::string_view key, double fallback) const;
    [[nodiscard]] std::string get_string(std::string_view key, std::string fallback) const;

    // Changes one setting, or several in one write. The file is read again under its lock and only these keys are
    // changed in it, so another process's settings are kept; a key given more than once takes its last value; a key
    // that already holds its value changes nothing,
    // and when nothing changes nothing is written or logged. Each changed key is logged as one Information event
    // naming the key and the new value. Throws Error, with the file, the values in memory, and the change log all
    // as they were, when a key is empty or not UTF-8, a string is not UTF-8, a double is not finite, the document
    // would pass kSettingsMaxBytes, or the file cannot be written.
    void set(std::string_view key, SettingValue value);
    void set(std::span<const SettingChange> changes);
    void set(std::initializer_list<SettingChange> changes);

    [[nodiscard]] SettingsLoadReport load_report() const;
    // <folder>\settings.json.
    [[nodiscard]] const std::filesystem::path& file() const noexcept;

  private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace isotone::core
