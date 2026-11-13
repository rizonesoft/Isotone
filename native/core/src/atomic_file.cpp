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
#include <memory>
#include <optional>
#include <span>
#include <string>
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

// One attempt at reading the whole file, or nothing when it does not exist. unbuffered reads the device rather than
// the file cache; when the file system refuses that, refused is set and nothing is returned. Throws Error; a file
// over max_bytes is ERROR_FILE_TOO_LARGE, decided before anything is allocated for it.
std::optional<std::vector<std::byte>> read_once(const std::filesystem::path& file, std::uint64_t max_bytes,
                                                bool unbuffered, bool& refused)
{
    refused = false;
    const DWORD flags = FILE_ATTRIBUTE_NORMAL | FILE_FLAG_SEQUENTIAL_SCAN | (unbuffered ? FILE_FLAG_NO_BUFFERING : 0U);
    DWORD code = ERROR_SUCCESS;
    const UniqueHandle handle = open_for_reading(file, flags, code);
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
                                                 bool unbuffered)
{
    bool refused = false;
    if (unbuffered)
    {
        auto bytes = read_once(file, max_bytes, true, refused);
        if (!refused)
        {
            return bytes;
        }
    }
    return read_once(file, max_bytes, false, refused);
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

// The Error for a write that failed after the target had been replaced, having tried to restore the previous version.
Error replaced_then_failed(const Failure& failure, const std::filesystem::path& target,
                           const std::filesystem::path& backup, bool had_previous, const AtomicFileSeams& seams)
{
    const DWORD restore_code = restore_previous(target, backup, had_previous, seams);
    if (restore_code == ERROR_SUCCESS)
    {
        return Error{failure.call, failure.code, failure.context};
    }
    if (had_previous)
    {
        return Error{failure.call, failure.code,
                     std::format("{}; restoring the previous version then failed with error {} (MoveFileExW), so both "
                                 "files were kept: the unverified {} and the previous version {}",
                                 failure.context, restore_code, utf8(target), utf8(backup))};
    }
    return Error{failure.call, failure.code,
                 std::format("{}; removing the unverified {} then failed with error {} (DeleteFileW), and there was "
                             "no previous version",
                             failure.context, utf8(target), restore_code)};
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

} // namespace

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
    const auto& target = file_->target_;
    const auto backup = file_->backup_path();
    const std::uint64_t limit = file_->options_.max_read_bytes;
    if (!file_exists(backup))
    {
        return read_whole(target, limit, false);
    }

    // A backup is here: a write was interrupted after it replaced the target, or could not restore it.
    std::optional<std::vector<std::byte>> current;
    std::optional<Error> too_large;
    try
    {
        current = read_whole(target, limit, false);
    }
    catch (const Error& error)
    {
        // A target over the limit fails any check; without a check there is nothing to choose by.
        if (error.code() != ERROR_FILE_TOO_LARGE || !check)
        {
            throw;
        }
        too_large = error;
    }
    if (!too_large && passes(current, check))
    {
        remove_quietly(backup);
        return current;
    }
    auto previous = read_whole(backup, limit, false);
    if (passes(previous, check))
    {
        if (MoveFileExW(backup.c_str(), target.c_str(), MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH) == FALSE)
        {
            throw Error{"MoveFileExW", GetLastError(), "restoring " + utf8(target) + " from " + utf8(backup)};
        }
        return previous;
    }
    // Neither copy passes: the caller judges the target, and the backup waits for the next write.
    if (too_large)
    {
        throw Error{*too_large};
    }
    return current;
}

void AtomicFile::Session::write(std::span<const std::byte> bytes) const
{
    const auto& target = file_->target_;
    const auto& seams = file_->options_.seams;
    const auto temporary = file_->temporary_path();
    const auto backup = file_->backup_path();

    bool had_previous = false;
    // A backup already here was left by a write that was interrupted or could not restore: it may be the last good
    // version, so this write keeps it as what a failure goes back to and never replaces it with the target.
    bool kept_backup = false;
    try
    {
        write_temporary(temporary, bytes, seams);
        had_previous = file_exists(target);
        kept_backup = file_exists(backup);
        if (const DWORD code = injected(seams, AtomicFileStep::Replace); code != 0)
        {
            throw Error{"ReplaceFileW", code, "replacing " + utf8(target)};
        }
    }
    catch (...)
    {
        remove_quietly(temporary);
        throw;
    }

    if (had_previous)
    {
        if (ReplaceFileW(target.c_str(), temporary.c_str(), kept_backup ? nullptr : backup.c_str(),
                         REPLACEFILE_IGNORE_MERGE_ERRORS | REPLACEFILE_IGNORE_ACL_ERRORS, nullptr, nullptr) == FALSE)
        {
            const DWORD code = GetLastError();
            const Failure failure{.call = "ReplaceFileW", .code = code, .context = "replacing " + utf8(target)};
            remove_quietly(temporary);
            if (code == ERROR_UNABLE_TO_MOVE_REPLACEMENT_2 && !kept_backup)
            {
                // The target was already renamed to the backup's name: put it back.
                throw replaced_then_failed(failure, target, backup, true, seams);
            }
            throw Error{failure.call, failure.code, failure.context};
        }
    }
    else if (MoveFileExW(temporary.c_str(), target.c_str(), MOVEFILE_WRITE_THROUGH) == FALSE)
    {
        const DWORD code = GetLastError();
        remove_quietly(temporary);
        throw Error{"MoveFileExW", code, "creating " + utf8(target)};
    }

    if (const auto failure = read_back_failure(target, bytes, AtomicFileStep::ReadBackTarget, seams))
    {
        throw replaced_then_failed(*failure, target, backup, had_previous || kept_backup, seams);
    }
    if ((had_previous || kept_backup) && injected(seams, AtomicFileStep::DeleteBackup) == 0)
    {
        // The new version is in place and verified; a backup that stays is removed by the next read.
        remove_quietly(backup);
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
    const auto backup = backup_path();
    if (!file_exists(backup))
    {
        auto bytes = read_whole(target_, options_.max_read_bytes, false);
        // A replace renames the target away for an instant: nothing at the target with a backup now present means
        // a writer is at work, and the locked read below waits for it.
        if (bytes || !file_exists(backup))
        {
            return bytes;
        }
    }
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
    // The folder cannot be written, so nothing is settled: return the better copy and change nothing.
    auto current = read_whole(target_, options_.max_read_bytes, false);
    if (passes(current, check))
    {
        return current;
    }
    auto previous = read_whole(backup, options_.max_read_bytes, false);
    return passes(previous, check) ? previous : current;
}

void AtomicFile::write(std::span<const std::byte> bytes) const
{
    lock().write(bytes);
}

} // namespace isotone::core
