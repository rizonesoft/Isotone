// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/atomic_file.h"
#include "isotone/core/error.h"
#include "temp_folder.h"

#include <chrono>
#include <cstddef>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <gtest/gtest.h>
#include <iterator>
#include <memory>
#include <optional>
#include <set>
#include <span>
#include <string>
#include <string_view>
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

using isotone::core::AtomicFile;
using isotone::core::AtomicFileOptions;
using isotone::core::AtomicFileStep;
using isotone::core::Error;
using isotone::tests::TempFolder;

std::vector<std::byte> bytes_of(std::string_view text)
{
    const auto view = std::as_bytes(std::span{text});
    return {view.begin(), view.end()};
}

std::string text_of(const std::optional<std::vector<std::byte>>& bytes)
{
    if (!bytes)
    {
        return "<no file>";
    }
    std::string text;
    for (const std::byte value : *bytes)
    {
        text.push_back(static_cast<char>(value));
    }
    return text;
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

struct HandleCloser
{
    void operator()(HANDLE handle) const noexcept
    {
        CloseHandle(handle);
    }
};

// Opens a file with no sharing, as another program holding it would.
std::unique_ptr<void, HandleCloser> hold_exclusively(const std::filesystem::path& file)
{
    const HANDLE handle = CreateFileW(file.c_str(), GENERIC_READ | GENERIC_WRITE, 0, nullptr, OPEN_ALWAYS,
                                      FILE_ATTRIBUTE_NORMAL, nullptr);
    return std::unique_ptr<void, HandleCloser>{handle == INVALID_HANDLE_VALUE ? nullptr : handle};
}

// A read_back seam that changes the first byte a given step read back, while armed is null or true.
auto corrupt_read_back(AtomicFileStep wanted, const bool* armed = nullptr)
{
    return [wanted, armed](AtomicFileStep step, std::vector<std::byte>& bytes) {
        if (step == wanted && (armed == nullptr || *armed) && !bytes.empty())
        {
            bytes.front() = std::byte{0};
        }
    };
}

// A fail seam that fails one step with a code, while armed is null or true.
auto fail_step(AtomicFileStep wanted, std::uint32_t code, const bool* armed = nullptr)
{
    return [wanted, code, armed](AtomicFileStep step) {
        return step == wanted && (armed == nullptr || *armed) ? code : 0U;
    };
}

bool starts_good(std::span<const std::byte> bytes)
{
    return !bytes.empty() && bytes.front() == std::byte{'g'};
}

TEST(AtomicFile, ReplacesAndReadsBack)
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};

    file.write(bytes_of("one"));
    EXPECT_EQ(slurp(file.target()), "one");
    file.write(bytes_of("the second version"));
    EXPECT_EQ(slurp(file.target()), "the second version");
    EXPECT_EQ(text_of(file.read()), "the second version");
    file.write({});
    EXPECT_EQ(text_of(file.read()), "");

    // A file larger than one chunk goes through whole.
    std::string large((3U * 1024U * 1024U) + 17U, 'x');
    large.back() = 'y';
    file.write(bytes_of(large));
    EXPECT_EQ(text_of(file.read()), large);

    // Nothing but the file is left: no temporary file, no backup, no lock.
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

TEST(AtomicFile, FirstWriteCreatesTheFile)
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "new.json"};

    EXPECT_FALSE(file.read().has_value());
    file.write(bytes_of("first"));
    EXPECT_EQ(text_of(file.read()), "first");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"new.json"});

    // A folder that is not there yet (or was removed while the app ran) is created by the write.
    const AtomicFile nested{temp.path() / "made" / "on demand" / "new.json"};
    EXPECT_FALSE(nested.read().has_value());
    nested.write(bytes_of("first"));
    EXPECT_EQ(text_of(nested.read()), "first");
}

// One step of a write made to fail before the target is replaced.
struct FailingStep
{
    AtomicFileStep step;
    std::uint32_t code;
    std::string_view call;
};

void expect_failed_step_keeps_previous(const FailingStep& failing)
{
    const TempFolder temp;
    AtomicFileOptions options;
    options.seams.fail = fail_step(failing.step, failing.code);
    const AtomicFile file{temp.path() / "data.json", options};
    put(file.target(), "previous");

    const Error error = error_of([&file] { file.write(bytes_of("replacement")); });
    EXPECT_EQ(error.code(), failing.code) << failing.call;
    EXPECT_EQ(error.call(), failing.call);
    EXPECT_EQ(slurp(file.target()), "previous") << failing.call;
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"}) << failing.call;
}

