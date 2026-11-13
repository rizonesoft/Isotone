// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/ui/theme.h"

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <iterator>
#include <optional>
#include <string_view>

namespace isotone::ui
{
namespace
{

template <typename Enum> constexpr std::size_t index_of(Enum value) noexcept
{
    return static_cast<std::size_t>(value);
}

const tokens::KeyInfo& info_of(TokenKey key)
{
    return tokens::kKeys.at(index_of(key));
}

// The computed Highlight color that replaces a state key, or nothing for any other key.
std::optional<Color> accent_color(const HighlightColors& accent, TokenKey key) noexcept
{
    switch (key)
    {
    case TokenKey::State:
        return accent.state;
    case TokenKey::StateHover:
        return accent.state_hover;
    case TokenKey::StatePressed:
        return accent.state_pressed;
    case TokenKey::StateOn:
        return accent.state_on;
    case TokenKey::StateSubtle:
        return accent.state_subtle;
    case TokenKey::StateTint:
        return accent.state_tint;
    case TokenKey::StateLine:
        return accent.state_line;
    case TokenKey::StateText:
        return accent.state_text;
    default:
        return std::nullopt;
    }
}

} // namespace

LinearColor linear(Color color) noexcept
{
    // A byte indexes all 256 entries, so no lookup here can be out of range.
    const auto channel = [](std::uint8_t value) { return *std::next(tokens::kSrgbToLinear.begin(), value); };
    return LinearColor{.red = channel(color.red),
                       .green = channel(color.green),
                       .blue = channel(color.blue),
                       .alpha = static_cast<float>(color.alpha) / static_cast<float>(UINT8_MAX)};
}

std::string_view token_name(TokenKey key)
{
    return info_of(key).name;
}

TokenType token_type(TokenKey key)
{
    return info_of(key).type;
}

std::optional<TokenKey> find_token(std::string_view name) noexcept
{
    const auto found =
        std::ranges::find_if(tokens::kKeys, [name](const tokens::KeyInfo& info) { return info.name == name; });
    if (found == tokens::kKeys.end())
    {
        return std::nullopt;
    }
    return static_cast<TokenKey>(std::distance(tokens::kKeys.begin(), found));
}

Theme::Theme(const ThemeState& state) : state_{state}
{
}

const ThemeState& Theme::state() const noexcept
{
    return state_;
}

void Theme::set_state(const ThemeState& state)
{
    state_ = state;
}

Color Theme::color(TokenKey key, bool contrast) const
{
    if (contrast)
    {
        const tokens::Contrast& mapped = tokens::kHighContrast.at(index_of(key));
        if (mapped.rule == tokens::ContrastRule::None)
        {
            // The fill is dropped: fully transparent.
            return Color{};
        }
        if (mapped.rule == tokens::ContrastRule::System)
        {
            return state_.system_colors.at(index_of(mapped.system));
        }
        // Kept: the theme's own value, as resolved below with the mapping left out (a kept alias follows its
        // target's theme value, not its target's system color).
    }
    if (info_of(key).rule == tokens::Rule::Alias)
    {
        key = info_of(key).first;
    }
    if (state_.highlight == Highlight::IsotoneOrange)
    {
        key = tokens::kIsotoneOrange.at(index_of(key));
    }
    else if (state_.highlight == Highlight::WindowsAccent && state_.accent.has_value())
    {
        if (const auto replaced = accent_color(*state_.accent, key))
        {
            return *replaced;
        }
    }
    return tokens::kColors.at(index_of(state_.brightness)).at(info_of(key).slot);
}

Shadow Theme::shadow(TokenKey key) const
{
    const bool glow = key == TokenKey::GlowState;
    if (state_.highlight == Highlight::IsotoneOrange)
    {
        key = tokens::kIsotoneOrange.at(index_of(key));
    }
    Shadow value = tokens::kShadows.at(index_of(state_.brightness)).at(info_of(key).slot);
    if (glow && state_.highlight == Highlight::WindowsAccent && state_.accent.has_value())
    {
        value.color = state_.accent->glow;
    }
    return value;
}

TokenValue Theme::resolve(TokenKey key) const
{
    if (info_of(key).rule == tokens::Rule::Density)
    {
        key = state_.density == Density::Compact ? info_of(key).first : info_of(key).second;
    }
    const tokens::KeyInfo& info = info_of(key);
    switch (info.type)
    {
    case TokenType::Color:
        return color(key, state_.high_contrast);
    case TokenType::Shadow:
        return shadow(key);
    case TokenType::Size:
        return tokens::kSizes.at(info.slot);
    case TokenType::Duration:
        return std::chrono::milliseconds{tokens::kDurations.at(info.slot)};
    case TokenType::Easing:
        return tokens::kEasings.at(info.slot);
    case TokenType::TypeStyle:
        break;
    }
    return tokens::kTypeStyles.at(info.slot);
}

} // namespace isotone::ui
