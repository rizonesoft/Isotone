// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/settings.h"

#include "isotone/core/error.h"
#include "isotone/core/log.h"
#include "utf.h"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <format>
#include <limits>
#include <mutex>
#include <nlohmann/json.hpp>
#include <optional>
#include <span>
#include <string>
#include <utility>
#include <variant>
#include <vector>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>

namespace isotone::core
{
namespace
{

using Json = nlohmann::json;

constexpr std::string_view kVersionKey{"version"};
constexpr std::string_view kValuesKey{"values"};
// How many numbered names a file kept aside in the same second may try before the move is reported as refused.
constexpr int kMaxAsideNames = 100;

struct Parsed
{
    SettingsDocument kind = SettingsDocument::Unreadable;
    Json values = Json::object();
    std::string reason;
};

Parsed unreadable(std::string reason)
{
    return Parsed{.kind = SettingsDocument::Unreadable, .values = Json::object(), .reason = std::move(reason)};
}

// True when arrays and objects nest deeper than the limit. Brackets inside a string do not count.
bool nests_too_deep(std::string_view text) noexcept
{
    std::size_t depth = 0;
    bool in_string = false;
    bool escaped = false;
    for (const char character : text)
    {
        if (in_string)
        {
            if (escaped)
            {
                escaped = false;
            }
            else if (character == '\\')
            {
                escaped = true;
            }
            else if (character == '"')
            {
                in_string = false;
            }
        }
        else if (character == '"')
        {
            in_string = true;
        }
        else if (character == '[' || character == '{')
        {
            ++depth;
            if (depth > kSettingsMaxDepth)
            {
                return true;
            }
        }
        else if ((character == ']' || character == '}') && depth > 0)
        {
            --depth;
        }
    }
    return false;
}

Parsed parse_document(std::span<const std::byte> bytes)
{
    if (bytes.size() > kSettingsMaxBytes)
    {
        return unreadable(std::format("larger than {} bytes", kSettingsMaxBytes));
    }
    std::string text(bytes.size(), '\0');
    std::ranges::transform(bytes, text.begin(), [](std::byte value) { return static_cast<char>(value); });
    if (nests_too_deep(text))
    {
        return unreadable(std::format("nested deeper than {} levels", kSettingsMaxDepth));
    }
    // No exceptions, no comments: a document that does not parse comes back discarded.
    Json root = Json::parse(text, nullptr, false, false);
    if (root.is_discarded())
    {
        return unreadable("not valid JSON");
    }
    if (!root.is_object())
    {
        return unreadable("not a JSON object");
    }
    const auto version = root.find(kVersionKey);
    if (version == root.end() || !version->is_number_integer())
    {
        return unreadable("without a whole-number version");
    }
    // An unsigned value past the signed range is a version far above this one.
    const bool above_signed =
        version->is_number_unsigned() &&
        version->get<std::uint64_t>() > static_cast<std::uint64_t>(std::numeric_limits<std::int64_t>::max());
    const std::int64_t number = above_signed ? std::numeric_limits<std::int64_t>::max() : version->get<std::int64_t>();
    if (number < 1)
    {
        return unreadable("with a version below 1");
    }
    if (number > kSettingsVersion)
    {
        return Parsed{.kind = SettingsDocument::Newer,
                      .values = Json::object(),
                      .reason =
                          std::format("of version {}, newer than this version reads ({})", number, kSettingsVersion)};
    }
    const auto values = root.find(kValuesKey);
    if (values == root.end() || !values->is_object())
    {
        return unreadable("without a values object");
    }
    return Parsed{.kind = SettingsDocument::Supported, .values = std::move(*values), .reason = {}};
}

// The document as it is written: the version first, then the values with their keys sorted, indented by two.
std::string serialize(const Json& values)
{
    const std::string body = values.dump(2, ' ', false, Json::error_handler_t::strict);
    std::string text = std::format("{{\n  \"{}\": {},\n  \"{}\": ", kVersionKey, kSettingsVersion, kValuesKey);
    text.reserve(text.size() + body.size() + (body.size() / 8) + 4);
    for (const char character : body)
    {
        text.push_back(character);
        if (character == '\n')
        {
            // A JSON string never holds a raw line break, so every one here is the layout's.
            text.append("  ");
        }
    }
    text.append("\n}\n");
    return text;
}

bool any_version(std::span<const std::byte> bytes)
{
    return parse_document(bytes).kind != SettingsDocument::Unreadable;
}

Json to_json(const SettingValue& value)
{
    return std::visit([](const auto& held) { return Json(held); }, value);
}

LogValue to_log_value(const SettingValue& value)
{
    return std::visit([](const auto& held) { return LogValue{held}; }, value);
}

// A JSON whole number as a signed 64-bit value, or nothing when it is past that range (JSON stores those unsigned).
std::optional<std::int64_t> as_int64(const Json& number)
{
    if (number.is_number_unsigned() &&
        number.get<std::uint64_t>() > static_cast<std::uint64_t>(std::numeric_limits<std::int64_t>::max()))
    {
        return std::nullopt;
    }
    return number.get<std::int64_t>();
}

// Two values are the same setting when they are the same kind (a whole number is a whole number however JSON stored
// it) and hold the same value. Whole numbers are compared as signed values in range, never through the library's
// mixed-sign comparison, which casts.
bool same_value(const Json& stored, const Json& wanted)
{
    if (stored.is_number_integer() && wanted.is_number_integer())
    {
        const auto stored_number = as_int64(stored);
        const auto wanted_number = as_int64(wanted);
        return stored_number.has_value() && stored_number == wanted_number;
    }
    const bool same_kind = (stored.is_boolean() && wanted.is_boolean()) ||
                           (stored.is_number_float() && wanted.is_number_float()) ||
                           (stored.is_string() && wanted.is_string());
    return same_kind && stored == wanted;
}

// The changes with one entry per key: the last value given for a key, at the place the key first appeared.
std::vector<const SettingChange*> last_change_per_key(std::span<const SettingChange> changes)
{
    std::vector<const SettingChange*> final_changes;
    for (const SettingChange& change : changes)
    {
        const auto earlier = std::ranges::find_if(
            final_changes, [&change](const SettingChange* other) { return other->key == change.key; });
        if (earlier == final_changes.end())
        {
            final_changes.push_back(&change);
        }
        else
        {
            *earlier = &change;
        }
    }
    return final_changes;
}

bool is_utf8(const std::string& text)
{
    try
    {
        static_cast<void>(detail::utf8_to_utf16(text));
        return true;
    }
    catch (const Error&)
    {
        return false;
    }
}

void check_change(const SettingChange& change)
{
    if (change.key.empty() || !is_utf8(change.key))
    {
        throw Error{"Settings::set", ERROR_INVALID_PARAMETER, "checking a setting's key: it is empty or is not UTF-8"};
    }
    if (const auto* text = std::get_if<std::string>(&change.value); text != nullptr && !is_utf8(*text))
    {
        throw Error{"Settings::set", ERROR_NO_UNICODE_TRANSLATION,
                    "checking the value of " + change.key + ": it is not UTF-8"};
    }
    if (const auto* number = std::get_if<double>(&change.value); number != nullptr && !std::isfinite(*number))
    {
        throw Error{"Settings::set", ERROR_INVALID_PARAMETER,
                    "checking the value of " + change.key + ": it is not a finite number"};
    }
}

std::string utf8(const std::filesystem::path& path)
{
    return detail::utf16_to_utf8(path.native());
}

// What the settings file holds right now, read under its lock.
struct Current
{
    bool present = false;
    Parsed parsed;
};

Current read_current(const AtomicFile::Session& session)
{
    try
    {
        const auto bytes = session.read(any_version);
        if (!bytes)
        {
            return Current{.present = false, .parsed = {}};
        }
        return Current{.present = true, .parsed = parse_document(*bytes)};
    }
    catch (const Error& error)
    {
        if (error.code() != ERROR_FILE_TOO_LARGE)
        {
            throw;
        }
        return Current{.present = true, .parsed = unreadable(std::format("larger than {} bytes", kSettingsMaxBytes))};
    }
}

} // namespace

SettingsDocument inspect_settings_document(std::span<const std::byte> bytes, std::string* rewritten)
{
    const Parsed parsed = parse_document(bytes);
    if (parsed.kind == SettingsDocument::Supported && rewritten != nullptr)
    {
        *rewritten = serialize(parsed.values);
    }
    return parsed.kind;
}

struct Settings::Impl
{
    Impl(const std::filesystem::path& folder, Log& app_log, SettingsOptions store_options)
        : options{std::move(store_options)},
          file{folder / kSettingsFileName, AtomicFileOptions{.max_read_bytes = kSettingsMaxBytes,
                                                             .lock_wait = options.lock_wait,
                                                             .seams = options.seams}},
          log{&app_log}
    {
    }

