// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// foundation-host.exe: the entry point of the foundation test host (host.h, README.md).

#include "host.h"

#include <cstddef>
#include <span>
#include <string>
#include <vector>

int wmain(int argc, wchar_t** argv)
{
    std::vector<std::wstring> arguments;
    const std::span<wchar_t*> all{argv, static_cast<std::size_t>(argc)};
    // The first argument is the program's own name.
    for (const wchar_t* argument : all.subspan(all.empty() ? 0 : 1))
    {
        arguments.emplace_back(argument);
    }
    return isotone::foundation_host::run_host(arguments);
}
