#!/usr/bin/env python3
"""Generate the token tables of isotone::ui from the design (D01 T14 §1).

    python scripts/generate-ui-tokens.py            # write native/ui/tokens/tokens.generated.h and .cpp
    python scripts/generate-ui-tokens.py --check    # exit 1 naming each token whose committed row is stale

docs/design/tokens.json is the source of every value a native surface draws with (standards/design-contract.md).
This script reads it and writes two C++ files: an enum of every token key, and typed tables that
isotone::ui::Theme (native/ui/include/isotone/ui/theme.h) resolves a key from. The files are never edited by hand:
change tokens.json, run this, commit both.

What the tables hold:

  keys          every token, the neutral density key of each -compact / -comfortable pair, and the type styles
  colors        one table per brightness theme, sRGB bytes and linear floats; an alias keeps its reference
  shadows       one table per brightness theme: offset, blur, and color
  single values sizes, spacing, and radii in DIPs, durations in milliseconds, the easing curve, type styles
  Highlight     the Isotone orange mapping (each state key to its state-orange token)
  high contrast every color token to a system color, to keep, or to none (color.highContrast)
  fonts         the three family lists, generic CSS names dropped
  sRGB table    the 256 linear values, so a color made at run time converts exactly as a generated one

A source it cannot read is refused naming the token (exit 2): a color that is not #rrggbb or #rrggbbaa, a size
without px, an alias to a token that does not exist, a theme without a value, a name used twice, a high-contrast
mapping that misses or misnames a token. Stdlib only; the output is byte for byte the same on every run.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "docs" / "design" / "tokens.json"
OUT_DIR = ROOT / "native" / "ui" / "tokens"
HEADER_NAME = "tokens.generated.h"
SOURCE_NAME = "tokens.generated.cpp"
MARK = "generated from docs/design/tokens.json by scripts/generate-ui-tokens.py; do not edit"

BRIGHTNESS = (("dark", "Dark"), ("darkest", "Darkest"), ("medium", "MediumGray"), ("light", "Light"))
SYSTEM_COLORS = ("window", "windowText", "grayText", "highlight", "highlightText", "hotlight", "buttonFace",
                 "buttonText")
FAMILIES = (("sans", "Sans"), ("display", "Display"), ("mono", "Mono"))
GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "ui-monospace", "system-ui", "cursive", "fantasy"}
STATE_KEYS = ("state", "state-hover", "state-pressed", "state-on", "state-subtle", "state-tint", "state-line",
              "state-text")
COMPACT, COMFORTABLE = "-compact", "-comfortable"

COLOR_RE = re.compile(r"^#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$")
ALIAS_RE = re.compile(r"^\{([a-z0-9-]+)\}$")
PX_RE = re.compile(r"^(-?\d+(?:\.\d+)?)px$")
MS_RE = re.compile(r"^(\d+)ms$")
EM_RE = re.compile(r"^(-?\d+(?:\.\d+)?)em$")
BEZIER_RE = re.compile(r"^cubic-bezier\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)$")
SHADOW_RE = re.compile(r"^(-?\d+(?:\.\d+)?)(?:px)? (-?\d+(?:\.\d+)?)(?:px)? (\d+(?:\.\d+)?)px (#[0-9a-fA-F]{6,8})$")
NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


class Refused(Exception):
    """The source cannot be read as design tokens; the message names the token."""


def refuse(token, reason) -> NoReturn:
    raise Refused(f"{token}: {reason}")


def pascal(name):
    return "".join(part.capitalize() for part in name.split("-"))


def key_base(model):
    """The smallest unsigned type that holds every key."""
    return "std::uint8_t" if len(model.keys) <= 256 else "std::uint16_t"


def number(value):
    """A float literal: always with a decimal point or an exponent, shortest text that reads back the same."""
    text = repr(float(value))
    return ("0.0F" if float(value) == 0 else text + "F")


def linear(channel):
    c = channel / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def parse_color(token, text):
    m = COLOR_RE.match(text) if isinstance(text, str) else None
    if not m:
        refuse(token, f"the color {text!r} is not #rrggbb or #rrggbbaa")
    rgb = m.group(1)
    alpha = int(m.group(2), 16) if m.group(2) else 255
    return (int(rgb[0:2], 16), int(rgb[2:4], 16), int(rgb[4:6], 16), alpha)


def color_literal(rgba):
    r, g, b, a = rgba
    return f"Color{{.red = {r}, .green = {g}, .blue = {b}, .alpha = {a}}}"


def parse_px(token, text):
    m = PX_RE.match(text) if isinstance(text, str) else None
    if not m:
        refuse(token, f"the size {text!r} is not a number followed by px")
    return float(m.group(1))


class Model:
    """Everything read from tokens.json, in the order the tables are written."""

    def __init__(self, source):
        self.keys = []          # (name, type, rule, payload) in enum order
        self.seen = {}
        self.colors = []        # color token names with a value per theme (the slot order)
        self.color_values = {}  # name -> {theme id: rgba}
        self.aliases = {}       # name -> target name
        self.shadows = []
        self.shadow_values = {}
        self.sizes, self.durations, self.easings, self.styles = [], [], [], []
        self.density = {}       # neutral name -> (compact name, comfortable name)
        self.high_contrast = {}
        self.families = {}
        self.read(source)

    def add(self, name, kind, rule, payload=None):
        if not isinstance(name, str) or not NAME_RE.match(name):
            refuse(name, "a token name is lowercase words joined by hyphens")
        if name in self.seen:
            refuse(name, f"the name is used twice ({self.seen[name]} and {kind})")
        clash = next((other for other in self.seen if pascal(other) == pascal(name)), None)
        if clash:
            refuse(name, f"the name reads the same as {clash} once the hyphens are gone")
        self.seen[name] = kind
        self.keys.append((name, kind, rule, payload))

    def read(self, source):
        themes = [t["id"] for t in source["color"]["themes"]]
        if themes != [b[0] for b in BRIGHTNESS]:
            refuse("color.themes", f"the themes are {themes}, and the tables are written for {[b[0] for b in BRIGHTNESS]}")
        for token in source["color"]["tokens"]:
            name, value = token["name"], token["value"]
            alias = ALIAS_RE.match(value) if isinstance(value, str) else None
            if alias:
                self.add(name, "Color", "Alias", alias.group(1))
                self.aliases[name] = alias.group(1)
                continue
            self.add(name, "Color", "Value", len(self.colors))
            self.colors.append(name)
            self.color_values[name] = self.per_theme(name, value, parse_color)
        for name, target in self.aliases.items():
            if target not in self.color_values:
                refuse(name, f"the alias names {target}, which is not a color token with a value")
        for token in source["shadow"]["tokens"]:
            name = token["name"]
            self.add(name, "Shadow", "Value", len(self.shadows))
            self.shadows.append(name)
            self.shadow_values[name] = self.per_theme(name, token["value"], self.parse_shadow)
        for group in ("spacing", "radius", "size"):
            for token in source[group]["tokens"]:
                self.add(token["name"], "Size", "Value", len(self.sizes))
                self.sizes.append((token["name"], parse_px(token["name"], token["value"])))
        for token in source["duration"]["tokens"]:
            name, value = token["name"], token["value"]
            bezier = BEZIER_RE.match(value) if isinstance(value, str) else None
            ms = MS_RE.match(value) if isinstance(value, str) else None
            if bezier:
                self.add(name, "Easing", "Value", len(self.easings))
                self.easings.append((name, tuple(float(g) for g in bezier.groups())))
            elif ms:
                self.add(name, "Duration", "Value", len(self.durations))
                self.durations.append((name, int(ms.group(1))))
            else:
                refuse(name, f"the value {value!r} is neither a duration in ms nor a cubic-bezier curve")
        self.read_type(source["type"])
        self.read_density()
        self.read_high_contrast(source["color"].get("highContrast"))

    def per_theme(self, name, value, parse):
        if isinstance(value, str):
            return {theme: parse(name, value) for theme, _ in BRIGHTNESS}
        if not isinstance(value, dict):
            refuse(name, "the value is neither one value nor one per theme")
        out = {}
        for theme, _ in BRIGHTNESS:
            if theme not in value:
                refuse(name, f"the theme {theme} has no value")
            out[theme] = parse(name, value[theme])
        return out

    @staticmethod
    def parse_shadow(name, text):
        m = SHADOW_RE.match(text) if isinstance(text, str) else None
        if not m:
            refuse(name, f"the shadow {text!r} is not 'x y blur #color'")
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), parse_color(name, m.group(4)))

    def read_type(self, type_source):
        for key, _ in FAMILIES:
            text = type_source["families"].get(key)
            if not isinstance(text, str):
                refuse(f"type.families.{key}", "the family list is missing")
            names = [part.strip().strip('"') for part in text.split(",")]
            names = [n for n in names if n and n.lower() not in GENERIC_FAMILIES]
            if not names or any(not n.isascii() or '"' in n or "\\" in n for n in names):
                refuse(f"type.families.{key}", f"the family list {text!r} has no usable family name")
            self.families[key] = names
        for group in type_source["groups"]:
            if group["family"] not in self.families:
                refuse(group["name"], f"the family {group['family']!r} is not one of {[f[0] for f in FAMILIES]}")
            for style in group["styles"]:
                name = style["name"]
                size = parse_px(name, style["fontSize"])
                spacing_text = style.get("letterSpacing", "0px")
                em = EM_RE.match(spacing_text)
                spacing = float(em.group(1)) * size if em else parse_px(name, spacing_text)
                weight = style["fontWeight"]
                if not isinstance(weight, int) or not 1 <= weight <= 1000:
                    refuse(name, f"the font weight {weight!r} is not a whole number from 1 to 1000")
                self.add(name, "TypeStyle", "Value", len(self.styles))
                self.styles.append((name, group["family"], size, parse_px(name, style["lineHeight"]), weight,
                                    round(spacing, 6)))

    def read_density(self):
        names = {key[0]: key[1] for key in self.keys}
        for name, kind in list(names.items()):
            if name.endswith(COMFORTABLE):
                base = name[: -len(COMFORTABLE)]
                if base + COMPACT in names:        # a size pair: the neutral key is new
                    if names[base + COMPACT] != kind:
                        refuse(name, f"{base + COMPACT} is a {names[base + COMPACT]} and this is a {kind}")
                    self.add(base, kind, "Density", (base + COMPACT, name))
                    self.density[base] = (base + COMPACT, name)
                elif base in names:                # a type style: its own name is the neutral key
                    if names[base] != kind:
                        refuse(name, f"{base} is a {names[base]} and this is a {kind}")
                    self.rename_to_compact(base)
                    self.density[base] = (base + COMPACT, name)
                else:
                    refuse(name, f"there is neither {base + COMPACT} nor {base} to pair it with")
        for name in names:
            if name.endswith(COMPACT) and name[: -len(COMPACT)] + COMFORTABLE not in names:
                refuse(name, f"there is no {name[: -len(COMPACT)] + COMFORTABLE} to pair it with")

    def rename_to_compact(self, base):
        """The style `base` becomes `base-compact` (same values), and `base` becomes the neutral key."""
        compact = base + COMPACT
        index = next(i for i, key in enumerate(self.keys) if key[0] == base)
        _, kind, rule, payload = self.keys[index]
        del self.seen[base]
        self.keys[index] = (base, kind, "Density", (compact, base + COMFORTABLE))
        self.seen[base] = kind
        self.add(compact, kind, rule, payload)
        self.styles[payload] = (compact,) + self.styles[payload][1:]

    def read_high_contrast(self, section):
        if not isinstance(section, dict) or not isinstance(section.get("tokens"), dict):
            refuse("color.highContrast", "the high-contrast mapping is missing")
        mapping = section["tokens"]
        colors = [key[0] for key in self.keys if key[1] == "Color"]
        for name in colors:
            if name not in mapping:
                refuse(name, "the high-contrast mapping does not name this color token")
        for name, target in mapping.items():
            if name not in colors:
                refuse(name, "the high-contrast mapping names a token that is not a color token")
            if target not in SYSTEM_COLORS and target not in ("keep", "none"):
                refuse(name, f"the high-contrast target {target!r} is not a system color, keep, or none")
        self.high_contrast = dict(mapping)
        for state in STATE_KEYS:
            orange = state.replace("state", "state-orange", 1)
            for name in (state, orange):
                if self.seen.get(name) != "Color":
                    refuse(name, "the Highlight needs this color token")
        for name in ("glow-state", "glow-state-orange"):
            if self.seen.get(name) != "Shadow":
                refuse(name, "the Highlight needs this shadow token")


# Writing -----------------------------------------------------------------------------------------------------------

def render_header(model):
    out = [f"// {MARK}", "// clang-format off", "", "#pragma once", "", "#include <array>", "#include <cstddef>",
           "#include <cstdint>", "#include <span>", "#include <string_view>", "", "namespace isotone::ui", "{", "",
           "// Every design token a surface may ask for (docs/design/tokens.json), the neutral key of each density",
           "// pair, and the type styles. A style names a key and never a value.",
           "enum class TokenKey : std::uint16_t", "{"]
    out += [f"    {pascal(name)}, // {name}" for name, _, _, _ in model.keys]
    out[out.index("enum class TokenKey : std::uint16_t")] = f"enum class TokenKey : {key_base(model)}"
    out += ["};", "", f"inline constexpr std::size_t kTokenCount = {len(model.keys)};", "",
            "// What kind of value a key resolves to.",
            "enum class TokenType : std::uint8_t", "{", "    Color,", "    Size,", "    Duration,", "    Easing,",
            "    Shadow,", "    TypeStyle,", "};", "",
            "// The four interface brightness themes, in the order of tokens.json (Dark is the default).",
            "enum class Brightness : std::uint8_t", "{"]
    out += [f"    {label}," for _, label in BRIGHTNESS]
    out += ["};", "", f"inline constexpr std::size_t kBrightnessCount = {len(BRIGHTNESS)};", "",
            "// The Windows system colors the high-contrast mapping uses (GetSysColor).",
            "enum class SystemColor : std::uint8_t", "{"]
    out += [f"    {name[0].upper() + name[1:]}," for name in SYSTEM_COLORS]
    out += ["};", "", f"inline constexpr std::size_t kSystemColorCount = {len(SYSTEM_COLORS)};", "",
            "enum class FontFamily : std::uint8_t", "{"]
    out += [f"    {label}," for _, label in FAMILIES]
    out += ["};", "",
            "// A color as sRGB bytes, alpha straight (not premultiplied). Its linear values come from one table",
            "// (isotone::ui::linear in theme.h), so every color converts the same way.",
            "struct Color", "{",
            "    std::uint8_t red = 0;", "    std::uint8_t green = 0;", "    std::uint8_t blue = 0;",
            "    std::uint8_t alpha = 0;", "",
            "    friend bool operator==(const Color& left, const Color& right) = default;", "};", "",
            "// A drop shadow or glow: offsets and blur radius in DIPs.",
            "struct Shadow", "{", "    float offset_x = 0.0F;", "    float offset_y = 0.0F;", "    float blur = 0.0F;",
            "    Color color;", "", "    friend bool operator==(const Shadow& left, const Shadow& right) = default;", "};", "",
            "// A cubic Bezier easing curve: its two control points.",
            "struct Easing", "{", "    float x1 = 0.0F;", "    float y1 = 0.0F;", "    float x2 = 0.0F;",
            "    float y2 = 0.0F;", "", "    friend bool operator==(const Easing& left, const Easing& right) = default;", "};", "",
            "// A type style: sizes, line height, and letter spacing in DIPs.",
            "struct TypeStyle", "{", "    FontFamily family = FontFamily::Sans;", "    float size = 0.0F;",
            "    float line_height = 0.0F;", "    std::uint16_t weight = 0;", "    float letter_spacing = 0.0F;", "",
            "    friend bool operator==(const TypeStyle& left, const TypeStyle& right) = default;", "};", "",
            "// The generated tables. Code reads them through isotone::ui::Theme (theme.h), never directly.",
            "namespace tokens", "{", "",
            "// How a key gets its value: from its slot in its type's table, from another key (an alias), or from",
            "// one of two keys by density.",
            "enum class Rule : std::uint8_t", "{", "    Value,", "    Alias,", "    Density,", "};", "",
            "struct KeyInfo", "{", "    std::string_view name;", "    TokenType type = TokenType::Color;",
            "    Rule rule = Rule::Value;", "    std::uint16_t slot = 0;",
            "    TokenKey first = TokenKey{};  // the alias target, or the Compact key",
            "    TokenKey second = TokenKey{}; // the Comfortable key", "};", "",
            "// What a color key becomes under Windows high contrast.",
            "enum class ContrastRule : std::uint8_t", "{", "    Keep,", "    None,", "    System,", "};", "",
            "struct Contrast", "{", "    ContrastRule rule = ContrastRule::Keep;",
            "    SystemColor system = SystemColor::Window;", "};", "",
            f"inline constexpr std::size_t kColorCount = {len(model.colors)};",
            f"inline constexpr std::size_t kShadowCount = {len(model.shadows)};",
            f"inline constexpr std::size_t kSizeCount = {len(model.sizes)};",
            f"inline constexpr std::size_t kDurationCount = {len(model.durations)};",
            f"inline constexpr std::size_t kEasingCount = {len(model.easings)};",
            f"inline constexpr std::size_t kTypeStyleCount = {len(model.styles)};", "",
            "extern const std::array<KeyInfo, kTokenCount> kKeys;",
            "extern const std::array<std::array<Color, kColorCount>, kBrightnessCount> kColors;",
            "extern const std::array<std::array<Shadow, kShadowCount>, kBrightnessCount> kShadows;",
            "extern const std::array<float, kSizeCount> kSizes;",
            "extern const std::array<std::int32_t, kDurationCount> kDurations;",
            "extern const std::array<Easing, kEasingCount> kEasings;",
            "extern const std::array<TypeStyle, kTypeStyleCount> kTypeStyles;",
            "// The Isotone orange Highlight: each key's replacement, or the key itself.",
            "extern const std::array<TokenKey, kTokenCount> kIsotoneOrange;",
            "// Windows high contrast: what each key becomes (Keep for every key that is not a color).",
            "extern const std::array<Contrast, kTokenCount> kHighContrast;",
            "// The linear value of each sRGB byte.",
            "extern const std::array<float, 256> kSrgbToLinear;", "",
            "// The font families of a family list, most wanted first.",
            "[[nodiscard]] std::span<const std::wstring_view> font_families(FontFamily family) noexcept;", "",
            "} // namespace tokens", "", "} // namespace isotone::ui", ""]
    return "\n".join(out)


def key_info(name, kind, rule, payload):
    if rule == "Value":
        return (f"KeyInfo{{.name = \"{name}\", .type = TokenType::{kind}, .rule = Rule::Value, .slot = {payload}, "
                f".first = TokenKey::{pascal(name)}, .second = TokenKey::{pascal(name)}}}")
    if rule == "Alias":
        return (f"KeyInfo{{.name = \"{name}\", .type = TokenType::{kind}, .rule = Rule::Alias, .slot = 0, "
                f".first = TokenKey::{pascal(payload)}, .second = TokenKey::{pascal(payload)}}}")
    return (f"KeyInfo{{.name = \"{name}\", .type = TokenType::{kind}, .rule = Rule::Density, .slot = 0, "
            f".first = TokenKey::{pascal(payload[0])}, .second = TokenKey::{pascal(payload[1])}}}")


def render_source(model):
    out = [f"// {MARK}", "// clang-format off", "", f'#include "{HEADER_NAME}"', "", "#include <array>", "#include <bit>",
           "#include <cstdint>", "#include <span>", "#include <string_view>", "", "namespace isotone::ui::tokens", "{",
           "", "const std::array<KeyInfo, kTokenCount> kKeys{{"]
    out += [f"    {key_info(*key)}, // {key[0]}" for key in model.keys]
    out += ["}};", "", "const std::array<std::array<Color, kColorCount>, kBrightnessCount> kColors{{"]
    for theme, label in BRIGHTNESS:
        out.append(f"    {{{{ // {label}")
        out += [f"        {color_literal(model.color_values[name][theme])}, // {name} ({theme})" for name in model.colors]
        out.append("    }},")
    out += ["}};", "", "const std::array<std::array<Shadow, kShadowCount>, kBrightnessCount> kShadows{{"]
    for theme, label in BRIGHTNESS:
        out.append(f"    {{{{ // {label}")
        for name in model.shadows:
            x, y, blur, rgba = model.shadow_values[name][theme]
            out.append(f"        Shadow{{.offset_x = {number(x)}, .offset_y = {number(y)}, .blur = {number(blur)}, "
                       f".color = {color_literal(rgba)}}}, // {name} ({theme})")
        out.append("    }},")
    out += ["}};", "", "const std::array<float, kSizeCount> kSizes{{"]
    out += [f"    {number(value)}, // {name}" for name, value in model.sizes]
    out += ["}};", "", "const std::array<std::int32_t, kDurationCount> kDurations{{"]
    out += [f"    {value}, // {name}" for name, value in model.durations]
    out += ["}};", "", "const std::array<Easing, kEasingCount> kEasings{{"]
    out += [f"    Easing{{.x1 = {number(c[0])}, .y1 = {number(c[1])}, .x2 = {number(c[2])}, .y2 = {number(c[3])}}}, // {name}"
            for name, c in model.easings]
    out += ["}};", "", "const std::array<TypeStyle, kTypeStyleCount> kTypeStyles{{"]
    labels = dict(FAMILIES)
    out += [f"    TypeStyle{{.family = FontFamily::{labels[family]}, .size = {number(size)}, .line_height = {number(line)}, "
            f".weight = {weight}, .letter_spacing = {number(spacing)}}}, // {name}"
            for name, family, size, line, weight, spacing in model.styles]
    orange = {state: state.replace("state", "state-orange", 1) for state in STATE_KEYS}
    orange["glow-state"] = "glow-state-orange"
    out += ["}};", "", "const std::array<TokenKey, kTokenCount> kIsotoneOrange{{"]
    out += [f"    TokenKey::{pascal(orange.get(name, name))}, // {name}" for name, _, _, _ in model.keys]
    out += ["}};", "", "const std::array<Contrast, kTokenCount> kHighContrast{{"]
    for name, kind, _, _ in model.keys:
        target = model.high_contrast.get(name, "keep") if kind == "Color" else "keep"
        if target in ("keep", "none"):
            rule, system = ("Keep" if target == "keep" else "None"), "Window"
        else:
            rule, system = "System", target[0].upper() + target[1:]
        out.append(f"    Contrast{{.rule = ContrastRule::{rule}, .system = SystemColor::{system}}}, // {name}")
    out += ["}};", "", "const std::array<float, 256> kSrgbToLinear{{"]
    # Each value by its exact bits: a decimal literal would be rounded once more by the compiler, and a table of
    # data is not a place for the nearest named constant.
    out += [f"    std::bit_cast<float>(std::uint32_t{{0x{struct.unpack('<I', struct.pack('<f', linear(value)))[0]:08X}U}}), "
            f"// {value}: {linear(value):.9f}" for value in range(256)]
    out += ["}};", "", "namespace", "{", ""]
    for key, label in FAMILIES:
        names = ", ".join(f'L"{name}"' for name in model.families[key])
        out.append(f"constexpr std::array<std::wstring_view, {len(model.families[key])}> k{label}Families{{{{{names}}}}}; "
                   f"// type.families.{key}")
    out += ["", "} // namespace", "",
            "std::span<const std::wstring_view> font_families(FontFamily family) noexcept", "{",
            "    switch (family)", "    {"]
    for _, label in FAMILIES[1:]:
        out += [f"    case FontFamily::{label}:", f"        return k{label}Families;"]
    out += [f"    case FontFamily::{FAMILIES[0][1]}:", "        break;", "    }",
            f"    return k{FAMILIES[0][1]}Families;", "}", "", "} // namespace isotone::ui::tokens", ""]
    return "\n".join(out)


def generate(tokens_path):
    """{file name: text} for the source at tokens_path. Raises Refused."""
    try:
        source = json.loads(Path(tokens_path).read_text(encoding="utf-8"))
        model = Model(source)
    except (KeyError, TypeError) as error:
        raise Refused(f"tokens.json: a part the generator reads is missing or has another shape ({error!r})") from error
    return {HEADER_NAME: render_header(model), SOURCE_NAME: render_source(model)}


def stale_rows(name, committed, wanted):
    """One line for each row that differs, named by the token in its trailing comment."""
    old, new = committed.split("\n"), wanted.split("\n")
    rows = []
    for index in range(max(len(old), len(new))):
        a = old[index] if index < len(old) else ""
        b = new[index] if index < len(new) else ""
        if a != b:
            token = (b or a).rsplit("// ", 1)[-1].strip() if "// " in (b or a) else (b or a).strip()
            rows.append(f"{name}:{index + 1}: {token}")
    return rows


def write_atomically(path, text):
    """Temporary file beside the target, then replace, then read back (the repository's rule for tracked data)."""
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(text.encode("utf-8"))
    temporary.replace(path)
    if path.read_bytes() != text.encode("utf-8"):
        raise OSError(f"{path} did not read back as written")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate the isotone::ui token tables from docs/design/tokens.json.")
    parser.add_argument("--check", action="store_true", help="compare with the committed files; exit 1 on a difference")
    parser.add_argument("--tokens", default=str(TOKENS), help="the tokens.json to read (tests pass a fixture)")
    parser.add_argument("--out", default=str(OUT_DIR), help="the folder the two files are written to or checked in")
    args = parser.parse_args(argv)
    try:
        files = generate(args.tokens)
    except Refused as refused:
        print(f"generate-ui-tokens: {refused}")
        return 2
    except (OSError, json.JSONDecodeError) as error:
        print(f"generate-ui-tokens: {args.tokens} cannot be read: {error}")
        return 2
    out_dir = Path(args.out)
    if args.check:
        stale = []
        for name, text in files.items():
            path = out_dir / name
            committed = path.read_bytes().decode("utf-8").replace("\r\n", "\n") if path.is_file() else ""
            if committed != text:
                stale += stale_rows(name, committed, text) or [f"{name}: differs"]
        for row in stale[:40]:
            print(f"generate-ui-tokens: stale: {row}")
        if stale:
            print(f"generate-ui-tokens: {len(stale)} row(s) differ from docs/design/tokens.json; run "
                  f"python scripts/generate-ui-tokens.py and commit the result")
            return 1
        print(f"generate-ui-tokens: {', '.join(files)} are current")
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        write_atomically(out_dir / name, text)
    print(f"generate-ui-tokens: wrote {', '.join(str(Path(args.out) / name) for name in files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
