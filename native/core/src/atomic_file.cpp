// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/atomic_file.h"

#include "isotone/core/error.h"
#include "utf.h"

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <format>
#include <limits>
#include <memory>
#include <optional>
#include <span>
#include <string>
#include <string_view>
#include <system_error>
#include <thread>
#include <utility>
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

// One read or write call moves at most this much. It is a multiple of every sector size in use, and VirtualAlloc
// aligns a buffer of it to a page, which is what an unbuffered read needs.
constexpr DWORD kChunkBytes = 1U << 20U;
// How long a lock file that reports access denied is retried: a lock its last holder is still closing reads that
// way for an instant, and a folder that cannot be written reads that way for good.
constexpr std::chrono::milliseconds kDeniedWait{250};
// How long opening a file for reading waits out a sharing violation (a replace in progress holds it briefly).
constexpr std::chrono::milliseconds kSharingWait{250};
constexpr std::chrono::milliseconds kRetryPause{10};
// How often a read without the lock is tried again when a write crossed it, before it takes the lock.
constexpr int kUnlockedReadTries = 4;

struct HandleCloser
{
    void operator()(HANDLE handle) const noexcept
    {
        CloseHandle(handle);
    }
};
using UniqueHandle = std::unique_ptr<void, HandleCloser>;

// CreateFileW's result as an owner: empty when the call failed (read GetLastError at once).
UniqueHandle own(HANDLE handle) noexcept
{
    return UniqueHandle{handle == INVALID_HANDLE_VALUE ? nullptr : handle};
}

struct VirtualFreeDeleter
{
    void operator()(void* memory) const noexcept
    {
        VirtualFree(memory, 0, MEM_RELEASE);
    }
};

// What went wrong in a step, kept as parts so a second failure can be added to the report.
struct Failure
{
    std::string call;
    DWORD code = 0;
    std::string context;
};

std::string utf8(const std::filesystem::path& path)
{
    return detail::utf16_to_utf8(path.native());
}

void remove_quietly(const std::filesystem::path& file) noexcept
{
    // A file that cannot be removed here is overwritten or settled by the next write or read.
    static_cast<void>(DeleteFileW(file.c_str()));
}

bool exists_quietly(const std::filesystem::path& file) noexcept
{
    return GetFileAttributesW(file.c_str()) != INVALID_FILE_ATTRIBUTES;
}

bool file_exists(const std::filesystem::path& file)
{
    if (GetFileAttributesW(file.c_str()) != INVALID_FILE_ATTRIBUTES)
    {
        return true;
    }
    const DWORD code = GetLastError();
    if (code == ERROR_FILE_NOT_FOUND || code == ERROR_PATH_NOT_FOUND)
    {
        return false;
    }
    throw Error{"GetFileAttributesW", code, "checking " + utf8(file)};
}

DWORD injected(const AtomicFileSeams& seams, AtomicFileStep step)
{
    return seams.fail ? seams.fail(step) : 0U;
}

UniqueHandle open_for_reading(const std::filesystem::path& file, DWORD flags, DWORD& code)
{
    const auto deadline = std::chrono::steady_clock::now() + kSharingWait;
    for (;;)
    {
        UniqueHandle handle =
            own(CreateFileW(file.c_str(), GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, nullptr,
                            OPEN_EXISTING, flags, nullptr));
        code = handle ? ERROR_SUCCESS : GetLastError();
        if (code != ERROR_SHARING_VIOLATION || std::chrono::steady_clock::now() >= deadline)
        {
            return handle;
        }
        std::this_thread::sleep_for(kRetryPause);
    }
}

Error too_large(const std::filesystem::path& file, std::uint64_t bytes, std::uint64_t max_bytes)
{
    return Error{"AtomicFile::read", ERROR_FILE_TOO_LARGE,
                 std::format("reading {}: it is {} bytes, over the limit of {}", utf8(file), bytes, max_bytes)};
}

