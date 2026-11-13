// generated from docs/design/tokens.json by scripts/generate-ui-tokens.py; do not edit
// clang-format off

#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <span>
#include <string_view>

namespace isotone::ui
{

// Every design token a surface may ask for (docs/design/tokens.json), the neutral key of each density
// pair, and the type styles. A style names a key and never a value.
enum class TokenKey : std::uint8_t
{
    Frame, // frame
    SurfacePanel, // surface-panel
    SurfaceTabstrip, // surface-tabstrip
    SurfaceRaised, // surface-raised
    SurfaceField, // surface-field
    SurfaceControl, // surface-control
    SurfaceControlHover, // surface-control-hover
    SurfaceControlPressed, // surface-control-pressed
    SurfaceHover, // surface-hover
    CanvasSurround, // canvas-surround
    RulerSurface, // ruler-surface
    Scrim, // scrim
    Divider, // divider
    DividerStrong, // divider-strong
    BorderControl, // border-control
    BorderControlHover, // border-control-hover
    BorderPopup, // border-popup
    ScrollThumb, // scroll-thumb
    ScrollThumbHover, // scroll-thumb-hover
    TextPrimary, // text-primary
    TextSecondary, // text-secondary
    TextDisabled, // text-disabled
    TextPlaceholder, // text-placeholder
    Icon, // icon
    State, // state
    StateHover, // state-hover
    StatePressed, // state-pressed
    StateOn, // state-on
    StateSubtle, // state-subtle
    StateTint, // state-tint
    StateLine, // state-line
    StateText, // state-text
    FocusRing, // focus-ring
    SelectionInactive, // selection-inactive
    StateOrange, // state-orange
    StateOrangeHover, // state-orange-hover
    StateOrangePressed, // state-orange-pressed
    StateOrangeOn, // state-orange-on
    StateOrangeSubtle, // state-orange-subtle
    StateOrangeTint, // state-orange-tint
    StateOrangeLine, // state-orange-line
    StateOrangeText, // state-orange-text
    AccentStilus, // accent-stilus
    AccentStilusHover, // accent-stilus-hover
    AccentStilusOn, // accent-stilus-on
    AccentGesso, // accent-gesso
    AccentGessoHover, // accent-gesso-hover
    AccentGessoOn, // accent-gesso-on
    AccentAlbumen, // accent-albumen
    AccentAlbumenHover, // accent-albumen-hover
    AccentAlbumenOn, // accent-albumen-on
    StatusError, // status-error
    StatusErrorSubtle, // status-error-subtle
    StatusWarning, // status-warning
    StatusWarningSubtle, // status-warning-subtle
    StatusSuccess, // status-success
    StatusSuccessSubtle, // status-success-subtle
    StatusInfo, // status-info
    StatusInfoSubtle, // status-info-subtle
    CaptionCloseHover, // caption-close-hover
    CaptionClosePressed, // caption-close-pressed
    CaptionCloseOn, // caption-close-on
    CheckerLight, // checker-light
    CheckerDark, // checker-dark
    Guide, // guide
    GuideSmart, // guide-smart
    AntsLight, // ants-light
    AntsDark, // ants-dark
    HandleFill, // handle-fill
    HandleStroke, // handle-stroke
    Artboard, // artboard
    ShadowTooltip, // shadow-tooltip
    ShadowPopup, // shadow-popup
    ShadowDialog, // shadow-dialog
    GlowState, // glow-state
    GlowStateOrange, // glow-state-orange
    SpaceHair, // space-hair
    Space1, // space-1
    Space15, // space-1-5
    Space2, // space-2
    Space3, // space-3
    Space4, // space-4
    Space6, // space-6
    RadiusSm, // radius-sm
    RadiusMd, // radius-md
    RadiusLg, // radius-lg
    RadiusRound, // radius-round
    ControlHCompact, // control-h-compact
    ControlHComfortable, // control-h-comfortable
    ControlHDialog, // control-h-dialog
    TitlebarH, // titlebar-h
    CaptionButtonW, // caption-button-w
    MenuRowHCompact, // menu-row-h-compact
    MenuRowHComfortable, // menu-row-h-comfortable
    MenuWMin, // menu-w-min
    OptionsbarHCompact, // optionsbar-h-compact
    OptionsbarHComfortable, // optionsbar-h-comfortable
    InfobarH, // infobar-h
    DoctabHCompact, // doctab-h-compact
    DoctabHComfortable, // doctab-h-comfortable
    DoctabWMax, // doctab-w-max
    ToolButtonCompact, // tool-button-compact
    ToolButtonComfortable, // tool-button-comfortable
    ToolrailWCompact, // toolrail-w-compact
    ToolrailWComfortable, // toolrail-w-comfortable
    PanelWMin, // panel-w-min
    PanelWDefault, // panel-w-default
    PanelWMax, // panel-w-max
    PanelTabHCompact, // panel-tab-h-compact
    PanelTabHComfortable, // panel-tab-h-comfortable
    PanelIconstripW, // panel-iconstrip-w
    SectionHeaderH, // section-header-h
    RowHCompact, // row-h-compact
    RowHComfortable, // row-h-comfortable
    LayerRowHCompact, // layer-row-h-compact
    LayerRowHComfortable, // layer-row-h-comfortable
    StatusbarHCompact, // statusbar-h-compact
    StatusbarHComfortable, // statusbar-h-comfortable
    RulerW, // ruler-w
    IconSm, // icon-sm
    IconMd, // icon-md
    IconStroke, // icon-stroke
    CheckSizeCompact, // check-size-compact
    CheckSizeComfortable, // check-size-comfortable
    ToggleW, // toggle-w
    SliderTrackH, // slider-track-h
    SliderThumb, // slider-thumb
    ScrollbarWRest, // scrollbar-w-rest
    ScrollbarWHover, // scrollbar-w-hover
    SwatchCompact, // swatch-compact
    SwatchComfortable, // swatch-comfortable
    ColorChip, // color-chip
    FocusRingW, // focus-ring-w
    HandleSize, // handle-size
    CheckerTile, // checker-tile
    TypeCaption, // type-caption
    TypeBodyCompact, // type-body-compact
    TypeBodyComfortable, // type-body-comfortable
    TypeTitle, // type-title
    DurationFast, // duration-fast
    DurationStandard, // duration-standard
    DurationSlow, // duration-slow
    TooltipDelay, // tooltip-delay
    EaseOut, // ease-out
    Caption, // caption
    Body, // body
    BodyStrong, // body-strong
    SectionHeader, // section-header
    Title, // title
    DialogTitle, // dialog-title
    CaptionComfortable, // caption-comfortable
    BodyComfortable, // body-comfortable
    BodyStrongComfortable, // body-strong-comfortable
    Display, // display
    Mono, // mono
    MonoBody, // mono-body
    ControlH, // control-h
    MenuRowH, // menu-row-h
    OptionsbarH, // optionsbar-h
    DoctabH, // doctab-h
    ToolButton, // tool-button
    ToolrailW, // toolrail-w
    PanelTabH, // panel-tab-h
    RowH, // row-h
    LayerRowH, // layer-row-h
    StatusbarH, // statusbar-h
    CheckSize, // check-size
    Swatch, // swatch
    TypeBody, // type-body
    CaptionCompact, // caption-compact
    BodyCompact, // body-compact
    BodyStrongCompact, // body-strong-compact
};

inline constexpr std::size_t kTokenCount = 172;

// What kind of value a key resolves to.
enum class TokenType : std::uint8_t
{
    Color,
    Size,
    Duration,
    Easing,
    Shadow,
    TypeStyle,
};

// The four interface brightness themes, in the order of tokens.json (Dark is the default).
enum class Brightness : std::uint8_t
{
    Dark,
    Darkest,
    MediumGray,
    Light,
};

inline constexpr std::size_t kBrightnessCount = 4;

// The Windows system colors the high-contrast mapping uses (GetSysColor).
enum class SystemColor : std::uint8_t
{
    Window,
    WindowText,
    GrayText,
    Highlight,
    HighlightText,
    Hotlight,
    ButtonFace,
    ButtonText,
};

inline constexpr std::size_t kSystemColorCount = 8;

enum class FontFamily : std::uint8_t
{
    Sans,
    Display,
    Mono,
};

// A color as sRGB bytes, alpha straight (not premultiplied). Its linear values come from one table
// (isotone::ui::linear in theme.h), so every color converts the same way.
struct Color
{
    std::uint8_t red = 0;
    std::uint8_t green = 0;
    std::uint8_t blue = 0;
    std::uint8_t alpha = 0;

