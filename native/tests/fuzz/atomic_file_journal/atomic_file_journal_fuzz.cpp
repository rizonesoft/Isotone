// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// The libFuzzer entry point for the journal reader of AtomicFile (D01 T27 §2): any bytes are read without a fault.
#include "isotone/core/atomic_file.h"

#include <cstddef>
#include <cstdint>
#include <span>

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t* data, std::size_t size)
{
    if (data == nullptr)
    {
        return 0;
    }
    static_cast<void>(isotone::core::is_atomic_file_journal(std::as_bytes(std::span{data, size})));
    return 0;
}