// Reads an open file to its end into bytes. False when an unbuffered read was refused before anything was read.
bool read_to_end(HANDLE handle, const std::filesystem::path& file, std::uint64_t max_bytes, bool unbuffered,
                 std::vector<std::byte>& bytes)
{
    const std::unique_ptr<void, VirtualFreeDeleter> buffer{
        VirtualAlloc(nullptr, kChunkBytes, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)};
    if (!buffer)
    {
        throw Error{"VirtualAlloc", GetLastError(), "reading " + utf8(file)};
    }
    for (;;)
    {
        DWORD got = 0;
        if (ReadFile(handle, buffer.get(), kChunkBytes, &got, nullptr) == FALSE)
        {
            const DWORD code = GetLastError();
            if (code == ERROR_HANDLE_EOF)
            {
                return true;
            }
            if (unbuffered && bytes.empty() && code == ERROR_INVALID_PARAMETER)
            {
                return false;
            }
            throw Error{"ReadFile", code, "reading " + utf8(file)};
        }
        if (got == 0)
        {
            return true;
        }
        if (bytes.size() + got > max_bytes)
        {
            // The file grew after it was measured.
            throw too_large(file, bytes.size() + got, max_bytes);
        }
        const std::span<const std::byte> chunk{static_cast<const std::byte*>(buffer.get()), got};
        bytes.insert(bytes.end(), chunk.begin(), chunk.end());
    }
}

// Which file a name holds: the volume and the file's index on it. Two opens of one name give the same identity
// exactly when no other file took the name in between.
struct FileIdentity
{
    DWORD volume = 0;
    std::uint64_t index = 0;

    bool operator==(const FileIdentity&) const = default;
};

std::optional<FileIdentity> identity_of(HANDLE handle) noexcept
{
    BY_HANDLE_FILE_INFORMATION information{};
    if (GetFileInformationByHandle(handle, &information) == FALSE)
    {
        return std::nullopt;
    }
    return FileIdentity{.volume = information.dwVolumeSerialNumber,
                        .index = (static_cast<std::uint64_t>(information.nFileIndexHigh) << 32U) |
                                 information.nFileIndexLow};
}

// The identity of the file at a name now, or nothing when there is none (or it cannot be told).
std::optional<FileIdentity> identity_at(const std::filesystem::path& file) noexcept
{
    const UniqueHandle handle =
        own(CreateFileW(file.c_str(), FILE_READ_ATTRIBUTES, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                        nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr));
    return handle ? identity_of(handle.get()) : std::nullopt;
}

// One attempt at reading the whole file, or nothing when it does not exist. unbuffered reads the device rather than
// the file cache; when the file system refuses that, refused is set and nothing is returned. identity, when given,
// receives which file was read. Throws Error; a file over max_bytes is ERROR_FILE_TOO_LARGE, decided before
// anything is allocated for it.
std::optional<std::vector<std::byte>> read_once(const std::filesystem::path& file, std::uint64_t max_bytes,
                                                bool unbuffered, bool& refused,
                                                std::optional<FileIdentity>* identity = nullptr)
{
    refused = false;
    const DWORD flags = FILE_ATTRIBUTE_NORMAL | FILE_FLAG_SEQUENTIAL_SCAN | (unbuffered ? FILE_FLAG_NO_BUFFERING : 0U);
    DWORD code = ERROR_SUCCESS;
    const UniqueHandle handle = open_for_reading(file, flags, code);
    if (identity != nullptr)
    {
        *identity = handle ? identity_of(handle.get()) : std::nullopt;
    }
    if (!handle)
    {
        if (code == ERROR_FILE_NOT_FOUND || code == ERROR_PATH_NOT_FOUND)
        {
            return std::nullopt;
        }
        refused = unbuffered &&
                  (code == ERROR_INVALID_PARAMETER || code == ERROR_NOT_SUPPORTED || code == ERROR_INVALID_FUNCTION);
        if (refused)
        {
            return std::nullopt;
        }
        throw Error{"CreateFileW", code, "opening " + utf8(file)};
    }

    LARGE_INTEGER size{};
    if (GetFileSizeEx(handle.get(), &size) == FALSE)
    {
        throw Error{"GetFileSizeEx", GetLastError(), "measuring " + utf8(file)};
    }
    const auto file_bytes = static_cast<std::uint64_t>(size.QuadPart);
    if (file_bytes > max_bytes)
    {
        throw too_large(file, file_bytes, max_bytes);
    }
    std::vector<std::byte> bytes;
    bytes.reserve(static_cast<std::size_t>(file_bytes));
    refused = !read_to_end(handle.get(), file, max_bytes, unbuffered, bytes);
    if (refused)
    {
        return std::nullopt;
    }
    return bytes;
}

