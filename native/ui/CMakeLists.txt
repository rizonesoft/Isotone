# isotone::ui, the suite's native UI toolkit. It starts with the design tokens: tables generated from
# docs/design/tokens.json by scripts/generate-ui-tokens.py (never edited by hand) and the Theme that resolves a
# token key for the current brightness theme, Highlight, density, and contrast (D01 T14 §1).
isotone_add_library(isotone_ui
  src/theme.cpp
  tokens/tokens.generated.cpp
  # Two folders: the hand-written headers, and the generated header beside its source (theme.h includes it by name).
  PUBLIC_INCLUDE "${CMAKE_CURRENT_SOURCE_DIR}/include" "${CMAKE_CURRENT_SOURCE_DIR}/tokens")
add_library(isotone::ui ALIAS isotone_ui)
target_link_libraries(isotone_ui PUBLIC isotone::core)
