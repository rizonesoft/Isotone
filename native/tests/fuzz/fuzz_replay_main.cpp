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

std::string to_utf8(std::wstring_view wide)
{
    if (wide.empty())
    {
        return {};
    }
    const int required =
        WideCharToMultiByte(CP_UTF8, 0U, wide.data(), static_cast<int>(wide.size()), nullptr, 0, nullptr, nullptr);
    if (required <= 0)
    {
        return {};
    }
    std::string out(static_cast<std::size_t>(required), '\0');
    WideCharToMultiByte(CP_UTF8, 0U, wide.data(), static_cast<int>(wide.size()), out.data(), required, nullptr,
                        nullptr);
    return out;
}

bool is_cmd_space(wchar_t wch) noexcept
{
    return wch == L' ' || wch == L'\t';
}

void skip_cmd_spaces(std::wstring_view& cmd) noexcept
{
    while (!cmd.empty() && is_cmd_space(cmd.front()))
    {
        cmd.remove_prefix(1U);
    }
}

std::size_t consume_backslashes(std::wstring_view& cmd) noexcept
{
    std::size_t count = 0U;
    while (!cmd.empty() && cmd.front() == L'\\')
    {
        ++count;
        cmd.remove_prefix(1U);
    }
    return count;
}

std::wstring parse_one_arg(std::wstring_view& cmd)
{
    std::wstring current{};
    bool in_quotes = false;
    while (!cmd.empty())
    {
        const std::size_t backslashes = consume_backslashes(cmd);
        if (!cmd.empty() && cmd.front() == L'"')
        {
            current.append(backslashes / 2U, L'\\');
            cmd.remove_prefix(1U);
            if ((backslashes % 2U) != 0U)
            {
                current.push_back(L'"');
            }
            else if (in_quotes && !cmd.empty() && cmd.front() == L'"')
            {
                current.push_back(L'"');
                cmd.remove_prefix(1U);
            }
            else
            {
                in_quotes = !in_quotes;
            }
            continue;
        }
        current.append(backslashes, L'\\');
        if (cmd.empty() || (!in_quotes && is_cmd_space(cmd.front())))
        {
            break;
        }
        current.push_back(cmd.front());
        cmd.remove_prefix(1U);
    }
    return current;
}

std::vector<std::wstring> parse_command_line(std::wstring_view cmd)
{
    std::vector<std::wstring> args{};
    for (skip_cmd_spaces(cmd); !cmd.empty(); skip_cmd_spaces(cmd))
    {
        args.push_back(parse_one_arg(cmd));
    }
    return args;
}

bool collect_inputs(std::wstring_view root, std::vector<std::wstring>& files)
{
    const DWORD attrs = GetFileAttributesW(std::wstring{root}.c_str());
    if (attrs == INVALID_FILE_ATTRIBUTES || (attrs & FILE_ATTRIBUTE_DIRECTORY) == 0U)
    {
        return false;
    }

    std::wstring pattern{root};
    if (!pattern.empty() && pattern.back() != L'/' && pattern.back() != L'\\')
    {
        pattern.push_back(L'/');
    }
    const std::wstring prefix = pattern;
    pattern.push_back(L'*');

    WIN32_FIND_DATAW entry{};
    const std::unique_ptr<void, find_handle_deleter> handle{FindFirstFileW(pattern.c_str(), &entry)};
    if (handle.get() == INVALID_HANDLE_VALUE)
    {
        return false;
    }

    std::vector<std::wstring> local{};
    for (BOOL has_entry = TRUE; has_entry != FALSE; has_entry = FindNextFileW(handle.get(), &entry))
    {
        const std::wstring_view name{static_cast<const wchar_t*>(entry.cFileName)};
        if (name == L"." || name == L".." || name == L".gitkeep")
        {
            continue;
        }
        const std::wstring child = prefix + std::wstring{name};
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

bool read_bytes(const std::wstring& file_path, std::vector<std::uint8_t>& out)
{
    const std::unique_ptr<void, file_handle_deleter> handle{CreateFileW(
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

int main()
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
        const wchar_t* raw_cmd = GetCommandLineW();
        const std::vector<std::wstring> args =
            raw_cmd != nullptr ? parse_command_line(std::wstring_view{raw_cmd}) : std::vector<std::wstring>{};
        if (args.size() < 2U)
        {
            std::println(stderr, "fuzz-replay: expected at least one corpus or regressions directory");
            return 2;
        }

        const std::span<const std::wstring> dir_args = std::span<const std::wstring>{args}.subspan(1U);
        std::vector<std::wstring> files{};
        for (const std::wstring& dir : dir_args)
        {
            if (!collect_inputs(dir, files))
            {
                std::println(stderr, "fuzz-replay: directory missing or unreadable: {}", to_utf8(dir));
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
        for (const std::wstring& file_path : files)
        {
            if (!read_bytes(file_path, buffer))
            {
                std::println(stderr, "fuzz-replay: failed to read input file: {}", to_utf8(file_path));
                return 2;
            }
            const std::uint8_t* ptr = buffer.empty() ? &empty_byte : buffer.data();
            const int result = LLVMFuzzerTestOneInput(ptr, buffer.size());
            if (result != 0)
            {
                std::println(stderr, "fuzz-replay: target returned {} on {}", result, to_utf8(file_path));
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