// The whole file, or nothing when it does not exist. unbuffered reads the device rather than the file cache, and
// falls back to an ordinary read where the file system refuses that. Throws Error as read_once does.
std::optional<std::vector<std::byte>> read_whole(const std::filesystem::path& file, std::uint64_t max_bytes,
                                                 bool unbuffered, std::optional<FileIdentity>* identity = nullptr)
{
    bool refused = false;
    if (unbuffered)
    {
        auto bytes = read_once(file, max_bytes, true, refused, identity);
        if (!refused)
        {
            return bytes;
        }
    }
    return read_once(file, max_bytes, false, refused, identity);
}

// Reads file back from the device and compares it with expected. Nothing when they agree.
std::optional<Failure> read_back_failure(const std::filesystem::path& file, std::span<const std::byte> expected,
                                         AtomicFileStep step, const AtomicFileSeams& seams)
{
    if (const DWORD code = injected(seams, step); code != 0)
    {
        return Failure{.call = "ReadFile", .code = code, .context = "reading back " + utf8(file)};
    }
    std::vector<std::byte> actual;
    try
    {
        // A file longer than what was written is already wrong, so the size written is the limit.
        auto read = read_whole(file, expected.size(), true);
        if (!read)
        {
            return Failure{
                .call = "CreateFileW", .code = ERROR_FILE_NOT_FOUND, .context = "reading back " + utf8(file)};
        }
        actual = std::move(*read);
    }
    catch (const Error& error)
    {
        if (error.code() == ERROR_FILE_TOO_LARGE)
        {
            // Longer than what was written: other bytes, like any other difference.
            return Failure{.call = "AtomicFile::write",
                           .code = ERROR_CRC,
                           .context = "reading back " + utf8(file) + ": the bytes differ from what was written"};
        }
        return Failure{
            .call = std::string{error.call()}, .code = error.code(), .context = "reading back " + utf8(file)};
    }
    if (seams.read_back)
    {
        seams.read_back(step, actual);
    }
    if (!std::ranges::equal(actual, expected))
    {
        return Failure{.call = "AtomicFile::write",
                       .code = ERROR_CRC,
                       .context = "reading back " + utf8(file) + ": the bytes differ from what was written"};
    }
    return std::nullopt;
}

// Writes bytes to temporary, flushes them to the device, and reads them back. Throws Error.
void write_temporary(const std::filesystem::path& temporary, std::span<const std::byte> bytes,
                     const AtomicFileSeams& seams)
{
    if (const DWORD code = injected(seams, AtomicFileStep::WriteTemporary); code != 0)
    {
        throw Error{"WriteFile", code, "writing " + utf8(temporary)};
    }
    {
        const UniqueHandle handle = own(
            CreateFileW(temporary.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr));
        if (!handle)
        {
            throw Error{"CreateFileW", GetLastError(), "creating " + utf8(temporary)};
        }
        std::span<const std::byte> rest = bytes;
        while (!rest.empty())
        {
            const auto chunk = static_cast<DWORD>(std::min<std::size_t>(rest.size(), kChunkBytes));
            DWORD written = 0;
            if (WriteFile(handle.get(), rest.data(), chunk, &written, nullptr) == FALSE || written == 0)
            {
                throw Error{"WriteFile", GetLastError(), "writing " + utf8(temporary)};
            }
            rest = rest.subspan(written);
        }
        if (const DWORD code = injected(seams, AtomicFileStep::FlushTemporary); code != 0)
        {
            throw Error{"FlushFileBuffers", code, "flushing " + utf8(temporary)};
        }
        if (FlushFileBuffers(handle.get()) == FALSE)
        {
            throw Error{"FlushFileBuffers", GetLastError(), "flushing " + utf8(temporary)};
        }
    }
    if (const auto failure = read_back_failure(temporary, bytes, AtomicFileStep::ReadBackTemporary, seams))
    {
        throw Error{failure->call, failure->code, failure->context};
    }
}

// What a started replace expects the target to hold, and whether the write replaces a previous version or is the
// file's first: kept in <name>.txn from before the replace until the target has read back correct, so a later read
// can tell a verified target from a wrong one without knowing the format.
struct Journal
{
    std::uint64_t size = 0;
    std::uint64_t hash = 0;
    bool first = false;
};

