// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// The generated token tables and isotone::ui::Theme against docs/design/tokens.json, which these tests read
// themselves: nothing here repeats a value the generator read.

#include "isotone/ui/theme.h"

#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <fstream>
#include <gtest/gtest.h>
#include <iterator>
#include <nlohmann/json.hpp>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <type_traits>
#include <variant>
#include <vector>

namespace
{

using isotone::ui::Brightness;
using isotone::ui::Color;
using isotone::ui::Density;
using isotone::ui::Easing;
using isotone::ui::find_token;
using isotone::ui::FontFamily;
using isotone::ui::Highlight;
using isotone::ui::HighlightColors;
using isotone::ui::kBrightnessCount;
using isotone::ui::kSystemColorCount;
using isotone::ui::kTokenCount;
using isotone::ui::linear;
using isotone::ui::LinearColor;
using isotone::ui::Shadow;
using isotone::ui::SystemColor;
using isotone::ui::Theme;
using isotone::ui::ThemeState;
using isotone::ui::token_name;
using isotone::ui::token_type;
using isotone::ui::TokenKey;
using isotone::ui::TokenType;
using isotone::ui::TokenValue;
using isotone::ui::TypeStyle;
using Json = nlohmann::json;

constexpr std::array<std::string_view, kBrightnessCount> kThemeIds{"dark", "darkest", "medium", "light"};
constexpr std::array<std::string_view, kSystemColorCount> kSystemNames{
    "window", "windowText", "grayText", "highlight", "highlightText", "hotlight", "buttonFace", "buttonText"};

const Json& source()
{
    static const Json tokens = [] {
        std::ifstream file{ISOTONE_TOKENS_JSON};
        return Json::parse(file);
    }();
    return tokens;
}

TokenKey key_of(std::string_view name)
{
    const auto key = find_token(name);
    EXPECT_TRUE(key.has_value()) << "no token key named " << name;
    return key.value_or(TokenKey{});
}

constexpr Color make_color(std::uint8_t red, std::uint8_t green, std::uint8_t blue, std::uint8_t alpha = UINT8_MAX)
{
    return Color{.red = red, .green = green, .blue = blue, .alpha = alpha};
}

std::uint8_t hex_byte(std::string_view text, std::size_t offset)
{
    return static_cast<std::uint8_t>(std::stoul(std::string{text.substr(offset, 2)}, nullptr, 16));
}

// "#rrggbb" or "#rrggbbaa" as a Color.
Color color_of(std::string_view text)
{
    constexpr std::size_t kWithAlpha = 9;
    constexpr std::uint8_t kOpaque = 255;
    return make_color(hex_byte(text, 1), hex_byte(text, 3), hex_byte(text, 5),
                      text.size() == kWithAlpha ? hex_byte(text, 7) : kOpaque);
}

// The number in front of a unit: "24px", "100ms", "0.04em".
float number_of(const std::string& text)
{
    return std::stof(text);
}

// A token's value for one theme: tokens.json gives one value, or one per theme.
std::string theme_value(const Json& value, std::size_t theme)
{
    return value.is_string() ? value.get<std::string>() : value.at(std::string{kThemeIds.at(theme)}).get<std::string>();
}

ThemeState state_for(std::size_t theme)
{
    ThemeState state;
    state.brightness = static_cast<Brightness>(theme);
    return state;
}

template <typename Value> Value resolved(const Theme& theme, std::string_view name)
{
    const TokenValue value = theme.resolve(key_of(name));
    EXPECT_TRUE(std::holds_alternative<Value>(value)) << name;
    return std::holds_alternative<Value>(value) ? std::get<Value>(value) : Value{};
}

// Nine colors no token has, so a computed Highlight is told apart from every generated value.
HighlightColors computed_accent()
{
    constexpr std::uint8_t kBase = 201;
    std::uint8_t next = kBase;
    const auto fresh = [&next] { return make_color(next++, 1, 2); };
    HighlightColors accent;
    accent.state = fresh();
    accent.state_hover = fresh();
    accent.state_pressed = fresh();
    accent.state_on = fresh();
    accent.state_subtle = fresh();
    accent.state_tint = fresh();
    accent.state_line = fresh();
    accent.state_text = fresh();
    accent.glow = fresh();
    return accent;
}

// Eight system colors no token has.
std::array<Color, kSystemColorCount> system_colors()
{
    constexpr std::uint8_t kBase = 101;
    std::array<Color, kSystemColorCount> colors{};
    std::uint8_t next = kBase;
    for (Color& color : colors)
    {
        color = make_color(3, next++, 4);
    }
    return colors;
}

std::size_t index_of_type(TokenType type)
{
    switch (type)
    {
    case TokenType::Color:
        return 0;
    case TokenType::Size:
        return 1;
    case TokenType::Duration:
        return 2;
    case TokenType::Easing:
        return 3;
    case TokenType::Shadow:
        return 4;
    case TokenType::TypeStyle:
        break;
    }
    return 5;
}

// Every key resolves, in this state, to a value of the key's own type.
void expect_every_key_resolves(const ThemeState& state)
{
    const Theme theme{state};
    for (std::size_t index = 0; index < kTokenCount; ++index)
    {
        const auto key = static_cast<TokenKey>(index);
        EXPECT_EQ(theme.resolve(key).index(), index_of_type(token_type(key))) << token_name(key);
    }
}

// Every Highlight, density, and contrast state of one brightness theme, with and without a computed accent.
void expect_every_state_resolves(std::size_t brightness)
{
    for (const Highlight highlight : {Highlight::Blue, Highlight::IsotoneOrange, Highlight::WindowsAccent})
    {
        for (const Density density : {Density::Compact, Density::Comfortable})
        {
            ThemeState state = state_for(brightness);
            state.highlight = highlight;
            state.density = density;
            state.system_colors = system_colors();
            expect_every_key_resolves(state);
            state.high_contrast = true;
            expect_every_key_resolves(state);
            state.accent = computed_accent();
            expect_every_key_resolves(state);
            state.high_contrast = false;
            expect_every_key_resolves(state);
        }
    }
}

TEST(Theme, EveryKeyResolvesInEveryState)
{
    for (std::size_t brightness = 0; brightness < kBrightnessCount; ++brightness)
    {
        expect_every_state_resolves(brightness);
    }
}

// A value that is not a key is refused, not read past the tables.
TEST(Theme, AValueThatIsNotAKeyIsRefused)
{
    // The bits of the count, one past the last key: a value a damaged file or a stale binary could hand over.
    const auto past_the_end = std::bit_cast<TokenKey>(static_cast<std::underlying_type_t<TokenKey>>(kTokenCount));
    EXPECT_THROW(static_cast<void>(Theme{}.resolve(past_the_end)), std::out_of_range);
    EXPECT_THROW(static_cast<void>(token_name(past_the_end)), std::out_of_range);
    EXPECT_FALSE(find_token("no-such-token").has_value());
}

// Colors and aliases of tokens.json in one theme.
void expect_colors_match(std::size_t brightness)
{
    const Theme theme{state_for(brightness)};
    for (const Json& token : source().at("color").at("tokens"))
    {
        const auto name = token.at("name").get<std::string>();
        const std::string text = theme_value(token.at("value"), brightness);
        const Color expected =
            text.front() == '{' ? resolved<Color>(theme, text.substr(1, text.size() - 2)) : color_of(text);
        EXPECT_EQ(resolved<Color>(theme, name), expected) << name << " in " << kThemeIds.at(brightness);
    }
}

// Shadows of tokens.json in one theme: "x y blur #color".
void expect_shadows_match(std::size_t brightness)
{
    const Theme theme{state_for(brightness)};
    for (const Json& token : source().at("shadow").at("tokens"))
    {
        const auto name = token.at("name").get<std::string>();
        std::istringstream parts{theme_value(token.at("value"), brightness)};
        std::string offset_x;
        std::string offset_y;
        std::string blur;
        std::string color;
        parts >> offset_x >> offset_y >> blur >> color;
        const Shadow expected{.offset_x = number_of(offset_x),
                              .offset_y = number_of(offset_y),
                              .blur = number_of(blur),
                              .color = color_of(color)};
        EXPECT_EQ(resolved<Shadow>(theme, name), expected) << name << " in " << kThemeIds.at(brightness);
    }
}

void expect_sizes_match()
{
    const Theme theme;
    for (const std::string_view group : {"spacing", "radius", "size"})
    {
        for (const Json& token : source().at(std::string{group}).at("tokens"))
        {
            const auto name = token.at("name").get<std::string>();
            EXPECT_FLOAT_EQ(resolved<float>(theme, name), number_of(token.at("value").get<std::string>())) << name;
        }
    }
}

void expect_durations_and_easings_match()
{
    const Theme theme;
    for (const Json& token : source().at("duration").at("tokens"))
    {
        const auto name = token.at("name").get<std::string>();
        const auto text = token.at("value").get<std::string>();
        if (text.ends_with("ms"))
        {
            EXPECT_EQ(resolved<std::chrono::milliseconds>(theme, name).count(), std::stol(text)) << name;
            continue;
        }
        Easing expected;
        char comma = ',';
        std::istringstream curve{text.substr(text.find('(') + 1)};
        curve >> expected.x1 >> comma >> expected.y1 >> comma >> expected.x2 >> comma >> expected.y2;
        EXPECT_EQ(resolved<Easing>(theme, name), expected) << name;
    }
}

FontFamily family_of(const std::string& name)
{
    if (name == "display")
    {
        return FontFamily::Display;
    }
    return name == "mono" ? FontFamily::Mono : FontFamily::Sans;
}

// A type style as tokens.json gives it: letter spacing is in px or in em of the font size.
TypeStyle style_of(const std::string& family, const Json& style)
{
    TypeStyle expected;
    expected.family = family_of(family);
    expected.size = number_of(style.at("fontSize").get<std::string>());
    expected.line_height = number_of(style.at("lineHeight").get<std::string>());
    expected.weight = style.at("fontWeight").get<std::uint16_t>();
    const auto spacing = style.value("letterSpacing", std::string{"0px"});
    expected.letter_spacing = spacing.ends_with("em") ? number_of(spacing) * expected.size : number_of(spacing);
    return expected;
}

// The style with this name in tokens.json.
TypeStyle source_style(std::string_view name)
{
    for (const Json& group : source().at("type").at("groups"))
    {
        for (const Json& style : group.at("styles"))
        {
            if (style.at("name").get<std::string>() == name)
            {
                return style_of(group.at("family").get<std::string>(), style);
            }
        }
    }
    ADD_FAILURE() << "tokens.json has no type style named " << name;
    return TypeStyle{};
}

void expect_style_near(const TypeStyle& actual, const TypeStyle& expected, std::string_view name)
{
    EXPECT_EQ(actual.family, expected.family) << name;
    EXPECT_FLOAT_EQ(actual.size, expected.size) << name;
    EXPECT_FLOAT_EQ(actual.line_height, expected.line_height) << name;
    EXPECT_EQ(actual.weight, expected.weight) << name;
    EXPECT_NEAR(actual.letter_spacing, expected.letter_spacing, 1e-5F) << name;
}

// Every type style, under the density that selects its own values: a "-comfortable" style in Comfortable, the
// others in Compact.
void expect_type_styles_match()
{
    for (const Json& group : source().at("type").at("groups"))
    {
        for (const Json& style : group.at("styles"))
        {
            const auto name = style.at("name").get<std::string>();
            ThemeState state;
            state.density = name.ends_with("-comfortable") ? Density::Comfortable : Density::Compact;
            expect_style_near(resolved<TypeStyle>(Theme{state}, name),
                              style_of(group.at("family").get<std::string>(), style), name);
        }
    }
}

TEST(Theme, ValuesMatchTokensJson)
{
    for (std::size_t brightness = 0; brightness < kBrightnessCount; ++brightness)
    {
        expect_colors_match(brightness);
        expect_shadows_match(brightness);
    }
    expect_sizes_match();
    expect_durations_and_easings_match();
    expect_type_styles_match();
}

constexpr std::array<std::string_view, 8> kStateKeys{"state",        "state-hover", "state-pressed", "state-on",
                                                     "state-subtle", "state-tint",  "state-line",    "state-text"};

std::string orange_name(std::string_view state)
{
    return "state-orange" + std::string{state.substr(std::string_view{"state"}.size())};
}

// Isotone orange: each state key takes its state-orange token's value, the glow its orange glow, and nothing else
// moves.
void expect_orange_replaces_state(std::size_t brightness)
{
    const Theme blue{state_for(brightness)};
    ThemeState state = state_for(brightness);
    state.highlight = Highlight::IsotoneOrange;
    const Theme orange{state};
    for (const std::string_view key : kStateKeys)
    {
        EXPECT_EQ(resolved<Color>(orange, key), resolved<Color>(blue, orange_name(key))) << key;
    }
    EXPECT_EQ(resolved<Shadow>(orange, "glow-state"), resolved<Shadow>(blue, "glow-state-orange"));
    EXPECT_EQ(resolved<Color>(orange, "surface-panel"), resolved<Color>(blue, "surface-panel"));
    EXPECT_EQ(resolved<Color>(orange, "state-orange"), resolved<Color>(blue, "state-orange"));
}

// A computed Windows accent: the state keys take the supplied colors and the glow keeps its shape with the
// supplied color; with no table the choice resolves as Blue.
void expect_computed_accent_replaces_state()
{
    const Theme blue;
    ThemeState state;
    state.highlight = Highlight::WindowsAccent;
    const Theme without_table{state};
    state.accent = computed_accent();
    const Theme accent{state};
    const HighlightColors colors = computed_accent();
    EXPECT_EQ(resolved<Color>(accent, "state"), colors.state);
    EXPECT_EQ(resolved<Color>(accent, "state-text"), colors.state_text);
    EXPECT_EQ(resolved<Color>(accent, "focus-ring"), colors.state_line);
    auto glow = resolved<Shadow>(blue, "glow-state");
    glow.color = colors.glow;
    EXPECT_EQ(resolved<Shadow>(accent, "glow-state"), glow);
    EXPECT_EQ(resolved<Color>(without_table, "state"), resolved<Color>(blue, "state"));
    EXPECT_EQ(resolved<Color>(accent, "surface-panel"), resolved<Color>(blue, "surface-panel"));
}

TEST(Theme, OrangeAndComputedHighlightReplaceTheStateKeys)
{
    for (std::size_t brightness = 0; brightness < kBrightnessCount; ++brightness)
    {
        expect_orange_replaces_state(brightness);
    }
    expect_computed_accent_replaces_state();
}

Theme with_density(Density density)
{
    ThemeState state;
    state.density = density;
    return Theme{state};
}

// The value tokens.json gives a size token.
float source_size(std::string_view name)
{
    for (const Json& token : source().at("size").at("tokens"))
    {
        if (token.at("name").get<std::string>() == name)
        {
            return number_of(token.at("value").get<std::string>());
        }
    }
    ADD_FAILURE() << "tokens.json has no size token named " << name;
    return 0.0F;
}

TEST(Theme, DensitySelectsTheNeutralKeys)
{
    const Theme compact = with_density(Density::Compact);
    const Theme comfortable = with_density(Density::Comfortable);

    // A size pair: the neutral key follows the density, and the two explicit keys never change.
    EXPECT_FLOAT_EQ(resolved<float>(compact, "control-h"), source_size("control-h-compact"));
    EXPECT_FLOAT_EQ(resolved<float>(comfortable, "control-h"), source_size("control-h-comfortable"));
    EXPECT_FLOAT_EQ(resolved<float>(comfortable, "control-h-compact"), source_size("control-h-compact"));
    EXPECT_FLOAT_EQ(resolved<float>(compact, "control-h-comfortable"), source_size("control-h-comfortable"));
    EXPECT_NE(source_size("control-h-compact"), source_size("control-h-comfortable"));
}

// A type style: tokens.json names the Compact values `caption` and the Comfortable ones `caption-comfortable`.
TEST(Theme, DensitySelectsTheNeutralTypeStyles)
{
    const Theme compact = with_density(Density::Compact);
    const Theme comfortable = with_density(Density::Comfortable);
    for (const std::string_view name : {"caption", "body", "body-strong"})
    {
        const std::string text{name};
        const TypeStyle small = source_style(name);
        const TypeStyle large = source_style(text + "-comfortable");
        expect_style_near(resolved<TypeStyle>(compact, name), small, name);
        expect_style_near(resolved<TypeStyle>(comfortable, name), large, name);
        expect_style_near(resolved<TypeStyle>(comfortable, text + "-compact"), small, name);
        expect_style_near(resolved<TypeStyle>(compact, text + "-comfortable"), large, name);
        EXPECT_NE(small.size, large.size) << name;
    }
    // A style with no Comfortable sibling is the same in both.
    expect_style_near(resolved<TypeStyle>(comfortable, "title"), source_style("title"), "title");
}

// In one brightness theme: an alias has its target's value, and a change of Highlight reaches it through the target.
void expect_aliases_follow(std::size_t brightness)
{
    ThemeState state = state_for(brightness);
    const Theme blue{state};
    EXPECT_EQ(resolved<Color>(blue, "icon"), resolved<Color>(blue, "text-secondary"));
    EXPECT_EQ(resolved<Color>(blue, "focus-ring"), resolved<Color>(blue, "state-line"));
    EXPECT_EQ(resolved<Color>(blue, "handle-stroke"), resolved<Color>(blue, "state"));
    state.highlight = Highlight::IsotoneOrange;
    const Theme orange{state};
    EXPECT_EQ(resolved<Color>(orange, "focus-ring"), resolved<Color>(blue, "state-orange-line"));
    EXPECT_EQ(resolved<Color>(orange, "handle-stroke"), resolved<Color>(blue, "state-orange"));
}

TEST(Theme, AliasesFollowTheirTarget)
{
    for (std::size_t brightness = 0; brightness < kBrightnessCount; ++brightness)
    {
        expect_aliases_follow(brightness);
    }
}

// Under high contrast each color token is what color.highContrast says: a system color, transparent, or the
// theme's own value.
void expect_high_contrast_mapping(std::size_t brightness)
{
    ThemeState state = state_for(brightness);
    const Theme plain{state};
    state.high_contrast = true;
    state.system_colors = system_colors();
    const Theme contrast{state};
    const Json& mapping = source().at("color").at("highContrast").at("tokens");
    EXPECT_EQ(mapping.size(), source().at("color").at("tokens").size());
    for (const auto& [name, target_json] : mapping.items())
    {
        const auto target = target_json.get<std::string>();
        Color expected;
        if (target == "keep")
        {
            expected = resolved<Color>(plain, name);
        }
        else if (target != "none")
        {
            const auto found = std::ranges::find(kSystemNames, target);
            ASSERT_NE(found, kSystemNames.end()) << target;
            expected = state.system_colors.at(static_cast<std::size_t>(std::distance(kSystemNames.begin(), found)));
        }
        EXPECT_EQ(resolved<Color>(contrast, name), expected) << name << " -> " << target;
    }
}

TEST(Theme, HighContrastMapsEveryColor)
{
    for (std::size_t brightness = 0; brightness < kBrightnessCount; ++brightness)
    {
        expect_high_contrast_mapping(brightness);
    }
    // The Highlight choice does not reach a mapped color, and sizes do not change.
    ThemeState state;
    state.high_contrast = true;
    state.system_colors = system_colors();
    state.highlight = Highlight::IsotoneOrange;
    const Theme contrast{state};
    EXPECT_EQ(resolved<Color>(contrast, "state"),
              state.system_colors.at(static_cast<std::size_t>(SystemColor::Highlight)));
    EXPECT_FLOAT_EQ(resolved<float>(contrast, "control-h"), resolved<float>(Theme{}, "control-h"));
}

// The linear value of every sRGB byte is the standard's own formula, to a float's precision.
TEST(Theme, LinearValuesFollowTheSrgbCurve)
{
    constexpr int kBytes = 256;
    constexpr double kMaximum = 255.0;
    constexpr double kKnee = 0.04045;
    constexpr double kSlope = 12.92;
    constexpr double kOffset = 0.055;
    constexpr double kGamma = 2.4;
    for (int byte = 0; byte < kBytes; ++byte)
    {
        const double encoded = byte / kMaximum;
        const double expected =
            encoded <= kKnee ? encoded / kSlope : std::pow((encoded + kOffset) / (1.0 + kOffset), kGamma);
        const auto value = static_cast<std::uint8_t>(byte);
        const LinearColor actual = linear(make_color(value, value, value, value));
        EXPECT_FLOAT_EQ(actual.red, static_cast<float>(expected)) << byte;
        EXPECT_FLOAT_EQ(actual.blue, actual.green) << byte;
        EXPECT_FLOAT_EQ(actual.alpha, static_cast<float>(encoded)) << byte;
    }
}

} // namespace
