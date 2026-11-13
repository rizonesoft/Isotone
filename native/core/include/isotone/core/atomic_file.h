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
    WriteJournal,
    Replace,
    ReadBackTarget,
    RestoreBackup,
    DeleteBackup,
};

// The two points of a read without the lock a test can act at (AtomicFileSeams::reading).
enum class AtomicFileReadPoint : std::uint8_t
{
    BeforeRead,
    AfterRead,
};

// Test seams: production code leaves them empty.
struct AtomicFileSeams
{
    // Called before each step; a nonzero Win32 error makes that step fail with it instead of running.
    std::function<std::uint32_t(AtomicFileStep step)> fail;
    // Called with the bytes a readback step read; changing them makes the comparison fail.
    std::function<void(AtomicFileStep step, std::vector<std::byte>& bytes)> read_back;
    // Called once the target has taken the new bytes and before it is read back: a test stores other bytes there,
    // as a failing device would.
    std::function<void()> after_replace;
    // Called before and after a read without the lock reads the target: a test lets a write cross the read there.
    std::function<void(AtomicFileReadPoint point)> reading;
};

struct AtomicFileOptions
{
    // A file larger than this is refused by read (ERROR_FILE_TOO_LARGE) before anything is allocated for it.
    std::uint64_t max_read_bytes = 64ULL * 1024ULL * 1024ULL;
    // How long a write or a settling read waits for another writer's lock before it reports.
    std::chrono::milliseconds lock_wait{2000};
    AtomicFileSeams seams;
};

// Says whether bytes are a complete file of the caller's kind. Used only to choose between a target and a backup
// that has no journal beside it.
using AtomicFileCheck = std::function<bool(std::span<const std::byte> bytes)>;

// Whether bytes are a journal as AtomicFile writes one ("isotone-atomic-file 1 <size> <checksum in hex> <first or
// replace>" and a line break, at most 128 bytes), read exactly as a settling read reads <name>.txn. For the fuzz
// target and tests.
// Throws std::bad_alloc only. Any thread.
[[nodiscard]] bool is_atomic_file_journal(std::span<const std::byte> bytes);

// One app data file that is only ever replaced whole (settings and other app data; never a user's document, whose
// save sequence is its own: D01 T19 §1). A write goes to <name>.tmp beside the target, is flushed, read back from
// the device and compared; a journal, <name>.txn, then records the size and checksum the target must hold; only
// then do the bytes take the target's name, with the previous version kept as <name>.bak; and the backup and the
// journal go once the target has read back correct. Writers in any process take turns through <name>.lock, which
// is deleted when its holder closes it or dies. Killing the process at any instant, or a write that fails and
// cannot put the previous version back, leaves a complete old or new file and a journal that says which: the next
// read or write keeps the target when it holds the journal's bytes and otherwise restores the backup (or, after a
// first write, removes a target that is not what was written), with no knowledge of the file's format. A backup the
// target has replaced but that cannot be deleted yet keeps its journal, and no write starts while it is there, so
// no failure can ever put an older version back over a newer one. Every member function may be called from any thread;
// every failure is an Error naming the failing call.
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

        // The whole file, or nothing when there is none. What an interrupted or failed write left is settled first,
        // by its journal as the class comment says. A backup with no journal (one that was lost, or other code's)
        // is settled by check: the target is kept when it exists and passes check (always, when check is empty),
        // otherwise the backup is restored; when neither passes, the target is returned and the backup left.
        [[nodiscard]] std::optional<std::vector<std::byte>> read(const AtomicFileCheck& check = {}) const;

        // Replaces the file with bytes as the class comment describes, first settling what an earlier write left.
        // On a failure the previous version is still at the target's name (or there is still no file, when there
        // was none). When restoring it fails too, both copies and the journal stay where they are and the Error
        // names both failures and both paths. A backup with no journal is never overwritten: it stays what a
        // failed write goes back to, and is deleted only once new bytes have read back correct.
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
    // <target>.tmp, <target>.bak, <target>.txn, and <target>.lock.
    [[nodiscard]] std::filesystem::path temporary_path() const;
    [[nodiscard]] std::filesystem::path backup_path() const;
    [[nodiscard]] std::filesystem::path journal_path() const;
    [[nodiscard]] std::filesystem::path lock_path() const;

    // Takes the lock, waiting up to AtomicFileOptions::lock_wait for another holder. Creates the target's folder when
    // it does not exist.
    [[nodiscard]] Session lock() const;

    // The whole file, or nothing when there is none. With no backup and no journal beside the target this takes no
    // lock and writes nothing, so it works in a folder that cannot be written; it returns only bytes no write
    // crossed (it reads again, and takes the lock, when one did), so never a version a write then rolled back. With
    // either, it takes the lock and settles as Session::read does; in a folder where no lock can be created it changes
    // nothing and returns the copy settling would choose.
    [[nodiscard]] std::optional<std::vector<std::byte>> read(const AtomicFileCheck& check = {}) const;

    // lock() then Session::write.
    void write(std::span<const std::byte> bytes) const;

  private:
    std::filesystem::path target_;
    AtomicFileOptions options_;
};

} // namespace isotone::core