constexpr std::string_view kJournalPrefix{"isotone-atomic-file 1 "};
constexpr std::string_view kJournalFirst{"first"};
constexpr std::string_view kJournalReplace{"replace"};
constexpr std::uint64_t kJournalMaxBytes = 128;

// FNV-1a, 64 bits: it catches a device that stored or returned other bytes, which is what the journal is for; it is
// not a defence against someone who can write the folder, who could replace the target and the journal alike.
std::uint64_t content_hash(std::span<const std::byte> bytes) noexcept
{
    constexpr std::uint64_t kOffset = 14695981039346656037ULL;
    constexpr std::uint64_t kPrime = 1099511628211ULL;
    std::uint64_t hash = kOffset;
    for (const std::byte value : bytes)
    {
        hash ^= std::to_integer<std::uint64_t>(value);
        hash *= kPrime;
    }
    return hash;
}

bool matches(const Journal& journal, std::span<const std::byte> bytes) noexcept
{
    return bytes.size() == journal.size && content_hash(bytes) == journal.hash;
}

// A whole number in the given base (10 or 16) with nothing else around it, or nothing.
std::optional<std::uint64_t> parse_number(std::string_view digits, std::uint64_t base) noexcept
{
    if (digits.empty())
    {
        return std::nullopt;
    }
    std::uint64_t value = 0;
    for (const char character : digits)
    {
        std::uint64_t digit = base;
        if (character >= '0' && character <= '9')
        {
            digit = static_cast<std::uint64_t>(character - '0');
        }
        else if (character >= 'a' && character <= 'f')
        {
            digit = static_cast<std::uint64_t>(character - 'a') + 10U;
        }
        if (digit >= base || value > (std::numeric_limits<std::uint64_t>::max() - digit) / base)
        {
            return std::nullopt;
        }
        value = (value * base) + digit;
    }
    return value;
}

// "isotone-atomic-file 1 <size> <hash in hex> <first|replace>\n", exactly; anything else is not a journal.
std::optional<Journal> parse_journal(std::string_view text)
{
    if (!text.starts_with(kJournalPrefix) || !text.ends_with('\n'))
    {
        return std::nullopt;
    }
    text.remove_prefix(kJournalPrefix.size());
    text.remove_suffix(1);
    const std::size_t first_space = text.find(' ');
    const std::size_t second_space =
        first_space == std::string_view::npos ? first_space : text.find(' ', first_space + 1);
    if (second_space == std::string_view::npos)
    {
        return std::nullopt;
    }
    const auto size = parse_number(text.substr(0, first_space), 10);
    const auto hash = parse_number(text.substr(first_space + 1, second_space - first_space - 1), 16);
    const std::string_view kind = text.substr(second_space + 1);
    if (!size || !hash || (kind != kJournalFirst && kind != kJournalReplace))
    {
        return std::nullopt;
    }
    return Journal{.size = *size, .hash = *hash, .first = kind == kJournalFirst};
}

// The journal a file's bytes hold, or nothing when they are not one.
std::optional<Journal> journal_from(std::span<const std::byte> bytes)
{
    if (bytes.size() > kJournalMaxBytes)
    {
        return std::nullopt;
    }
    std::string text(bytes.size(), '\0');
    std::ranges::transform(bytes, text.begin(), [](std::byte value) { return std::to_integer<char>(value); });
    return parse_journal(text);
}

// The journal beside the target, or nothing when there is none or it cannot be read as one.
std::optional<Journal> read_journal(const std::filesystem::path& journal_file)
{
    try
    {
        const auto bytes = read_whole(journal_file, kJournalMaxBytes, false);
        if (!bytes)
        {
            return std::nullopt;
        }
        return journal_from(*bytes);
    }
    catch (const Error&)
    {
        return std::nullopt;
    }
}

