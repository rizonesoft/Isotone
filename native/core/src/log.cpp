// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/log.h"

#include "utf.h"

#include <algorithm>
#include <array>
#include <charconv>
#include <cmath>
#include <format>
#include <fstream>
#include <limits>
#include <memory>
#include <string>
#include <system_error>
#include <utility>

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

// WriteFile takes a DWORD count; write in pieces well under it.
constexpr std::size_t kMaxWriteChunk = std::size_t{1} << 30U;
// The length of an ISO 8601 date, "2026-11-13".
constexpr std::size_t kDateLength = 10;
constexpr std::string_view kLogExtension{".log"};

// The handle's owner: closes it on destruction.
struct HandleCloser
{
    void operator()(HANDLE handle) const noexcept
    {
        if (handle != nullptr && handle != INVALID_HANDLE_VALUE)
        {
            CloseHandle(handle);
        }
    }
};

bool write_all(void* file, std::string_view bytes)
{
    while (!bytes.empty())
    {
        const auto chunk = static_cast<DWORD>(std::min(bytes.size(), kMaxWriteChunk));
        DWORD written = 0;
        if (WriteFile(file, bytes.data(), chunk, &written, nullptr) == FALSE || written == 0)
        {
            return false;
        }
        bytes.remove_prefix(written);
    }
    return true;
}