    // The file's name with a mark and the time, for a file kept aside: settings.unreadable-20261113T101500Z.json.
    [[nodiscard]] std::filesystem::path aside_name(std::string_view mark, int attempt) const
    {
        const auto now = options.clock ? options.clock() : std::chrono::system_clock::now();
        const auto seconds = std::chrono::floor<std::chrono::seconds>(now);
        const std::string suffix = attempt == 1 ? std::string{} : std::format("-{}", attempt);
        const std::string name = std::format("settings.{}-{:%Y%m%dT%H%M%S}Z{}.json", mark, seconds, suffix);
        return file.target().parent_path() / name;
    }

    // Moves the unusable file aside under the lock and says where it went. Throws Error when the move is refused.
    [[nodiscard]] SettingsLoadReport move_aside(const AtomicFile::Session& session, const Parsed& parsed) const
    {
        const bool newer = parsed.kind == SettingsDocument::Newer;
        for (int attempt = 1; attempt <= kMaxAsideNames; ++attempt)
        {
            const auto destination = aside_name(newer ? "newer" : "unreadable", attempt);
            try
            {
                static_cast<void>(session.move_aside(destination));
                return SettingsLoadReport{.outcome =
                                              newer ? SettingsLoad::NewerKeptAside : SettingsLoad::UnreadableKeptAside,
                                          .kept_aside = destination,
                                          .reason = parsed.reason};
            }
            catch (const Error& error)
            {
                if (error.code() != ERROR_ALREADY_EXISTS && error.code() != ERROR_FILE_EXISTS)
                {
                    throw;
                }
            }
        }
        throw Error{"MoveFileExW", ERROR_ALREADY_EXISTS,
                    "moving " + utf8(file.target()) + " aside: every name tried is taken"};
    }