// Writes the journal for bytes and flushes it to the device. first says there is no previous version. Throws Error.
void write_journal(const std::filesystem::path& journal_file, std::span<const std::byte> bytes, bool first,
                   const AtomicFileSeams& seams)
{
    if (const DWORD code = injected(seams, AtomicFileStep::WriteJournal); code != 0)
    {
        throw Error{"WriteFile", code, "writing " + utf8(journal_file)};
    }
    const std::string text = std::format("{}{} {:016x} {}\n", kJournalPrefix, bytes.size(), content_hash(bytes),
                                         first ? kJournalFirst : kJournalReplace);
    const UniqueHandle handle = own(
        CreateFileW(journal_file.c_str(), GENERIC_WRITE, 0, nullptr, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr));
    if (!handle)
    {
        throw Error{"CreateFileW", GetLastError(), "creating " + utf8(journal_file)};
    }
    DWORD written = 0;
    if (WriteFile(handle.get(), text.data(), static_cast<DWORD>(text.size()), &written, nullptr) == FALSE ||
        written != text.size())
    {
        throw Error{"WriteFile", GetLastError(), "writing " + utf8(journal_file)};
    }
    if (FlushFileBuffers(handle.get()) == FALSE)
    {
        throw Error{"FlushFileBuffers", GetLastError(), "flushing " + utf8(journal_file)};
    }
}

// Puts the previous version back at the target's name (or removes the target when there was none). 0 on success.
DWORD restore_previous(const std::filesystem::path& target, const std::filesystem::path& backup, bool had_previous,
                       const AtomicFileSeams& seams) noexcept
{
    try
    {
        if (const DWORD code = injected(seams, AtomicFileStep::RestoreBackup); code != 0)
        {
            return code;
        }
    }
    catch (...)
    {
        return ERROR_INTERNAL_ERROR;
    }
    const BOOL done =
        had_previous ? MoveFileExW(backup.c_str(), target.c_str(), MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)
                     : DeleteFileW(target.c_str());
    return done == FALSE ? GetLastError() : ERROR_SUCCESS;
}

// The files of one AtomicFile.
struct Files
{
    std::filesystem::path target;
    std::filesystem::path temporary;
    std::filesystem::path backup;
    std::filesystem::path journal;
};

// The Error for a write that failed after the target had been replaced, having tried to restore the previous
// version. The journal goes once the previous version is back; it stays, with both copies, when it is not.
Error replaced_then_failed(const Failure& failure, const Files& files, bool had_previous, const AtomicFileSeams& seams)
{
    const DWORD restore_code = restore_previous(files.target, files.backup, had_previous, seams);
    if (restore_code == ERROR_SUCCESS)
    {
        remove_quietly(files.journal);
        return Error{failure.call, failure.code, failure.context};
    }
    if (had_previous)
    {
        return Error{failure.call, failure.code,
                     std::format("{}; restoring the previous version then failed with error {} (MoveFileExW), so both "
                                 "files were kept: the unverified {} and the previous version {}",
                                 failure.context, restore_code, utf8(files.target), utf8(files.backup))};
    }
    return Error{failure.call, failure.code,
                 std::format("{}; removing the unverified {} then failed with error {} (DeleteFileW), and there was "
                             "no previous version",
                             failure.context, utf8(files.target), restore_code)};
}

void* take_lock(const std::filesystem::path& lock_file, std::chrono::milliseconds wait)
{
    const auto start = std::chrono::steady_clock::now();
    for (;;)
    {
        // No sharing: a second opener waits. Delete on close: a holder that dies never leaves the lock held.
        const HANDLE handle = CreateFileW(lock_file.c_str(), GENERIC_READ | GENERIC_WRITE | DELETE, 0, nullptr,
                                          OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL | FILE_FLAG_DELETE_ON_CLOSE, nullptr);
        if (handle != INVALID_HANDLE_VALUE)
        {
            return handle;
        }
        const DWORD code = GetLastError();
        const auto waited = std::chrono::steady_clock::now() - start;
        const bool busy = (code == ERROR_SHARING_VIOLATION && waited < wait) ||
                          (code == ERROR_ACCESS_DENIED && waited < std::min(wait, kDeniedWait));
        if (!busy)
        {
            throw Error{"CreateFileW", code, "taking the lock " + utf8(lock_file)};
        }
        std::this_thread::sleep_for(kRetryPause);
    }
}

bool passes(const std::optional<std::vector<std::byte>>& bytes, const AtomicFileCheck& check)
{
    return bytes.has_value() && (!check || check(*bytes));
}

std::filesystem::path with_suffix(std::filesystem::path file, std::wstring_view suffix)
{
    file += suffix;
    return file;
}

// The target as read for settling: its bytes, or the Error when it is over the limit (which fails any test of it).
struct TargetRead
{
    std::optional<std::vector<std::byte>> bytes;
    std::optional<Error> too_large;
};

