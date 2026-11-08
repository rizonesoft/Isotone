#pragma once

#include <cstddef>
#include <cstdint>
#include <optional>
#include <span>

namespace isotone::fuzz::qualify
{

struct wire_frame
{
    std::uint8_t kind{0U};
    std::uint16_t declared_length{0U};
    std::span<const std::uint8_t> payload;
};

// Decodes the 7-byte header (`"ISOT"`, 1-byte kind, 2-byte little-endian declared payload length) of a qualification
// frame and returns the remaining payload span without trusting `declared_length`.
std::optional<wire_frame> decode_wire_frame(std::span<const std::uint8_t> bytes) noexcept;

} // namespace isotone::fuzz::qualify
