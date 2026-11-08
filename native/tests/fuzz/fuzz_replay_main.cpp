// Deterministic corpus and regression replay driver for libFuzzer targets in non-fuzz presets (D00 T05 §9).
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#ifdef _MSC_VER
#include <crtdbg.h>
#endif
#include <memory>
#include <print>
#include <span>
#include <string>
#include <string_view>
#include <vector>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <Windows.h>

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t* data, std::size_t size);

namespace
{

struct find_handle_deleter
{
    void operator()(HANDLE handle) const noexcept
    {
        if (handle != nullptr && handle != INVALID_HANDLE_VALUE)
        {
            FindClose(handle);
        }
    }
};

struct file_handle_deleter
{
    void operator()(HANDLE handle) const noexcept
    {
        if (handle != nullptr && handle != INVALID_HANDLE_VALUE)
        {
            CloseHandle(handle);
        }
    }
};

bool collect_inputs(std::string_view root, std::vector<std::string>& files)
{
    const DWORD attrs = GetFileAttributesA(std::string{root}.c_str());
    if (attrs == INVALID_FILE_ATTRIBUTES || (attrs & FILE_ATTRIBUTE_DIRECTORY) == 0U)
    {
        return false;
    }

    std::string pattern{root};
    if (!pattern.empty() && pattern.back() != '/' && pattern.back() != '\\')
    {
        pattern.push_back('/');
    }
    const std::string prefix = pattern;
    pattern.push_back('*');

    WIN32_FIND_DATAA entry{};
    const std::unique_ptr<void, find_handle_deleter> handle{FindFirstFileA(pattern.c_str(), &entry)};
    if (handle.get() == INVALID_HANDLE_VALUE)
    {
        return false;
    }

    std::vector<std::string> local{};
    for (BOOL has_entry = TRUE; has_entry != FALSE; has_entry = FindNextFileA(handle.get(), &entry))
    {
        const std::string_view name{static_cast<const char*>(entry.cFileName)};
        if (name == "." || name == ".." || name == ".gitkeep")
        {
            continue;
        }
        const std::string child = prefix + std::string{name};
        if ((entry.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0U)
        {
            if (!collect_inputs(child, local))
            {
                return false;
            }
        }
        else
        {
            local.push_back(child);
        }
    }

    std::ranges::sort(local);
    files.insert(files.end(), local.begin(), local.end());
    return true;
}

bool read_bytes(const std::string& file_path, std::vector<std::uint8_t>& out)
{
    const std::unique_ptr<void, file_handle_deleter> handle{CreateFileA(
        file_path.c_str(), GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr)};
    if (handle.get() == INVALID_HANDLE_VALUE)
    {
        return false;
    }

    LARGE_INTEGER file_size{};
    if (GetFileSizeEx(handle.get(), &file_size) == FALSE || file_size.QuadPart < 0)
    {
        return false;
    }

    const auto byte_count = static_cast<std::size_t>(file_size.QuadPart);
    out.assign(byte_count, 0U);
    if (out.empty())
    {
        return true;
    }

    DWORD bytes_read = 0U;
    if (ReadFile(handle.get(), out.data(), static_cast<DWORD>(out.size()), &bytes_read, nullptr) == FALSE)
    {
        return false;
    }
    return static_cast<std::size_t>(bytes_read) == out.size();
}

} // namespace

int main(int argc, char** argv)
{
    try
    {
#ifdef _MSC_VER
        _set_abort_behavior(0, _WRITE_ABORT_MSG | _CALL_REPORTFAULT);
        _CrtSetReportMode(_CRT_ASSERT, _CRTDBG_MODE_FILE);
        _CrtSetReportFile(_CRT_ASSERT, _CRTDBG_FILE_STDERR);
        _CrtSetReportMode(_CRT_ERROR, _CRTDBG_MODE_FILE);
        _CrtSetReportFile(_CRT_ERROR, _CRTDBG_FILE_STDERR);
#endif
        if (argc < 2)
        {
            std::println(stderr, "fuzz-replay: expected at least one corpus or regressions directory");
            return 2;
        }

        const std::span<char*> args{argv, static_cast<std::size_t>(argc)};
        std::vector<std::string> files{};
        for (const char* raw_dir : args.subspan(1U))
        {
            const std::string_view dir{raw_dir};
            if (!collect_inputs(dir, files))
            {
                std::println(stderr, "fuzz-replay: directory missing or unreadable: {}", dir);
                return 2;
            }
        }

        if (files.empty())
        {
            std::println(stderr, "fuzz-replay: no input files found across corpus and regressions directories");
            return 2;
        }

        const std::uint8_t empty_byte = 0U;
        std::vector<std::uint8_t> buffer{};
        for (const std::string& file_path : files)
        {
            if (!read_bytes(file_path, buffer))
            {
                std::println(stderr, "fuzz-replay: failed to read input file: {}", file_path);
                return 2;
            }
            const std::uint8_t* ptr = buffer.empty() ? &empty_byte : buffer.data();
            const int result = LLVMFuzzerTestOneInput(ptr, buffer.size());
            if (result != 0)
            {
                std::println(stderr, "fuzz-replay: target returned {} on {}", result, file_path);
                return 1;
            }
        }

        std::println("fuzz-replay: replayed {} input(s)", files.size());
        return 0;
    }
    catch (...)
    {
        return 2;
    }
}