TargetRead read_target(const std::filesystem::path& target, std::uint64_t limit)
{
    TargetRead read;
    try
    {
        read.bytes = read_whole(target, limit, false);
    }
    catch (const Error& error)
    {
        if (error.code() != ERROR_FILE_TOO_LARGE)
        {
            throw;
        }
        read.too_large = error;
    }
    return read;
}

// What settling found: the file's bytes (nothing when there is no file), or the Error to give a reader when the
// only copy is over the limit.
struct Settled
{
    std::optional<std::vector<std::byte>> bytes;
    std::optional<Error> refused;
};

// The backup goes, and the journal only once the backup is gone: a backup that cannot be deleted yet keeps the
// journal that says the target, not it, is the good copy.
void remove_settled(const Files& files) noexcept
{
    remove_quietly(files.backup);
    if (!exists_quietly(files.backup))
    {
        remove_quietly(files.journal);
    }
}

// A journal with no backup beside it: the replace it describes did not happen, or was the file's first write.
Settled settle_without_backup(const Files& files, const Journal& expected, TargetRead current,
                              const AtomicFileSeams& seams, bool modify)
{
    const bool target_here = current.bytes.has_value() || current.too_large.has_value();
    if (expected.first && target_here)
    {
        // There was no previous version, and what is at the target is not what was written: it is no version of
        // the file at all. It is removed, as the write itself would have done, and never returned.
        if (modify)
        {
            if (const DWORD code = restore_previous(files.target, files.backup, false, seams); code != 0)
            {
                throw Error{"DeleteFileW", code,
                            "removing " + utf8(files.target) +
                                ", which does not hold the bytes its first write recorded and has no previous version"};
            }
            remove_quietly(files.journal);
        }
        return Settled{.bytes = std::nullopt, .refused = std::nullopt};
    }
    // The write stopped before its replace: the target is still the previous version (or there is still no file).
    if (modify)
    {
        remove_quietly(files.journal);
    }
    return Settled{.bytes = std::move(current.bytes), .refused = std::move(current.too_large)};
}

// Decides which copy holds the file after a write that was interrupted or could not restore, and, when modify,
// puts it at the target's name and removes what is settled. With a journal the target is good exactly when it
// holds the bytes the journal names, and otherwise the backup is the last good version. With a backup and no
// journal (one that was lost, or written by other code) the target is good when it passes check, which every
// target does when check is empty. Throws Error when a copy cannot be read or the restore fails.
Settled settle(const Files& files, std::uint64_t limit, const AtomicFileCheck& check, const AtomicFileSeams& seams,
               bool modify)
{
    const bool journal_here = file_exists(files.journal);
    const auto expected = journal_here ? read_journal(files.journal) : std::nullopt;
    const bool has_backup = file_exists(files.backup);
    TargetRead current = read_target(files.target, limit);
    if (journal_here && !expected && modify)
    {
        // Not a journal: it decides nothing.
        remove_quietly(files.journal);
    }
    if (!expected && !has_backup)
    {
        return Settled{.bytes = std::move(current.bytes), .refused = std::move(current.too_large)};
    }

    const bool target_good = expected ? current.bytes.has_value() && matches(*expected, *current.bytes)
                                      : !current.too_large && passes(current.bytes, check);
    if (target_good)
    {
        if (modify)
        {
            remove_settled(files);
        }
        return Settled{.bytes = std::move(current.bytes), .refused = std::nullopt};
    }
    if (expected && !has_backup)
    {
        return settle_without_backup(files, *expected, std::move(current), seams, modify);
    }
    auto previous = read_whole(files.backup, limit, false);
    if (expected ? previous.has_value() : passes(previous, check))
    {
        if (modify)
        {
            if (const DWORD code = restore_previous(files.target, files.backup, true, seams); code != 0)
            {
                throw Error{"MoveFileExW", code, "restoring " + utf8(files.target) + " from " + utf8(files.backup)};
            }
            remove_quietly(files.journal);
        }
        return Settled{.bytes = std::move(previous), .refused = std::nullopt};
    }
    // Neither copy passes the check: the caller judges the target, and the backup stays.
    return Settled{.bytes = std::move(current.bytes), .refused = std::move(current.too_large)};
}

std::optional<std::vector<std::byte>> take(Settled settled)
{
    if (settled.refused)
    {
        throw Error{*settled.refused};
    }
    return std::move(settled.bytes);
}

