# The AddressSanitizer lane's negative probe (D00 T05 §5): it passes only when the sanitizer reports the overflow, and
# only in the probe's own source file (the report's SUMMARY line names it), so an unrelated overflow cannot pass it.
isotone_add_sanitizer_probe(asan_probe asan_probe_test.cpp
  "SUMMARY: AddressSanitizer: heap-buffer-overflow [^\n]*asan_probe_test\\.cpp")