// Appends the UTF-8 text as a JSON string body, replacing each invalid sequence with U+FFFD (RFC 8259).
void append_json_text(std::string& out, std::string_view text)
{
    constexpr std::string_view kReplacement{"\xEF\xBF\xBD"};
    constexpr std::array<char, 16> kHex{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
    std::size_t index = 0;
    while (index < text.size())
    {
        const auto lead = static_cast<unsigned char>(text.at(index));
        if (lead < 0x80U)
        {
            switch (lead)
            {
            case '"':
                out += "\\\"";
                break;
            case '\\':
                out += "\\\\";
                break;
            case '\n':
                out += "\\n";
                break;
            case '\r':
                out += "\\r";
                break;
            case '\t':
                out += "\\t";
                break;
            case '\b':
                out += "\\b";
                break;
            case '\f':
                out += "\\f";
                break;
            default:
                if (lead < 0x20U)
                {
                    out += "\\u00";
                    out.push_back(kHex.at(lead >> 4U));
                    out.push_back(kHex.at(lead & 0x0FU));
                }
                else
                {
                    out.push_back(static_cast<char>(lead));
                }
            }
            ++index;
            continue;
        }
        std::size_t length = 0;
        std::uint32_t minimum = 0;
        std::uint32_t code = 0;
        if ((lead & 0xE0U) == 0xC0U)
        {
            length = 2;
            minimum = 0x80U;
            code = lead & 0x1FU;
        }
        else if ((lead & 0xF0U) == 0xE0U)
        {
            length = 3;
            minimum = 0x800U;
            code = lead & 0x0FU;
        }
        else if ((lead & 0xF8U) == 0xF0U)
        {
            length = 4;
            minimum = 0x10000U;
            code = lead & 0x07U;
        }
        bool valid = length != 0 && index + length <= text.size();
        for (std::size_t k = 1; valid && k < length; ++k)
        {
            const auto next = static_cast<unsigned char>(text.at(index + k));
            valid = (next & 0xC0U) == 0x80U;
            code = (code << 6U) | (next & 0x3FU);
        }
        valid = valid && code >= minimum && code <= 0x10FFFFU && (code < 0xD800U || code > 0xDFFFU);
        if (valid)
        {
            out.append(text.substr(index, length));
            index += length;
        }
        else
        {
            out.append(kReplacement);
            ++index;
        }
    }
}

template <typename Number> void append_number(std::string& out, Number value)
{
    std::array<char, 32> buffer{};
    const auto result = std::to_chars(buffer.data(), std::to_address(buffer.end()), value);
    out.append(std::string_view{buffer.data(), result.ptr});
}

// The value as JSON: numbers locale-free, a non-finite double as null.
void append_json_value(std::string& out, const LogValue& value)
{
    if (const auto* text = std::get_if<std::string>(&value))
    {
        out.push_back('"');
        append_json_text(out, *text);
        out.push_back('"');
    }
    else if (const auto* flag = std::get_if<bool>(&value))
    {
        out += *flag ? "true" : "false";
    }
    else if (const auto* real = std::get_if<double>(&value))
    {
        if (std::isfinite(*real))
        {
            append_number(out, *real);
        }
        else
        {
            out += "null";
        }
    }
    else if (const auto* whole = std::get_if<std::int64_t>(&value))
    {
        append_number(out, *whole);
    }
    else
    {
        append_number(out, std::get<std::uint64_t>(value));
    }
}

// The value as message text: strings as written, numbers locale-free.
void append_text_value(std::string& out, const LogValue& value)
{
    if (const auto* text = std::get_if<std::string>(&value))
    {
        out += *text;
    }
    else if (const auto* flag = std::get_if<bool>(&value))
    {
        out += *flag ? "true" : "false";
    }
    else if (const auto* real = std::get_if<double>(&value))
    {
        append_number(out, *real);
    }
    else if (const auto* whole = std::get_if<std::int64_t>(&value))
    {
        append_number(out, *whole);
    }
    else
    {
        append_number(out, std::get<std::uint64_t>(value));
    }
}

std::string lowercase_ascii(std::string_view text)
{
    std::string out{text};
    std::ranges::transform(out, out.begin(), [](char letter) {
        return letter >= 'A' && letter <= 'Z' ? static_cast<char>(letter - 'A' + 'a') : letter;
    });
    return out;
}

// A log file's place in the order: its date, then its part.
struct FileKey
{
    std::string date;
    unsigned part = 0;
    std::filesystem::path path;
};

// Parses "<prefix>-YYYY-MM-DD.log" or "<prefix>-YYYY-MM-DD.<part>.log"; false for any other name.
bool parse_file_name(std::string_view name, std::string_view prefix, FileKey& key)
{
    if (name.size() < prefix.size() + 1 + kDateLength + kLogExtension.size() || !name.starts_with(prefix) ||
        name.at(prefix.size()) != '-' || !name.ends_with(kLogExtension))
    {
        return false;
    }
    name.remove_prefix(prefix.size() + 1);
    const std::string_view date = name.substr(0, kDateLength);
    for (std::size_t i = 0; i < date.size(); ++i)
    {
        const bool dash = i == 4 || i == 7;
        if (dash ? date.at(i) != '-' : (date.at(i) < '0' || date.at(i) > '9'))
        {
            return false;
        }
    }
    name.remove_prefix(kDateLength);
    name.remove_suffix(kLogExtension.size());
    unsigned part = 0;
    if (!name.empty())
    {
        if (name.front() != '.' || name.size() < 2)
        {
            return false;
        }
        name.remove_prefix(1);
        const auto* const last = std::to_address(name.end());
        const auto result = std::from_chars(std::to_address(name.begin()), last, part);
        if (result.ec != std::errc{} || result.ptr != last)
        {
            return false;
        }
    }
    key.date = std::string{date};
    key.part = part;
    return true;
}

std::vector<FileKey> list_log_files(const std::filesystem::path& folder, std::string_view prefix)
{
    std::vector<FileKey> files;
    std::error_code error;
    for (std::filesystem::directory_iterator it{folder, error}, end; !error && it != end; it.increment(error))
    {
        FileKey key;
        const std::string name = detail::utf16_to_utf8(it->path().filename().native());
        if (it->is_regular_file(error) && parse_file_name(name, prefix, key))
        {
            key.path = it->path();
            files.push_back(std::move(key));
        }
    }
    std::ranges::sort(files, [](const FileKey& left, const FileKey& right) {
        return left.date != right.date ? left.date < right.date : left.part < right.part;
    });
    return files;
}

// The files of one app on one day.
struct DayFiles
{
    std::string_view prefix;
    std::string_view date;
};

// The highest part number already written for the day, or 0.
unsigned last_part(const std::filesystem::path& folder, DayFiles day)
{
    unsigned part = 0;
    for (const FileKey& key : list_log_files(folder, day.prefix))
    {
        if (key.date == day.date)
        {
            part = std::max(part, key.part);
        }
    }
    return part;
}

enum class PartState : std::uint8_t
{
    Opened,
    Full,
    Failed,
};

struct OpenedPart
{
    std::unique_ptr<void, HandleCloser> handle;
    std::uint64_t size = 0;
    bool ends_with_break = true;
};

// Opens the part for appending unless the incoming line would take it past max_bytes. Its size and last byte are
// read first, through a stream, so a record torn by an earlier failure is followed by a fresh line.
PartState open_part(const std::filesystem::path& path, std::uint64_t incoming_bytes, std::uint64_t max_bytes,
                    OpenedPart& opened)
{
    {
        std::ifstream existing{path, std::ios::binary | std::ios::ate};
        if (existing)
        {
            const auto end = static_cast<std::streamoff>(existing.tellg());
            opened.size = end > 0 ? static_cast<std::uint64_t>(end) : 0;
            if (opened.size > 0)
            {
                if (opened.size + incoming_bytes > max_bytes)
                {
                    return PartState::Full;
                }
                char last = '\n';
                existing.seekg(-1, std::ios::end);
                existing.get(last);
                opened.ends_with_break = last == '\n';
            }
        }
    }
    HANDLE raw = CreateFileW(path.c_str(), FILE_APPEND_DATA, FILE_SHARE_READ | FILE_SHARE_DELETE, nullptr, OPEN_ALWAYS,
                             FILE_ATTRIBUTE_NORMAL, nullptr);
    if (raw == INVALID_HANDLE_VALUE)
    {
        return PartState::Failed;
    }
    opened.handle.reset(raw);
    return PartState::Opened;
}

} // namespace

