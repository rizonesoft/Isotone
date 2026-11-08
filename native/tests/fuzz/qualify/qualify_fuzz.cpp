// The libFuzzer entry point for the qualification record parser (D00 T05 §9).
#include "qualify_parser.h"

#include <cstddef>
#include <cstdint>
#include <span>

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t* data, std::size_t size)
{
    if (data == nullptr)
    {
        return 0;
    }
    isotone::fuzz::qualify::record_summary summary{};
    (void)isotone::fuzz::qualify::parse_record(std::span<const std::uint8_t>{data, size}, summary);
    return 0;
}