// What an earlier write left is settled before a write starts: by its journal, or, for a backup with no journal, by
// the rule that the target is the good copy. A backup that then still cannot be deleted is one the target has
// replaced; while it is there no write may start, because a later failure could put it back over a newer version.
void settle_before_write(const Files& files, const AtomicFileSeams& seams)
{
    if (!file_exists(files.journal) && !file_exists(files.backup))
    {
        return;
    }
    static_cast<void>(settle(files, std::numeric_limits<std::uint64_t>::max(), {}, seams, true));
    if (DeleteFileW(files.backup.c_str()) == FALSE)
    {
        const DWORD code = GetLastError();
        if (code != ERROR_FILE_NOT_FOUND && code != ERROR_PATH_NOT_FOUND)
        {
            throw Error{"DeleteFileW", code,
                        "removing " + utf8(files.backup) + ", the backup of an earlier write that " +
                            utf8(files.target) + " has replaced; nothing was written"};
        }
    }
    remove_quietly(files.journal);
}

// Replaces the target with the verified temporary file. Throws Error with the target as it was; when the target was
// already renamed away, the previous version is put back first.
void replace_target(const Files& files, bool had_previous, const AtomicFileSeams& seams)
{
    if (!had_previous)
    {
        if (MoveFileExW(files.temporary.c_str(), files.target.c_str(), MOVEFILE_WRITE_THROUGH) == FALSE)
        {
            throw Error{"MoveFileExW", GetLastError(), "creating " + utf8(files.target)};
        }
        return;
    }
    if (ReplaceFileW(files.target.c_str(), files.temporary.c_str(), files.backup.c_str(),
                     REPLACEFILE_IGNORE_MERGE_ERRORS | REPLACEFILE_IGNORE_ACL_ERRORS, nullptr, nullptr) != FALSE)
    {
        return;
    }
    const DWORD code = GetLastError();
    const Failure failure{.call = "ReplaceFileW", .code = code, .context = "replacing " + utf8(files.target)};
    if (code == ERROR_UNABLE_TO_MOVE_REPLACEMENT_2)
    {
        // The target was already renamed to the backup's name: put it back.
        throw replaced_then_failed(failure, files, true, seams);
    }
    throw Error{failure.call, failure.code, failure.context};
}

} // namespace

bool is_atomic_file_journal(std::span<const std::byte> bytes)
{
    return journal_from(bytes).has_value();
}

AtomicFile::Session::Session(const AtomicFile& file, void* lock_handle) noexcept : file_{&file}, lock_{lock_handle}
{
}

AtomicFile::Session::Session(Session&& other) noexcept : file_{other.file_}, lock_{std::exchange(other.lock_, nullptr)}
{
}

AtomicFile::Session::~Session()
{
    if (lock_ != nullptr)
    {
        CloseHandle(lock_);
    }
}

std::optional<std::vector<std::byte>> AtomicFile::Session::read(const AtomicFileCheck& check) const
{
    const Files files{.target = file_->target_,
                      .temporary = file_->temporary_path(),
                      .backup = file_->backup_path(),
                      .journal = file_->journal_path()};
    return take(settle(files, file_->options_.max_read_bytes, check, file_->options_.seams, true));
}

void AtomicFile::Session::write(std::span<const std::byte> bytes) const
{
    const auto& seams = file_->options_.seams;
    const Files files{.target = file_->target_,
                      .temporary = file_->temporary_path(),
                      .backup = file_->backup_path(),
                      .journal = file_->journal_path()};

    bool had_previous = false;
    bool journal_written = false;
    try
    {
        write_temporary(files.temporary, bytes, seams);
        settle_before_write(files, seams);
        had_previous = file_exists(files.target);
        journal_written = true;
        write_journal(files.journal, bytes, !had_previous, seams);
        if (const DWORD code = injected(seams, AtomicFileStep::Replace); code != 0)
        {
            throw Error{"ReplaceFileW", code, "replacing " + utf8(files.target)};
        }
        replace_target(files, had_previous, seams);
    }
    catch (...)
    {
        // The temporary file goes. So does this write's journal when the replace did not happen (no backup was
        // made); a journal an earlier write left, with the copies it describes, stays for the next settling.
        remove_quietly(files.temporary);
        if (journal_written && !exists_quietly(files.backup))
        {
            remove_quietly(files.journal);
        }
        throw;
    }

    if (seams.after_replace)
    {
        seams.after_replace();
    }
    if (const auto failure = read_back_failure(files.target, bytes, AtomicFileStep::ReadBackTarget, seams))
    {
        throw replaced_then_failed(*failure, files, had_previous, seams);
    }
    // The new version is in place and verified.
    if (!had_previous || injected(seams, AtomicFileStep::DeleteBackup) == 0)
    {
        remove_settled(files);
    }
}