struct Log::File
{
    std::unique_ptr<void, HandleCloser> handle;
    std::chrono::sys_days day;
    unsigned part = 0;
    std::uint64_t size = 0;
};

std::string_view log_level_name(LogLevel level) noexcept
{
    switch (level)
    {
    case LogLevel::Verbose:
        return "Verbose";
    case LogLevel::Debug:
        return "Debug";
    case LogLevel::Information:
        return "Information";
    case LogLevel::Warning:
        return "Warning";
    case LogLevel::Error:
        return "Error";
    case LogLevel::Fatal:
        return "Fatal";
    }
    return "Unknown";
}

Log::Log(LogConfig config) : config_{std::move(config)}, file_prefix_{lowercase_ascii(config_.app_name)}
{
    if (!config_.file_writer)
    {
        config_.file_writer = write_all;
    }
}

Log::~Log() = default;

void Log::write(LogLevel level, std::string_view message_template, std::initializer_list<LogField> fields) noexcept
{
    write(level, message_template, std::span<const LogField>{fields.begin(), fields.size()});
}

void Log::write(LogLevel level, std::string_view message_template, std::span<const LogField> fields) noexcept
{
    try
    {
        if (level < config_.minimum_level)
        {
            return;
        }
        const auto now = config_.clock ? config_.clock() : std::chrono::system_clock::now();
        LogEvent event{.time = std::chrono::floor<std::chrono::milliseconds>(now),
                       .level = level,
                       .message_template = std::string{message_template},
                       .fields = std::vector<LogField>{fields.begin(), fields.end()}};
        const std::string line = to_json_line(event);

        const std::scoped_lock lock{mutex_};
        if (config_.outputs.file)
        {
            write_file_locked(event, line);
        }
        if (config_.outputs.debugger)
        {
            const std::wstring wide = detail::utf8_to_utf16(line + "\n");
            if (config_.debugger_writer)
            {
                config_.debugger_writer(wide);
            }
            else
            {
                OutputDebugStringW(wide.c_str());
            }
        }
        if (config_.outputs.memory && config_.memory_capacity > 0)
        {
            memory_.push_back(std::move(event));
            while (memory_.size() > config_.memory_capacity)
            {
                memory_.pop_front();
            }
        }
    }
    catch (...)
    {
        failures_.fetch_add(1, std::memory_order_relaxed);
    }
}

std::vector<LogEvent> Log::recent() const
{
    const std::scoped_lock lock{mutex_};
    return {memory_.begin(), memory_.end()};
}

std::uint64_t Log::failures() const noexcept
{
    return failures_.load(std::memory_order_relaxed);
}

