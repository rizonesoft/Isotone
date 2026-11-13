// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// The libFuzzer entry point for the settings document reader (D01 T27 §2): any bytes are read without a fault, and
// a document the reader accepts is written and read again to the same document.
#include "isotone/core/settings.h"

#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <span>
#include <string>

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t* data, std::size_t size)
{
    if (data == nullptr)
    {
        return 0;
    }
    using isotone::core::inspect_settings_document;
    using isotone::core::SettingsDocument;

    std::string written;
    if (inspect_settings_document(std::as_bytes(std::span{data, size}), &written) != SettingsDocument::Supported)
    {
        return 0;
    }
    // Indenting can take a document the reader accepted past the size the reader accepts; the store refuses to
    // write that one (Settings.OversizedWriteIsRefused), so it is not a round trip to check.
    if (written.size() > isotone::core::kSettingsMaxBytes)
    {
        return 0;
    }
    std::string written_again;
    if (inspect_settings_document(std::as_bytes(std::span{written}), &written_again) != SettingsDocument::Supported ||
        written_again != written)
    {
        std::abort();
    }
    return 0;
}
