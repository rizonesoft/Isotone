#include "qualify_wire.h"

#include <cstddef>
#include <cstdint>
#include <optional>
#include <span>

namespace isotone::fuzz::qualify
{

namespace
{

constexpr std::uint8_t byte_at(std::span<const std::uint8_t> bytes, std::size_t index) noexcept
{
    return bytes.subspan(index, 1U).front();
}

} // namespace

std::optional<wire_frame> decode_wire_frame(std::span<const std::uint8_t> bytes) noexcept
{
    constexpr std::size_t header_size = 7U;
    if (bytes.size() < header_size)
    {
        return std::nullopt;
    }
    if (byte_at(bytes, 0U) != static_cast<std::uint8_t>('I') || byte_at(bytes, 1U) != static_cast<std::uint8_t>('S') ||
        byte_at(bytes, 2U) != static_cast<std::uint8_t>('O') || byte_at(bytes, 3U) != static_cast<std::uint8_t>('T'))
    {
        return std::nullopt;
    }

    const std::uint8_t kind = byte_at(bytes, 4U);
    const auto low = static_cast<std::uint16_t>(byte_at(bytes, 5U));
    const auto high = static_cast<std::uint16_t>(static_cast<std::uint16_t>(byte_at(bytes, 6U)) << 8U);
    const auto declared_length = static_cast<std::uint16_t>(low | high);
    return wire_frame{
        .kind = kind,
        .declared_length = declared_length,
        .payload = bytes.subspan(header_size),
    };
}

} // namespace isotone::fuzz::qualify
