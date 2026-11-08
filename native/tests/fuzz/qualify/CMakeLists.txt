# The qualification fuzz target and its two linked static libraries (D00 T05 §9, D00-T05-S8-PR10).
isotone_add_library(qualify_wire qualify_wire.cpp PUBLIC_INCLUDE "${CMAKE_CURRENT_SOURCE_DIR}")
isotone_add_library(qualify_parser qualify_parser.cpp PUBLIC_INCLUDE "${CMAKE_CURRENT_SOURCE_DIR}")
target_link_libraries(qualify_parser PUBLIC qualify_wire)
if(ISOTONE_FUZZ_QUALIFY)
  target_compile_definitions(qualify_parser PRIVATE ISOTONE_FUZZ_QUALIFY=1)
endif()
set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS qualify_wire qualify_parser)

isotone_add_fuzz_target(
  qualify
  SOURCES qualify_fuzz.cpp
  LIBRARIES qualify_parser)
