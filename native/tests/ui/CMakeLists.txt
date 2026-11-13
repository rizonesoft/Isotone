# The isotone::ui tests. theme_tests reads docs/design/tokens.json itself and compares it with the generated tables.
isotone_add_test(theme_tests theme_tests.cpp LINK isotone::ui nlohmann_json::nlohmann_json)
target_compile_definitions(theme_tests PRIVATE "ISOTONE_TOKENS_JSON=\"${PROJECT_SOURCE_DIR}/../docs/design/tokens.json\"")
