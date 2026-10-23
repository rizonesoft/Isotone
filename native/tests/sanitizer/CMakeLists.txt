# The AddressSanitizer lane's negative probe (D00 T05 §5): it passes only when the sanitizer reports the overflow.
isotone_add_sanitizer_probe(asan_probe asan_probe_test.cpp "AddressSanitizer: heap-buffer-overflow")
