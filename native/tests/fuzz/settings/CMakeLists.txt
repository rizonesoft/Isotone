# The fuzz target for the settings document reader of isotone::core (D01 T27 §2).
isotone_add_fuzz_target(
  settings
  SOURCES settings_fuzz.cpp
  LIBRARIES isotone::core)
