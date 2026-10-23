#include "isotone/core/build_info.h"

#include <gtest/gtest.h>

#include <regex>
#include <string>

TEST(BuildInfo, VersionIsSet) {
  EXPECT_FALSE(isotone::core::version().empty());
}

TEST(BuildInfo, BuildIdShape) {
  const std::string id{isotone::core::build_id()};
  EXPECT_TRUE(std::regex_match(id, std::regex{"^[0-9a-f]{12}(-dirty)?$"})) << id;
}