    friend bool operator==(const Color& left, const Color& right) = default;
};

// A drop shadow or glow: offsets and blur radius in DIPs.
struct Shadow
{
    float offset_x = 0.0F;
    float offset_y = 0.0F;
    float blur = 0.0F;
    Color color;

    friend bool operator==(const Shadow& left, const Shadow& right) = default;
};

// A cubic Bezier easing curve: its two control points.
struct Easing
{
    float x1 = 0.0F;
    float y1 = 0.0F;
    float x2 = 0.0F;
    float y2 = 0.0F;

    friend bool operator==(const Easing& left, const Easing& right) = default;
};

// A type style: sizes, line height, and letter spacing in DIPs.
struct TypeStyle
{
    FontFamily family = FontFamily::Sans;
    float size = 0.0F;
    float line_height = 0.0F;
    std::uint16_t weight = 0;
    float letter_spacing = 0.0F;

    friend bool operator==(const TypeStyle& left, const TypeStyle& right) = default;
};

// The generated tables. Code reads them through isotone::ui::Theme (theme.h), never directly.
namespace tokens
{

// How a key gets its value: from its slot in its type's table, from another key (an alias), or from
// one of two keys by density.
enum class Rule : std::uint8_t
{
    Value,
    Alias,
    Density,
};

struct KeyInfo
{
    std::string_view name;
    TokenType type = TokenType::Color;
    Rule rule = Rule::Value;
    std::uint16_t slot = 0;
    TokenKey first = TokenKey{};  // the alias target, or the Compact key
    TokenKey second = TokenKey{}; // the Comfortable key
};

// What a color key becomes under Windows high contrast.
enum class ContrastRule : std::uint8_t
{
    Keep,
    None,
    System,
};

struct Contrast
{
    ContrastRule rule = ContrastRule::Keep;
    SystemColor system = SystemColor::Window;
};

inline constexpr std::size_t kColorCount = 68;
inline constexpr std::size_t kShadowCount = 5;
inline constexpr std::size_t kSizeCount = 63;
inline constexpr std::size_t kDurationCount = 4;
inline constexpr std::size_t kEasingCount = 1;
inline constexpr std::size_t kTypeStyleCount = 12;

extern const std::array<KeyInfo, kTokenCount> kKeys;
extern const std::array<std::array<Color, kColorCount>, kBrightnessCount> kColors;
extern const std::array<std::array<Shadow, kShadowCount>, kBrightnessCount> kShadows;
extern const std::array<float, kSizeCount> kSizes;
extern const std::array<std::int32_t, kDurationCount> kDurations;
extern const std::array<Easing, kEasingCount> kEasings;
extern const std::array<TypeStyle, kTypeStyleCount> kTypeStyles;
// The Isotone orange Highlight: each key's replacement, or the key itself.
extern const std::array<TokenKey, kTokenCount> kIsotoneOrange;
// Windows high contrast: what each key becomes (Keep for every key that is not a color).
extern const std::array<Contrast, kTokenCount> kHighContrast;
// The linear value of each sRGB byte.
extern const std::array<float, 256> kSrgbToLinear;

// The font families of a family list, most wanted first.
[[nodiscard]] std::span<const std::wstring_view> font_families(FontFamily family) noexcept;

} // namespace tokens

} // namespace isotone::ui
