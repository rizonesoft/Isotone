#pragma once

#include <cstdint>
#include <span>

namespace isotone::fuzz::qualify
{

struct record_summary
{
    std::uint8_t kind{0U};
    std::uint16_t length{0U};
    std::uint32_t checksum{0U};
};

// Parses a length-prefixed qualification record and computes its byte checksum. Returns false when the input is not a
// valid, complete record within the 256-byte qualification payload bound.
bool parse_record(std::span<const std::uint8_t> bytes, record_summary& out);

} // namespace isotone::fuzz::qualify
