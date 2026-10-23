// The AddressSanitizer lane's negative probe (D00 T05 §5): writes one byte past a heap allocation. Instrumented, the
// write stops the run with AddressSanitizer's heap-buffer-overflow report, which the asan_probe test requires; without
// instrumentation the run reaches the end with no report, and the test fails.
#include <cstddef>
#include <cstdio>
#include <memory>

int main()
{
    constexpr std::size_t size = 8;
    const auto buffer = std::make_unique<char[]>(size);
    // volatile, so the optimizer keeps the out-of-bounds store.
    volatile char* const bytes = buffer.get();
    bytes[size] = 1;
    std::puts("asan_probe: no AddressSanitizer report, so this build is not instrumented");
    return 0;
}
