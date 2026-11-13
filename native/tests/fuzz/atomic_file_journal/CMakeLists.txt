# The fuzz target for the journal reader of isotone::core::AtomicFile (D01 T27 §2).
isotone_add_fuzz_target(
  atomic_file_journal
  SOURCES atomic_file_journal_fuzz.cpp
  LIBRARIES isotone::core)