TEST(AtomicFile, FailureBeforeReplaceLeavesPrevious)
{
    expect_failed_step_keeps_previous(
        {.step = AtomicFileStep::WriteTemporary, .code = ERROR_DISK_FULL, .call = "WriteFile"});
    expect_failed_step_keeps_previous(
        {.step = AtomicFileStep::FlushTemporary, .code = ERROR_WRITE_FAULT, .call = "FlushFileBuffers"});
    expect_failed_step_keeps_previous(
        {.step = AtomicFileStep::ReadBackTemporary, .code = ERROR_READ_FAULT, .call = "ReadFile"});
    expect_failed_step_keeps_previous(
        {.step = AtomicFileStep::Replace, .code = ERROR_ACCESS_DENIED, .call = "ReplaceFileW"});

    // The temporary file reading back different bytes is caught before the target is touched.
    const TempFolder temp;
    AtomicFileOptions options;
    options.seams.read_back = corrupt_read_back(AtomicFileStep::ReadBackTemporary);
    const AtomicFile file{temp.path() / "data.json", options};
    put(file.target(), "previous");
    const Error error = error_of([&file] { file.write(bytes_of("replacement")); });
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_CRC));
    EXPECT_EQ(slurp(file.target()), "previous");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

TEST(AtomicFile, ReadbackFailureAfterReplaceRestoresPrevious)
{
    const TempFolder temp;
    AtomicFileOptions options;
    options.seams.read_back = corrupt_read_back(AtomicFileStep::ReadBackTarget);
    const AtomicFile file{temp.path() / "data.json", options};
    put(file.target(), "previous");

    const Error error = error_of([&file] { file.write(bytes_of("replacement")); });
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_CRC));
    EXPECT_EQ(slurp(file.target()), "previous");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});

    // With no previous version, the unverified file is removed rather than left.
    const AtomicFile fresh{temp.path() / "fresh.json", options};
    EXPECT_TRUE(throws_error([&fresh] { fresh.write(bytes_of("replacement")); }));
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

// Killed after the replace, before the backup was deleted: the target was verified before it took the name.
void expect_verified_target_wins()
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.target(), "new");
    put(file.backup_path(), "old");
    EXPECT_EQ(text_of(file.read()), "new");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

// Killed inside the replace: the target is gone and the backup holds the last version.
void expect_backup_restored_when_target_is_missing()
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.backup_path(), "old");
    EXPECT_EQ(text_of(file.read()), "old");
    EXPECT_EQ(slurp(file.target()), "old");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

// The target fails the caller's check and the backup passes it: the backup is restored.
void expect_backup_restored_when_target_fails_the_check()
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.target(), "torn");
    put(file.backup_path(), "good old");
    EXPECT_EQ(text_of(file.read(starts_good)), "good old");
    EXPECT_EQ(slurp(file.target()), "good old");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

// Neither passes: the caller gets the target to judge, and nothing is deleted.
void expect_nothing_deleted_when_neither_passes()
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.target(), "torn");
    put(file.backup_path(), "also torn");
    EXPECT_EQ(text_of(file.read(starts_good)), "torn");
    EXPECT_EQ(names_in(temp.path()), (std::set<std::string>{"data.json", "data.json.bak"}));
}

// A temporary file a crash left is overwritten by the next write.
void expect_leftover_temporary_overwritten()
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.target(), "old");
    put(file.temporary_path(), "half a wri");
    EXPECT_EQ(text_of(file.read()), "old");
    file.write(bytes_of("new"));
    EXPECT_EQ(text_of(file.read()), "new");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

TEST(AtomicFile, LeftoverBackupSettledAtNextRead)
{
    expect_verified_target_wins();
    expect_backup_restored_when_target_is_missing();
    expect_backup_restored_when_target_fails_the_check();
    expect_nothing_deleted_when_neither_passes();
    expect_leftover_temporary_overwritten();
}

TEST(AtomicFile, UndeletedBackupIsSettledLater)
{
    const TempFolder temp;
    AtomicFileOptions options;
    options.seams.fail = fail_step(AtomicFileStep::DeleteBackup, ERROR_SHARING_VIOLATION);
    const AtomicFile file{temp.path() / "data.json", options};
    put(file.target(), "previous");

    // The new version is in place and verified, so the write succeeded.
    file.write(bytes_of("replacement"));
    EXPECT_EQ(slurp(file.target()), "replacement");
    EXPECT_EQ(slurp(file.backup_path()), "previous");

    EXPECT_EQ(text_of(file.read()), "replacement");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

TEST(AtomicFile, LockedTargetIsReportedAndKept)
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.target(), "previous");
    {
        const auto held = hold_exclusively(file.target());
        ASSERT_TRUE(held);
        const Error error = error_of([&file] { file.write(bytes_of("replacement")); });
        EXPECT_EQ(error.call(), "ReplaceFileW");
        EXPECT_NE(std::string_view{error.what()}.find("data.json"), std::string_view::npos);
    }
    EXPECT_EQ(slurp(file.target()), "previous");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});

    // Once the other program lets go, the same write goes through.
    file.write(bytes_of("replacement"));
    EXPECT_EQ(slurp(file.target()), "replacement");
}

TEST(AtomicFile, ReadOnlyTargetIsReportedAndKept)
{
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.target(), "previous");
    ASSERT_NE(SetFileAttributesW(file.target().c_str(), FILE_ATTRIBUTE_READONLY), FALSE);

    const Error error = error_of([&file] { file.write(bytes_of("replacement")); });
    EXPECT_NE(SetFileAttributesW(file.target().c_str(), FILE_ATTRIBUTE_NORMAL), FALSE);
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_ACCESS_DENIED));
    EXPECT_EQ(slurp(file.target()), "previous");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

