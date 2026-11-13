// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include "tokens.generated.h"

#include <array>
#include <chrono>
#include <cstdint>
#include <optional>
#include <string_view>
#include <variant>

namespace isotone::ui
{

// The Highlight color: the user's choice of the state color (docs/design/components/Highlight/README.md).
enum class Highlight : std::uint8_t
{
    Blue,
    IsotoneOrange,
    WindowsAccent,
};

enum class Density : std::uint8_t
{
    Compact,
    Comfortable,
};

// A color in linear light, alpha straight: what blending and the color pipeline work in.
struct LinearColor
{
    float red = 0.0F;
    float green = 0.0F;
    float blue = 0.0F;
    float alpha = 0.0F;
};

// The color's linear values, from the generated sRGB table (exact for every byte). Any thread.
[[nodiscard]] LinearColor linear(Color color) noexcept;

// The colors a Highlight supplies. The Windows accent option computes them at run time (the Highlight service) and
// hands them to the Theme; glow is the color of the glow-state shadow.
struct HighlightColors
{
    Color state;
    Color state_hover;
    Color state_pressed;
    Color state_on;
    Color state_subtle;
    Color state_tint;
    Color state_line;
    Color state_text;
    Color glow;
};

// What a Theme resolves for: every choice and every Windows state a token's value depends on. The Theme calls no
// window API: the caller reads the system colors (GetSysColor) and the accent and passes them in.
struct ThemeState
{
    Brightness brightness = Brightness::Dark;
    Highlight highlight = Highlight::Blue;
    Density density = Density::Compact;
    // The computed Windows accent colors. Without them the Windows accent choice resolves as Blue.
    std::optional<HighlightColors> accent;
    // Windows high contrast is on: color keys resolve through the high-contrast mapping.
    bool high_contrast = false;
    // The system colors, indexed by SystemColor; read only when high_contrast is set.
    std::array<Color, kSystemColorCount> system_colors{};
};

// The value of a token: a color, a size in DIPs, a duration, an easing curve, a shadow, or a type style.
using TokenValue = std::variant<Color, float, std::chrono::milliseconds, Easing, Shadow, TypeStyle>;

// The token's name as tokens.json spells it ("surface-panel"). Throws std::out_of_range for a value that is not a
// key. Any thread.
[[nodiscard]] std::string_view token_name(TokenKey key);

// What kind of value the key resolves to. Throws std::out_of_range for a value that is not a key. Any thread.
[[nodiscard]] TokenType token_type(TokenKey key);

// The key with this name, or nothing. Any thread.
[[nodiscard]] std::optional<TokenKey> find_token(std::string_view name) noexcept;

// Resolves token keys for one state. A style asks it for a key and never holds a value, so a change of theme,
// Highlight, density, or contrast is a change of state here and of nothing else. Not synchronized: the UI thread
// owns it (standards/cpp.md, Threading).
class Theme
{
  public:
    explicit Theme(const ThemeState& state = {});

    [[nodiscard]] const ThemeState& state() const noexcept;
    void set_state(const ThemeState& state);

    // The key's value in this state, always of the key's type (token_type): a neutral density key takes its
    // Compact or Comfortable value; an alias follows its target; the Isotone orange and the computed Windows accent
    // replace the state keys; and under high contrast a color key becomes its system color, transparent when its
    // fill is dropped, or stays the theme's own value where the design keeps it. Throws std::out_of_range for a
    // value that is not a key.
    [[nodiscard]] TokenValue resolve(TokenKey key) const;

  private:
    [[nodiscard]] Color color(TokenKey key, bool contrast) const;
    [[nodiscard]] Shadow shadow(TokenKey key) const;

    ThemeState state_;
};

} // namespace isotone::ui