bool AtomicFile::Session::move_aside(const std::filesystem::path& destination) const
{
    const auto& target = file_->target_;
    if (MoveFileExW(target.c_str(), destination.c_str(), 0) != FALSE)
    {
        return true;
    }
    const DWORD code = GetLastError();
    if (code == ERROR_FILE_NOT_FOUND || code == ERROR_PATH_NOT_FOUND)
    {
        return false;
    }
    throw Error{"MoveFileExW", code, "moving " + utf8(target) + " aside to " + utf8(destination)};
}

AtomicFile::AtomicFile(std::filesystem::path target, AtomicFileOptions options)
    : target_{std::move(target)}, options_{std::move(options)}
{
}

const std::filesystem::path& AtomicFile::target() const noexcept
{
    return target_;
}

std::filesystem::path AtomicFile::temporary_path() const
{
    return with_suffix(target_, L".tmp");
}

std::filesystem::path AtomicFile::backup_path() const
{
    return with_suffix(target_, L".bak");
}

std::filesystem::path AtomicFile::journal_path() const
{
    return with_suffix(target_, L".txn");
}

std::filesystem::path AtomicFile::lock_path() const
{
    return with_suffix(target_, L".lock");
}

AtomicFile::Session AtomicFile::lock() const
{
    try
    {
        return Session{*this, take_lock(lock_path(), options_.lock_wait)};
    }
    catch (const Error& error)
    {
        if (error.code() != ERROR_PATH_NOT_FOUND)
        {
            throw;
        }
    }
    // The folder is gone (removed while the app ran, or never created): make it and take the lock once more.
    std::error_code failure;
    std::filesystem::create_directories(target_.parent_path(), failure);
    if (failure)
    {
        throw Error{"std::filesystem::create_directories", static_cast<std::uint32_t>(failure.value()),
                    "creating " + utf8(target_.parent_path())};
    }
    return Session{*this, take_lock(lock_path(), options_.lock_wait)};
}

std::optional<std::vector<std::byte>> AtomicFile::read(const AtomicFileCheck& check) const
{
    const Files files{
        .target = target_, .temporary = temporary_path(), .backup = backup_path(), .journal = journal_path()};
    const auto unsettled = [&files] { return file_exists(files.backup) || file_exists(files.journal); };
    const auto reached = [this](AtomicFileReadPoint point) {
        if (options_.seams.reading)
        {
            options_.seams.reading(point);
        }
    };
    // With nothing unsettled the file is read without the lock. What was read counts only if no write was in
    // flight while it was read: still nothing unsettled afterwards, and the name still holds the very file that
    // was read. A write that replaced the target, failed its readback, and put the previous version back leaves no
    // backup and no journal behind, but it leaves another file at the name, and its unverified bytes must never be
    // returned; a write that succeeded in between leaves its new file there, and the next try reads that.
    for (int attempt = 0; attempt < kUnlockedReadTries && !unsettled(); ++attempt)
    {
        reached(AtomicFileReadPoint::BeforeRead);
        std::optional<FileIdentity> read_from;
        auto bytes = read_whole(target_, options_.max_read_bytes, false, &read_from);
        reached(AtomicFileReadPoint::AfterRead);
        if (!unsettled() && identity_at(target_) == read_from)
        {
            return bytes;
        }
    }
    // A writer is at work, or keeps being: the locked read waits for it and settles what it left.
    try
    {
        return lock().read(check);
    }
    catch (const Error& error)
    {
        if (error.code() != ERROR_ACCESS_DENIED && error.code() != ERROR_WRITE_PROTECT)
        {
            throw;
        }
    }
    // The folder cannot be written, so nothing is settled: return the copy settling would choose and change nothing.
    return take(settle(files, options_.max_read_bytes, check, options_.seams, false));
}

void AtomicFile::write(std::span<const std::byte> bytes) const
{
    lock().write(bytes);
}

} // namespace isotone::core