// A writer that cannot get the lock in its wait reports, naming the lock, and changes nothing.
void expect_impatient_writer_reports(const AtomicFile& file)
{
    using namespace std::chrono_literals;
    AtomicFileOptions impatient;
    impatient.lock_wait = 50ms;
    const AtomicFile hurried{file.target(), impatient};
    const std::string before = slurp(file.target());
    {
        const auto held = file.lock();
        const Error error = error_of([&hurried] { hurried.write(bytes_of("third")); });
        EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_SHARING_VIOLATION));
        EXPECT_TRUE(std::string{error.what()}.contains("data.json.lock")) << error.what();
    }
    EXPECT_EQ(slurp(file.target()), before);
}

TEST(AtomicFile, SecondWriterWaitsForTheLock)
{
    using namespace std::chrono_literals;
    const TempFolder temp;
    AtomicFileOptions patient;
    patient.lock_wait = 30s;
    const AtomicFile file{temp.path() / "data.json", patient};
    put(file.target(), "previous");

    std::optional<AtomicFile::Session> first{file.lock()};
    std::thread second{[&file] { file.write(bytes_of("second")); }};
    // The second writer is waiting for the lock, so the first still sees and writes its own version.
    std::this_thread::sleep_for(150ms);
    EXPECT_EQ(slurp(file.target()), "previous");
    if (first.has_value())
    {
        first->write(bytes_of("first"));
    }
    EXPECT_EQ(slurp(file.target()), "first");
    first.reset();
    second.join();
    EXPECT_EQ(slurp(file.target()), "second");

    expect_impatient_writer_reports(file);
    // The lock file goes when its holder lets go.
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

TEST(AtomicFile, OverLimitFileIsRefused)
{
    const TempFolder temp;
    AtomicFileOptions options;
    options.max_read_bytes = 8;
    const AtomicFile file{temp.path() / "data.json", options};

    put(file.target(), "12345678");
    EXPECT_EQ(text_of(file.read()), "12345678");
    put(file.target(), "123456789");
    const Error error = error_of([&file] { static_cast<void>(file.read()); });
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_FILE_TOO_LARGE));
    EXPECT_EQ(slurp(file.target()), "123456789");
}

TEST(AtomicFile, ReadTakesNoLockAndWritesNothing)
{
    using namespace std::chrono_literals;
    const TempFolder temp;
    const AtomicFile file{temp.path() / "data.json"};
    put(file.target(), "contents");

    // Another holder has the lock for longer than this test may run: a read that wanted it would wait and fail.
    const auto held = hold_exclusively(file.lock_path());
    ASSERT_TRUE(held);
    const auto started = std::chrono::steady_clock::now();
    EXPECT_EQ(text_of(file.read()), "contents");
    EXPECT_LT(std::chrono::steady_clock::now() - started, 1s);
    EXPECT_EQ(names_in(temp.path()), (std::set<std::string>{"data.json", "data.json.lock"}));
}

// A write whose target reads back wrong and whose restore then fails: the report names both failures and both
// files, and neither copy is lost.
void expect_failed_restore_keeps_both(const AtomicFile& file)
{
    const Error error = error_of([&file] { file.write(bytes_of("unverified")); });
    const std::string report{error.what()};
    EXPECT_EQ(error.code(), static_cast<std::uint32_t>(ERROR_CRC));
    EXPECT_TRUE(report.contains("restoring the previous version then failed with error 21")) << report;
    EXPECT_TRUE(report.contains("data.json.bak")) << report;
    EXPECT_EQ(slurp(file.target()), "unverified");
    EXPECT_EQ(slurp(file.backup_path()), "good previous");
}

TEST(AtomicFile, FailedRestoreKeepsBothCopiesAndSettlesLater)
{
    const TempFolder temp;
    bool drive_gone = true;
    AtomicFileOptions options;
    options.seams.read_back = corrupt_read_back(AtomicFileStep::ReadBackTarget, &drive_gone);
    options.seams.fail = fail_step(AtomicFileStep::RestoreBackup, ERROR_NOT_READY, &drive_gone);
    const AtomicFile file{temp.path() / "data.json", options};
    put(file.target(), "good previous");
    expect_failed_restore_keeps_both(file);

    // The next read, with the caller's check, restores the version that passes it.
    drive_gone = false;
    EXPECT_EQ(text_of(file.read(starts_good)), "good previous");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});

    // And a write after the same double failure settles it too.
    drive_gone = true;
    expect_failed_restore_keeps_both(file);
    drive_gone = false;
    file.write(bytes_of("good next"));
    EXPECT_EQ(text_of(file.read(starts_good)), "good next");
    EXPECT_EQ(names_in(temp.path()), std::set<std::string>{"data.json"});
}

} // namespace
