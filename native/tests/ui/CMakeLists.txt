# The isotone::ui tests. theme_tests reads docs/design/tokens.json itself and compares it with the generated tables.
isotone_add_test(theme_tests theme_tests.cpp LINK isotone::ui nlohmann_json::nlohmann_json)
isotone_add_test(dpi_tests dpi_tests.cpp LINK isotone::ui)
# The window tests embed the suite's application manifest, so their windows are per-monitor DPI aware v2 as an app's
# are and the DPI they read is the monitor's.
isotone_add_test(window_tests window_tests.cpp "${PROJECT_SOURCE_DIR}/ui/app.manifest" LINK isotone::ui)
target_compile_definitions(theme_tests PRIVATE "ISOTONE_TOKENS_JSON=\"${PROJECT_SOURCE_DIR}/../docs/design/tokens.json\"")