    void log_report(const SettingsLoadReport& found) const
    {
        if (found.outcome == SettingsLoad::UnreadableKeptAside || found.outcome == SettingsLoad::NewerKeptAside)
        {
            log->write(
                LogLevel::Warning, "Settings file {file} is {reason}; it was kept as {kept_aside}",
                {{"file", utf8(file.target())}, {"reason", found.reason}, {"kept_aside", utf8(found.kept_aside)}});
        }
        else if (found.outcome == SettingsLoad::Unavailable)
        {
            log->write(LogLevel::Warning, "Settings file {file} could not be used and was left in place: {reason}",
                       {{"file", utf8(file.target())}, {"reason", found.reason}});
        }
    }

    void load()
    {
        std::string reason;
        try
        {
            const auto bytes = file.read(any_version);
            if (!bytes)
            {
                report = SettingsLoadReport{};
                return;
            }
            Parsed parsed = parse_document(*bytes);
            if (parsed.kind == SettingsDocument::Supported)
            {
                values = std::move(parsed.values);
                report = SettingsLoadReport{.outcome = SettingsLoad::Loaded, .kept_aside = {}, .reason = {}};
                return;
            }
            reason = std::move(parsed.reason);
        }
        catch (const Error& error)
        {
            if (error.code() != ERROR_FILE_TOO_LARGE)
            {
                report =
                    SettingsLoadReport{.outcome = SettingsLoad::Unavailable, .kept_aside = {}, .reason = error.what()};
                log_report(report);
                return;
            }
            reason = std::format("larger than {} bytes", kSettingsMaxBytes);
        }

        // The file is unusable. Look again under the lock, so a file another process has just replaced is never
        // the one moved aside, and move it in the same locked step.
        if (options.before_move_aside)
        {
            options.before_move_aside();
        }
        try
        {
            const auto session = file.lock();
            Current current = read_current(session);
            if (!current.present)
            {
                report = SettingsLoadReport{};
            }
            else if (current.parsed.kind == SettingsDocument::Supported)
            {
                values = std::move(current.parsed.values);
                report = SettingsLoadReport{.outcome = SettingsLoad::Loaded, .kept_aside = {}, .reason = {}};
            }
            else
            {
                report = move_aside(session, current.parsed);
            }
        }
        catch (const Error& error)
        {
            report = SettingsLoadReport{.outcome = SettingsLoad::Unavailable,
                                        .kept_aside = {},
                                        .reason = reason + "; it could not be moved aside: " + error.what()};
        }
        log_report(report);
    }