void Log::write_file_locked(const LogEvent& event, const std::string& line)
{
    const auto day = std::chrono::floor<std::chrono::days>(event.time);
    // The line, its break, and at most one break before it.
    const std::uint64_t incoming = line.size() + 2;
    if (!open_locked(day, incoming))
    {
        failures_.fetch_add(1, std::memory_order_relaxed);
        return;
    }
    std::string bytes;
    bytes.reserve(line.size() + 2);
    if (needs_newline_)
    {
        bytes.push_back('\n');
    }
    bytes += line;
    bytes.push_back('\n');
    if (!config_.file_writer(file_->handle.get(), bytes))
    {
        // Part of the line may be on disk: reopen on the next write, which starts on a fresh line.
        failures_.fetch_add(1, std::memory_order_relaxed);
        file_.reset();
        return;
    }
    file_->size += bytes.size();
    needs_newline_ = false;
}

bool Log::open_locked(std::chrono::sys_days day, std::uint64_t incoming_bytes)
{
    if (file_ && file_->day == day && (file_->size == 0 || file_->size + incoming_bytes <= config_.max_file_bytes))
    {
        return true;
    }
    const std::string date = std::format("{:%Y-%m-%d}", day);
    unsigned part = file_ && file_->day == day
                        ? file_->part + 1
                        : last_part(config_.folder, DayFiles{.prefix = file_prefix_, .date = date});
    file_.reset();

    std::error_code error;
    std::filesystem::create_directories(config_.folder, error);
    if (error)
    {
        return false;
    }
    for (;; ++part)
    {
        const std::string name = part == 0 ? std::format("{}-{}.log", file_prefix_, date)
                                           : std::format("{}-{}.{}.log", file_prefix_, date, part);
        OpenedPart opened;
        const PartState state =
            open_part(config_.folder / detail::utf8_to_utf16(name), incoming_bytes, config_.max_file_bytes, opened);
        if (state == PartState::Full)
        {
            continue;
        }
        if (state == PartState::Failed)
        {
            return false;
        }
        needs_newline_ = !opened.ends_with_break;
        const bool is_new = opened.size == 0;
        file_ = std::make_unique<File>(
            File{.handle = std::move(opened.handle), .day = day, .part = part, .size = opened.size});
        if (is_new)
        {
            prune_locked();
        }
        return true;
    }
}

void Log::prune_locked()
{
    std::vector<FileKey> files = list_log_files(config_.folder, file_prefix_);
    if (files.size() <= config_.max_files)
    {
        return;
    }
    const std::size_t surplus = files.size() - config_.max_files;
    for (std::size_t i = 0; i < surplus; ++i)
    {
        std::error_code error;
        std::filesystem::remove(files.at(i).path, error);
        if (error)
        {
            failures_.fetch_add(1, std::memory_order_relaxed);
        }
    }
}

std::string Log::to_json_line(const LogEvent& event)
{
    std::string out;
    out.reserve(128 + (event.message_template.size() * 2));
    out += std::format(R"({{"time":"{:%Y-%m-%dT%H:%M:%S}Z","level":"{}","template":")", event.time,
                       log_level_name(event.level));
    append_json_text(out, event.message_template);
    out += R"(","message":")";
    append_json_text(out, render(event.message_template, event.fields));
    out += R"(","fields":{)";
    bool first = true;
    for (const LogField& field : event.fields)
    {
        if (!first)
        {
            out.push_back(',');
        }
        first = false;
        out.push_back('"');
        append_json_text(out, field.name);
        out += "\":";
        append_json_value(out, field.value);
    }
    out += "}}";
    return out;
}

std::string Log::render(std::string_view message_template, std::span<const LogField> fields)
{
    std::string out;
    out.reserve(message_template.size());
    std::size_t index = 0;
    while (index < message_template.size())
    {
        const char character = message_template.at(index);
        if ((character == '{' || character == '}') && index + 1 < message_template.size() &&
            message_template.at(index + 1) == character)
        {
            out.push_back(character);
            index += 2;
            continue;
        }
        if (character == '{')
        {
            const std::size_t close = message_template.find('}', index + 1);
            if (close != std::string_view::npos)
            {
                const std::string_view name = message_template.substr(index + 1, close - index - 1);
                const auto found =
                    std::ranges::find_if(fields, [name](const LogField& field) { return field.name == name; });
                if (found != fields.end())
                {
                    append_text_value(out, found->value);
                    index = close + 1;
                    continue;
                }
            }
        }
        out.push_back(character);
        ++index;
    }
    return out;
}

} // namespace isotone::core
