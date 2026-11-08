#include "qualify_parser.h"

#include "qualify_wire.h"

#include <cstddef>
#include <cstdint>
#include <span>
#ifdef ISOTONE_FUZZ_QUALIFY
#include <cstdlib>
#include <vector>
#endif

namespace isotone::fuzz::qualify
{

bool parse_record(std::span<const std::uint8_t> bytes, record_summary& out)
{
    constexpr std::uint16_t max_payload_length = 256U;
    const auto frame = decode_wire_frame(bytes);
    if (!frame.has_value())
    {
        return false;
    }
    if (frame->declared_length > max_payload_length)
    {
        return false;
    }

#ifdef ISOTONE_FUZZ_QUALIFY
    // Planted qualification defect (D00 T05 §9): when kind is 'Q' (0x51), the payload is non-empty, and the declared
    // length exceeds the bytes actually remaining in the frame, index past the end of the heap-allocated payload copy.
    if (frame->kind == static_cast<std::uint8_t>('Q') && !frame->payload.empty() &&
        frame->declared_length > frame->payload.size())
    {
        const std::vector<std::uint8_t> truncated_copy(frame->payload.begin(), frame->payload.end());
        const volatile std::uint8_t oob_byte = truncated_copy.data()[frame->declared_length];
        (void)oob_byte;
        std::_Exit(1);
    }
#endif

    if (frame->declared_length > frame->payload.size())
    {
        return false;
    }

    const auto body = frame->payload.first(frame->declared_length);
    std::uint32_t checksum = 0U;
    for (const std::uint8_t value : body)
    {
        checksum = (checksum * 33U) + static_cast<std::uint32_t>(value);
    }

    out = record_summary{
        .kind = frame->kind,
        .length = frame->declared_length,
        .checksum = checksum,
    };
    return true;
}

} // namespace isotone::fuzz::qualify