    void apply(std::span<const SettingChange> changes)
    {
        for (const SettingChange& change : changes)
        {
            check_change(change);
        }
        const std::scoped_lock guard{mutex};
        Json next = Json::object();
        std::vector<const SettingChange*> changed;
        std::optional<SettingsLoadReport> moved;
        try
        {
            const auto session = file.lock();
            Current current = read_current(session);
            const bool unusable = current.present && current.parsed.kind != SettingsDocument::Supported;
            if (current.present && !unusable)
            {
                next = std::move(current.parsed.values);
            }
            // Each key is compared once, by its final value, with what the file holds.
            for (const SettingChange* change : last_change_per_key(changes))
            {
                Json wanted = to_json(change->value);
                const auto stored = next.find(change->key);
                if (stored == next.end())
                {
                    next.emplace(change->key, std::move(wanted));
                    changed.push_back(change);
                }
                else if (!same_value(*stored, wanted))
                {
                    *stored = std::move(wanted);
                    changed.push_back(change);
                }
            }
            if (!changed.empty())
            {
                const std::string text = serialize(next);
                if (text.size() > kSettingsMaxBytes)
                {
                    throw Error{"Settings::set", ERROR_FILE_TOO_LARGE,
                                std::format("saving {}: the settings would take {} bytes, over the limit of {}",
                                            utf8(file.target()), text.size(), kSettingsMaxBytes)};
                }
                // Only a write that will go ahead moves an unusable file aside: a refused change leaves it in place.
                if (unusable)
                {
                    moved = move_aside(session, current.parsed);
                }
                session.write(std::as_bytes(std::span{text}));
            }
        }
        catch (const Error& error)
        {
            if (moved)
            {
                report = *moved;
                log_report(report);
            }
            log->write(LogLevel::Error, "Saving settings to {file} failed: {error}",
                       {{"file", utf8(file.target())}, {"error", std::string{error.what()}}});
            throw;
        }
        values = std::move(next);
        if (moved)
        {
            report = *moved;
            log_report(report);
        }
        for (const SettingChange* change : changed)
        {
            log->write(LogLevel::Information, "Setting {key} changed to {value}",
                       {{"key", change->key}, {"value", to_log_value(change->value)}});
        }
    }

    SettingsOptions options;
    AtomicFile file;
    Log* log;
    mutable std::mutex mutex;
    Json values = Json::object();
    SettingsLoadReport report;
};

Settings::Settings(const std::filesystem::path& folder, Log& log, SettingsOptions options)
    : impl_{std::make_unique<Impl>(folder, log, std::move(options))}
{
    impl_->load();
}

Settings::~Settings() = default;

bool Settings::get_bool(std::string_view key, bool fallback) const
{
    const std::scoped_lock guard{impl_->mutex};
    const auto found = impl_->values.find(key);
    return found != impl_->values.end() && found->is_boolean() ? found->get<bool>() : fallback;
}

std::int64_t Settings::get_int(std::string_view key, std::int64_t fallback) const
{
    const std::scoped_lock guard{impl_->mutex};
    const auto found = impl_->values.find(key);
    if (found == impl_->values.end() || !found->is_number_integer())
    {
        return fallback;
    }
    return as_int64(*found).value_or(fallback);
}

double Settings::get_double(std::string_view key, double fallback) const
{
    const std::scoped_lock guard{impl_->mutex};
    const auto found = impl_->values.find(key);
    return found != impl_->values.end() && found->is_number() ? found->get<double>() : fallback;
}

std::string Settings::get_string(std::string_view key, std::string fallback) const
{
    const std::scoped_lock guard{impl_->mutex};
    const auto found = impl_->values.find(key);
    return found != impl_->values.end() && found->is_string() ? found->get<std::string>() : std::move(fallback);
}

void Settings::set(std::string_view key, SettingValue value)
{
    const SettingChange change{std::string{key}, std::move(value)};
    impl_->apply(std::span{&change, 1});
}

void Settings::set(std::span<const SettingChange> changes)
{
    impl_->apply(changes);
}

void Settings::set(std::initializer_list<SettingChange> changes)
{
    impl_->apply(std::span{changes.begin(), changes.size()});
}

SettingsLoadReport Settings::load_report() const
{
    const std::scoped_lock guard{impl_->mutex};
    return impl_->report;
}

const std::filesystem::path& Settings::file() const noexcept
{
    return impl_->file.target();
}

} // namespace isotone::core
