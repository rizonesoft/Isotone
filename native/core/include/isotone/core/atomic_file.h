// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include <chrono>
#include <cstddef>
#include <cstdint>
#include <filesystem>
#include <functional>
#include <memory>
#include <optional>
#include <span>
#include <vector>

namespace isotone::core
{

// The steps of a write a test can make fail (AtomicFileSeams).
enum class AtomicFileStep : std::uint8_t
{
    WriteTemporary,
    FlushTemporary,
    ReadBackTemporary,
    Replace,
    ReadBackTarget,
    RestoreBackup,
    DeleteBackup,
};

// Test seams: production code leaves both empty.
struct AtomicFileSeams
{
    // Called before each step; a nonzero Win32 error makes that step fail with it instead of running.
    std::function<std::uint32_t(AtomicFileStep step)> fail;
    // Called with the bytes a readback step read; changing them makes the comparison fail.
    std::function<void(AtomicFileStep step, std::vector<std::byte>& bytes)> read_back;
};

struct AtomicFileOptions
{
    // A file larger than this is refused by read (ERROR_FILE_TOO_LARGE) before anything is allocated for it.
    std::uint64_t max_read_bytes = 64ULL * 1024ULL * 1024ULL;
    // How long a write or a settling read waits for another writer's lock before it reports.
    std::chrono::milliseconds lock_wait{2000};
    AtomicFileSeams seams;
};

// Says whether bytes are a complete file of the caller's kind. Used only to choose between a target and the backup
// a crash left beside it.
using AtomicFileCheck = std::function<bool(std::span<const std::byte> bytes)>;

// One app data file that is only ever replaced whole (settings and other app data; never a user's document, whose
// save sequence is its own: D01 T19 §1). A write goes to <name>.tmp beside the target, is flushed, read back from
// the device and compared, and only then takes the target's name, with the previous version kept as <name>.bak
// until the target has read back correct. Writers in any process take turns through <name>.lock, which is deleted
// when its holder closes it or dies. Killing the process at any instant leaves a complete old or new file, which
// the next read settles. Every member function may be called from any thread; every failure is an Error naming the
// failing call.
class AtomicFile
{
  public:
    // The lock on one file, held from AtomicFile::lock() until this object is destroyed. It must not outlive the
    // AtomicFile it came from, and it is used from one thread at a time.
    class Session
    {
      public:
        ~Session();
        Session(const Session&) = delete;
        Session& operator=(const Session&) = delete;
        Session(Session&& other) noexcept;
        Session& operator=(Session&&) = delete;

        // The whole file, or nothing when there is none. A backup left by a crash is settled first: the target is
        // kept when it exists and passes check (always, when check is empty), otherwise the backup is restored to
        // the target's name; when neither passes, the target is returned and the backup left for the next write.
        [[nodiscard]] std::optional<std::vector<std::byte>> read(const AtomicFileCheck& check = {}) const;

        // Replaces the file with bytes as the class comment describes. On a failure the previous version is still
        // at the target's name (or there is still no file, when there was none). When restoring it fails too, both
        // copies stay where they are and the Error names both failures and both paths. A backup already beside the
        // target when a write starts (left by that, or by a crash) is never overwritten: it stays what a failed
        // write goes back to, and is deleted only once new bytes have read back correct. The next read restores a
        // backup if the target is missing or fails that read's check: a caller whose data matters passes one.
        void write(std::span<const std::byte> bytes) const;

        // Renames the target to destination, which must not exist, in the same folder; false when there is no
        // target. For a caller keeping an unreadable file aside rather than overwriting it.
        [[nodiscard]] bool move_aside(const std::filesystem::path& destination) const;

      private:
        friend class AtomicFile;
        Session(const AtomicFile& file, void* lock_handle) noexcept;

        const AtomicFile* file_;
        void* lock_;
    };

    explicit AtomicFile(std::filesystem::path target, AtomicFileOptions options = {});

    [[nodiscard]] const std::filesystem::path& target() const noexcept;
    // <target>.tmp, <target>.bak, and <target>.lock.
    [[nodiscard]] std::filesystem::path temporary_path() const;
    [[nodiscard]] std::filesystem::path backup_path() const;
    [[nodiscard]] std::filesystem::path lock_path() const;

    // Takes the lock, waiting up to AtomicFileOptions::lock_wait for another holder. Creates the target's folder when
    // it does not exist.
    [[nodiscard]] Session lock() const;

    // The whole file, or nothing when there is none. With no backup beside the target this takes no lock and writes
    // nothing, so it works in a folder that cannot be written. With one, it takes the lock and settles it as
    // Session::read does; in a folder where no lock can be created it changes nothing and returns the target when
    // that passes check, otherwise the backup.
    [[nodiscard]] std::optional<std::vector<std::byte>> read(const AtomicFileCheck& check = {}) const;

    // lock() then Session::write.
    void write(std::span<const std::byte> bytes) const;

  private:
    std::filesystem::path target_;
    AtomicFileOptions options_;
};

} // namespace isotone::core
