// generated from docs/design/tokens.json by scripts/generate-ui-tokens.py; do not edit
// clang-format off

#include "tokens.generated.h"

#include <array>
#include <bit>
#include <cstdint>
#include <span>
#include <string_view>

namespace isotone::ui::tokens
{

const std::array<KeyInfo, kTokenCount> kKeys{{
    KeyInfo{.name = "frame", .type = TokenType::Color, .rule = Rule::Value, .slot = 0, .first = TokenKey::Frame, .second = TokenKey::Frame}, // frame
    KeyInfo{.name = "surface-panel", .type = TokenType::Color, .rule = Rule::Value, .slot = 1, .first = TokenKey::SurfacePanel, .second = TokenKey::SurfacePanel}, // surface-panel
    KeyInfo{.name = "surface-tabstrip", .type = TokenType::Color, .rule = Rule::Value, .slot = 2, .first = TokenKey::SurfaceTabstrip, .second = TokenKey::SurfaceTabstrip}, // surface-tabstrip
    KeyInfo{.name = "surface-raised", .type = TokenType::Color, .rule = Rule::Value, .slot = 3, .first = TokenKey::SurfaceRaised, .second = TokenKey::SurfaceRaised}, // surface-raised
    KeyInfo{.name = "surface-field", .type = TokenType::Color, .rule = Rule::Value, .slot = 4, .first = TokenKey::SurfaceField, .second = TokenKey::SurfaceField}, // surface-field
    KeyInfo{.name = "surface-control", .type = TokenType::Color, .rule = Rule::Value, .slot = 5, .first = TokenKey::SurfaceControl, .second = TokenKey::SurfaceControl}, // surface-control
    KeyInfo{.name = "surface-control-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 6, .first = TokenKey::SurfaceControlHover, .second = TokenKey::SurfaceControlHover}, // surface-control-hover
    KeyInfo{.name = "surface-control-pressed", .type = TokenType::Color, .rule = Rule::Value, .slot = 7, .first = TokenKey::SurfaceControlPressed, .second = TokenKey::SurfaceControlPressed}, // surface-control-pressed
    KeyInfo{.name = "surface-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 8, .first = TokenKey::SurfaceHover, .second = TokenKey::SurfaceHover}, // surface-hover
    KeyInfo{.name = "canvas-surround", .type = TokenType::Color, .rule = Rule::Value, .slot = 9, .first = TokenKey::CanvasSurround, .second = TokenKey::CanvasSurround}, // canvas-surround
    KeyInfo{.name = "ruler-surface", .type = TokenType::Color, .rule = Rule::Value, .slot = 10, .first = TokenKey::RulerSurface, .second = TokenKey::RulerSurface}, // ruler-surface
    KeyInfo{.name = "scrim", .type = TokenType::Color, .rule = Rule::Value, .slot = 11, .first = TokenKey::Scrim, .second = TokenKey::Scrim}, // scrim
    KeyInfo{.name = "divider", .type = TokenType::Color, .rule = Rule::Value, .slot = 12, .first = TokenKey::Divider, .second = TokenKey::Divider}, // divider
    KeyInfo{.name = "divider-strong", .type = TokenType::Color, .rule = Rule::Value, .slot = 13, .first = TokenKey::DividerStrong, .second = TokenKey::DividerStrong}, // divider-strong
    KeyInfo{.name = "border-control", .type = TokenType::Color, .rule = Rule::Value, .slot = 14, .first = TokenKey::BorderControl, .second = TokenKey::BorderControl}, // border-control
    KeyInfo{.name = "border-control-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 15, .first = TokenKey::BorderControlHover, .second = TokenKey::BorderControlHover}, // border-control-hover
    KeyInfo{.name = "border-popup", .type = TokenType::Color, .rule = Rule::Value, .slot = 16, .first = TokenKey::BorderPopup, .second = TokenKey::BorderPopup}, // border-popup
    KeyInfo{.name = "scroll-thumb", .type = TokenType::Color, .rule = Rule::Value, .slot = 17, .first = TokenKey::ScrollThumb, .second = TokenKey::ScrollThumb}, // scroll-thumb
    KeyInfo{.name = "scroll-thumb-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 18, .first = TokenKey::ScrollThumbHover, .second = TokenKey::ScrollThumbHover}, // scroll-thumb-hover
    KeyInfo{.name = "text-primary", .type = TokenType::Color, .rule = Rule::Value, .slot = 19, .first = TokenKey::TextPrimary, .second = TokenKey::TextPrimary}, // text-primary
    KeyInfo{.name = "text-secondary", .type = TokenType::Color, .rule = Rule::Value, .slot = 20, .first = TokenKey::TextSecondary, .second = TokenKey::TextSecondary}, // text-secondary
    KeyInfo{.name = "text-disabled", .type = TokenType::Color, .rule = Rule::Value, .slot = 21, .first = TokenKey::TextDisabled, .second = TokenKey::TextDisabled}, // text-disabled
    KeyInfo{.name = "text-placeholder", .type = TokenType::Color, .rule = Rule::Value, .slot = 22, .first = TokenKey::TextPlaceholder, .second = TokenKey::TextPlaceholder}, // text-placeholder
    KeyInfo{.name = "icon", .type = TokenType::Color, .rule = Rule::Alias, .slot = 0, .first = TokenKey::TextSecondary, .second = TokenKey::TextSecondary}, // icon
    KeyInfo{.name = "state", .type = TokenType::Color, .rule = Rule::Value, .slot = 23, .first = TokenKey::State, .second = TokenKey::State}, // state
    KeyInfo{.name = "state-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 24, .first = TokenKey::StateHover, .second = TokenKey::StateHover}, // state-hover
    KeyInfo{.name = "state-pressed", .type = TokenType::Color, .rule = Rule::Value, .slot = 25, .first = TokenKey::StatePressed, .second = TokenKey::StatePressed}, // state-pressed
    KeyInfo{.name = "state-on", .type = TokenType::Color, .rule = Rule::Value, .slot = 26, .first = TokenKey::StateOn, .second = TokenKey::StateOn}, // state-on
    KeyInfo{.name = "state-subtle", .type = TokenType::Color, .rule = Rule::Value, .slot = 27, .first = TokenKey::StateSubtle, .second = TokenKey::StateSubtle}, // state-subtle
    KeyInfo{.name = "state-tint", .type = TokenType::Color, .rule = Rule::Value, .slot = 28, .first = TokenKey::StateTint, .second = TokenKey::StateTint}, // state-tint
    KeyInfo{.name = "state-line", .type = TokenType::Color, .rule = Rule::Value, .slot = 29, .first = TokenKey::StateLine, .second = TokenKey::StateLine}, // state-line
    KeyInfo{.name = "state-text", .type = TokenType::Color, .rule = Rule::Value, .slot = 30, .first = TokenKey::StateText, .second = TokenKey::StateText}, // state-text
    KeyInfo{.name = "focus-ring", .type = TokenType::Color, .rule = Rule::Alias, .slot = 0, .first = TokenKey::StateLine, .second = TokenKey::StateLine}, // focus-ring
    KeyInfo{.name = "selection-inactive", .type = TokenType::Color, .rule = Rule::Value, .slot = 31, .first = TokenKey::SelectionInactive, .second = TokenKey::SelectionInactive}, // selection-inactive
    KeyInfo{.name = "state-orange", .type = TokenType::Color, .rule = Rule::Value, .slot = 32, .first = TokenKey::StateOrange, .second = TokenKey::StateOrange}, // state-orange
    KeyInfo{.name = "state-orange-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 33, .first = TokenKey::StateOrangeHover, .second = TokenKey::StateOrangeHover}, // state-orange-hover
    KeyInfo{.name = "state-orange-pressed", .type = TokenType::Color, .rule = Rule::Value, .slot = 34, .first = TokenKey::StateOrangePressed, .second = TokenKey::StateOrangePressed}, // state-orange-pressed
    KeyInfo{.name = "state-orange-on", .type = TokenType::Color, .rule = Rule::Value, .slot = 35, .first = TokenKey::StateOrangeOn, .second = TokenKey::StateOrangeOn}, // state-orange-on
    KeyInfo{.name = "state-orange-subtle", .type = TokenType::Color, .rule = Rule::Value, .slot = 36, .first = TokenKey::StateOrangeSubtle, .second = TokenKey::StateOrangeSubtle}, // state-orange-subtle
    KeyInfo{.name = "state-orange-tint", .type = TokenType::Color, .rule = Rule::Value, .slot = 37, .first = TokenKey::StateOrangeTint, .second = TokenKey::StateOrangeTint}, // state-orange-tint
    KeyInfo{.name = "state-orange-line", .type = TokenType::Color, .rule = Rule::Value, .slot = 38, .first = TokenKey::StateOrangeLine, .second = TokenKey::StateOrangeLine}, // state-orange-line
    KeyInfo{.name = "state-orange-text", .type = TokenType::Color, .rule = Rule::Value, .slot = 39, .first = TokenKey::StateOrangeText, .second = TokenKey::StateOrangeText}, // state-orange-text
    KeyInfo{.name = "accent-stilus", .type = TokenType::Color, .rule = Rule::Value, .slot = 40, .first = TokenKey::AccentStilus, .second = TokenKey::AccentStilus}, // accent-stilus
    KeyInfo{.name = "accent-stilus-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 41, .first = TokenKey::AccentStilusHover, .second = TokenKey::AccentStilusHover}, // accent-stilus-hover
    KeyInfo{.name = "accent-stilus-on", .type = TokenType::Color, .rule = Rule::Value, .slot = 42, .first = TokenKey::AccentStilusOn, .second = TokenKey::AccentStilusOn}, // accent-stilus-on
    KeyInfo{.name = "accent-gesso", .type = TokenType::Color, .rule = Rule::Value, .slot = 43, .first = TokenKey::AccentGesso, .second = TokenKey::AccentGesso}, // accent-gesso
    KeyInfo{.name = "accent-gesso-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 44, .first = TokenKey::AccentGessoHover, .second = TokenKey::AccentGessoHover}, // accent-gesso-hover
    KeyInfo{.name = "accent-gesso-on", .type = TokenType::Color, .rule = Rule::Value, .slot = 45, .first = TokenKey::AccentGessoOn, .second = TokenKey::AccentGessoOn}, // accent-gesso-on
    KeyInfo{.name = "accent-albumen", .type = TokenType::Color, .rule = Rule::Value, .slot = 46, .first = TokenKey::AccentAlbumen, .second = TokenKey::AccentAlbumen}, // accent-albumen
    KeyInfo{.name = "accent-albumen-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 47, .first = TokenKey::AccentAlbumenHover, .second = TokenKey::AccentAlbumenHover}, // accent-albumen-hover
    KeyInfo{.name = "accent-albumen-on", .type = TokenType::Color, .rule = Rule::Value, .slot = 48, .first = TokenKey::AccentAlbumenOn, .second = TokenKey::AccentAlbumenOn}, // accent-albumen-on
    KeyInfo{.name = "status-error", .type = TokenType::Color, .rule = Rule::Value, .slot = 49, .first = TokenKey::StatusError, .second = TokenKey::StatusError}, // status-error
    KeyInfo{.name = "status-error-subtle", .type = TokenType::Color, .rule = Rule::Value, .slot = 50, .first = TokenKey::StatusErrorSubtle, .second = TokenKey::StatusErrorSubtle}, // status-error-subtle
    KeyInfo{.name = "status-warning", .type = TokenType::Color, .rule = Rule::Value, .slot = 51, .first = TokenKey::StatusWarning, .second = TokenKey::StatusWarning}, // status-warning
    KeyInfo{.name = "status-warning-subtle", .type = TokenType::Color, .rule = Rule::Value, .slot = 52, .first = TokenKey::StatusWarningSubtle, .second = TokenKey::StatusWarningSubtle}, // status-warning-subtle
    KeyInfo{.name = "status-success", .type = TokenType::Color, .rule = Rule::Value, .slot = 53, .first = TokenKey::StatusSuccess, .second = TokenKey::StatusSuccess}, // status-success
    KeyInfo{.name = "status-success-subtle", .type = TokenType::Color, .rule = Rule::Value, .slot = 54, .first = TokenKey::StatusSuccessSubtle, .second = TokenKey::StatusSuccessSubtle}, // status-success-subtle
    KeyInfo{.name = "status-info", .type = TokenType::Color, .rule = Rule::Value, .slot = 55, .first = TokenKey::StatusInfo, .second = TokenKey::StatusInfo}, // status-info
    KeyInfo{.name = "status-info-subtle", .type = TokenType::Color, .rule = Rule::Value, .slot = 56, .first = TokenKey::StatusInfoSubtle, .second = TokenKey::StatusInfoSubtle}, // status-info-subtle
    KeyInfo{.name = "caption-close-hover", .type = TokenType::Color, .rule = Rule::Value, .slot = 57, .first = TokenKey::CaptionCloseHover, .second = TokenKey::CaptionCloseHover}, // caption-close-hover
    KeyInfo{.name = "caption-close-pressed", .type = TokenType::Color, .rule = Rule::Value, .slot = 58, .first = TokenKey::CaptionClosePressed, .second = TokenKey::CaptionClosePressed}, // caption-close-pressed
    KeyInfo{.name = "caption-close-on", .type = TokenType::Color, .rule = Rule::Value, .slot = 59, .first = TokenKey::CaptionCloseOn, .second = TokenKey::CaptionCloseOn}, // caption-close-on
    KeyInfo{.name = "checker-light", .type = TokenType::Color, .rule = Rule::Value, .slot = 60, .first = TokenKey::CheckerLight, .second = TokenKey::CheckerLight}, // checker-light
    KeyInfo{.name = "checker-dark", .type = TokenType::Color, .rule = Rule::Value, .slot = 61, .first = TokenKey::CheckerDark, .second = TokenKey::CheckerDark}, // checker-dark
    KeyInfo{.name = "guide", .type = TokenType::Color, .rule = Rule::Value, .slot = 62, .first = TokenKey::Guide, .second = TokenKey::Guide}, // guide
    KeyInfo{.name = "guide-smart", .type = TokenType::Color, .rule = Rule::Value, .slot = 63, .first = TokenKey::GuideSmart, .second = TokenKey::GuideSmart}, // guide-smart
    KeyInfo{.name = "ants-light", .type = TokenType::Color, .rule = Rule::Value, .slot = 64, .first = TokenKey::AntsLight, .second = TokenKey::AntsLight}, // ants-light
    KeyInfo{.name = "ants-dark", .type = TokenType::Color, .rule = Rule::Value, .slot = 65, .first = TokenKey::AntsDark, .second = TokenKey::AntsDark}, // ants-dark
    KeyInfo{.name = "handle-fill", .type = TokenType::Color, .rule = Rule::Value, .slot = 66, .first = TokenKey::HandleFill, .second = TokenKey::HandleFill}, // handle-fill
    KeyInfo{.name = "handle-stroke", .type = TokenType::Color, .rule = Rule::Alias, .slot = 0, .first = TokenKey::State, .second = TokenKey::State}, // handle-stroke
    KeyInfo{.name = "artboard", .type = TokenType::Color, .rule = Rule::Value, .slot = 67, .first = TokenKey::Artboard, .second = TokenKey::Artboard}, // artboard
    KeyInfo{.name = "shadow-tooltip", .type = TokenType::Shadow, .rule = Rule::Value, .slot = 0, .first = TokenKey::ShadowTooltip, .second = TokenKey::ShadowTooltip}, // shadow-tooltip
    KeyInfo{.name = "shadow-popup", .type = TokenType::Shadow, .rule = Rule::Value, .slot = 1, .first = TokenKey::ShadowPopup, .second = TokenKey::ShadowPopup}, // shadow-popup
    KeyInfo{.name = "shadow-dialog", .type = TokenType::Shadow, .rule = Rule::Value, .slot = 2, .first = TokenKey::ShadowDialog, .second = TokenKey::ShadowDialog}, // shadow-dialog
    KeyInfo{.name = "glow-state", .type = TokenType::Shadow, .rule = Rule::Value, .slot = 3, .first = TokenKey::GlowState, .second = TokenKey::GlowState}, // glow-state
    KeyInfo{.name = "glow-state-orange", .type = TokenType::Shadow, .rule = Rule::Value, .slot = 4, .first = TokenKey::GlowStateOrange, .second = TokenKey::GlowStateOrange}, // glow-state-orange
    KeyInfo{.name = "space-hair", .type = TokenType::Size, .rule = Rule::Value, .slot = 0, .first = TokenKey::SpaceHair, .second = TokenKey::SpaceHair}, // space-hair
    KeyInfo{.name = "space-1", .type = TokenType::Size, .rule = Rule::Value, .slot = 1, .first = TokenKey::Space1, .second = TokenKey::Space1}, // space-1
    KeyInfo{.name = "space-1-5", .type = TokenType::Size, .rule = Rule::Value, .slot = 2, .first = TokenKey::Space15, .second = TokenKey::Space15}, // space-1-5
    KeyInfo{.name = "space-2", .type = TokenType::Size, .rule = Rule::Value, .slot = 3, .first = TokenKey::Space2, .second = TokenKey::Space2}, // space-2
    KeyInfo{.name = "space-3", .type = TokenType::Size, .rule = Rule::Value, .slot = 4, .first = TokenKey::Space3, .second = TokenKey::Space3}, // space-3
    KeyInfo{.name = "space-4", .type = TokenType::Size, .rule = Rule::Value, .slot = 5, .first = TokenKey::Space4, .second = TokenKey::Space4}, // space-4
    KeyInfo{.name = "space-6", .type = TokenType::Size, .rule = Rule::Value, .slot = 6, .first = TokenKey::Space6, .second = TokenKey::Space6}, // space-6
    KeyInfo{.name = "radius-sm", .type = TokenType::Size, .rule = Rule::Value, .slot = 7, .first = TokenKey::RadiusSm, .second = TokenKey::RadiusSm}, // radius-sm
    KeyInfo{.name = "radius-md", .type = TokenType::Size, .rule = Rule::Value, .slot = 8, .first = TokenKey::RadiusMd, .second = TokenKey::RadiusMd}, // radius-md
    KeyInfo{.name = "radius-lg", .type = TokenType::Size, .rule = Rule::Value, .slot = 9, .first = TokenKey::RadiusLg, .second = TokenKey::RadiusLg}, // radius-lg
    KeyInfo{.name = "radius-round", .type = TokenType::Size, .rule = Rule::Value, .slot = 10, .first = TokenKey::RadiusRound, .second = TokenKey::RadiusRound}, // radius-round
    KeyInfo{.name = "control-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 11, .first = TokenKey::ControlHCompact, .second = TokenKey::ControlHCompact}, // control-h-compact
    KeyInfo{.name = "control-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 12, .first = TokenKey::ControlHComfortable, .second = TokenKey::ControlHComfortable}, // control-h-comfortable
    KeyInfo{.name = "control-h-dialog", .type = TokenType::Size, .rule = Rule::Value, .slot = 13, .first = TokenKey::ControlHDialog, .second = TokenKey::ControlHDialog}, // control-h-dialog
    KeyInfo{.name = "titlebar-h", .type = TokenType::Size, .rule = Rule::Value, .slot = 14, .first = TokenKey::TitlebarH, .second = TokenKey::TitlebarH}, // titlebar-h
    KeyInfo{.name = "caption-button-w", .type = TokenType::Size, .rule = Rule::Value, .slot = 15, .first = TokenKey::CaptionButtonW, .second = TokenKey::CaptionButtonW}, // caption-button-w
    KeyInfo{.name = "menu-row-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 16, .first = TokenKey::MenuRowHCompact, .second = TokenKey::MenuRowHCompact}, // menu-row-h-compact
    KeyInfo{.name = "menu-row-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 17, .first = TokenKey::MenuRowHComfortable, .second = TokenKey::MenuRowHComfortable}, // menu-row-h-comfortable
    KeyInfo{.name = "menu-w-min", .type = TokenType::Size, .rule = Rule::Value, .slot = 18, .first = TokenKey::MenuWMin, .second = TokenKey::MenuWMin}, // menu-w-min
    KeyInfo{.name = "optionsbar-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 19, .first = TokenKey::OptionsbarHCompact, .second = TokenKey::OptionsbarHCompact}, // optionsbar-h-compact
    KeyInfo{.name = "optionsbar-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 20, .first = TokenKey::OptionsbarHComfortable, .second = TokenKey::OptionsbarHComfortable}, // optionsbar-h-comfortable
    KeyInfo{.name = "infobar-h", .type = TokenType::Size, .rule = Rule::Value, .slot = 21, .first = TokenKey::InfobarH, .second = TokenKey::InfobarH}, // infobar-h
    KeyInfo{.name = "doctab-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 22, .first = TokenKey::DoctabHCompact, .second = TokenKey::DoctabHCompact}, // doctab-h-compact
    KeyInfo{.name = "doctab-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 23, .first = TokenKey::DoctabHComfortable, .second = TokenKey::DoctabHComfortable}, // doctab-h-comfortable
    KeyInfo{.name = "doctab-w-max", .type = TokenType::Size, .rule = Rule::Value, .slot = 24, .first = TokenKey::DoctabWMax, .second = TokenKey::DoctabWMax}, // doctab-w-max
    KeyInfo{.name = "tool-button-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 25, .first = TokenKey::ToolButtonCompact, .second = TokenKey::ToolButtonCompact}, // tool-button-compact
    KeyInfo{.name = "tool-button-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 26, .first = TokenKey::ToolButtonComfortable, .second = TokenKey::ToolButtonComfortable}, // tool-button-comfortable
    KeyInfo{.name = "toolrail-w-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 27, .first = TokenKey::ToolrailWCompact, .second = TokenKey::ToolrailWCompact}, // toolrail-w-compact
    KeyInfo{.name = "toolrail-w-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 28, .first = TokenKey::ToolrailWComfortable, .second = TokenKey::ToolrailWComfortable}, // toolrail-w-comfortable
    KeyInfo{.name = "panel-w-min", .type = TokenType::Size, .rule = Rule::Value, .slot = 29, .first = TokenKey::PanelWMin, .second = TokenKey::PanelWMin}, // panel-w-min
    KeyInfo{.name = "panel-w-default", .type = TokenType::Size, .rule = Rule::Value, .slot = 30, .first = TokenKey::PanelWDefault, .second = TokenKey::PanelWDefault}, // panel-w-default
    KeyInfo{.name = "panel-w-max", .type = TokenType::Size, .rule = Rule::Value, .slot = 31, .first = TokenKey::PanelWMax, .second = TokenKey::PanelWMax}, // panel-w-max
    KeyInfo{.name = "panel-tab-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 32, .first = TokenKey::PanelTabHCompact, .second = TokenKey::PanelTabHCompact}, // panel-tab-h-compact
    KeyInfo{.name = "panel-tab-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 33, .first = TokenKey::PanelTabHComfortable, .second = TokenKey::PanelTabHComfortable}, // panel-tab-h-comfortable
    KeyInfo{.name = "panel-iconstrip-w", .type = TokenType::Size, .rule = Rule::Value, .slot = 34, .first = TokenKey::PanelIconstripW, .second = TokenKey::PanelIconstripW}, // panel-iconstrip-w
    KeyInfo{.name = "section-header-h", .type = TokenType::Size, .rule = Rule::Value, .slot = 35, .first = TokenKey::SectionHeaderH, .second = TokenKey::SectionHeaderH}, // section-header-h
    KeyInfo{.name = "row-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 36, .first = TokenKey::RowHCompact, .second = TokenKey::RowHCompact}, // row-h-compact
    KeyInfo{.name = "row-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 37, .first = TokenKey::RowHComfortable, .second = TokenKey::RowHComfortable}, // row-h-comfortable
    KeyInfo{.name = "layer-row-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 38, .first = TokenKey::LayerRowHCompact, .second = TokenKey::LayerRowHCompact}, // layer-row-h-compact
    KeyInfo{.name = "layer-row-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 39, .first = TokenKey::LayerRowHComfortable, .second = TokenKey::LayerRowHComfortable}, // layer-row-h-comfortable
    KeyInfo{.name = "statusbar-h-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 40, .first = TokenKey::StatusbarHCompact, .second = TokenKey::StatusbarHCompact}, // statusbar-h-compact
    KeyInfo{.name = "statusbar-h-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 41, .first = TokenKey::StatusbarHComfortable, .second = TokenKey::StatusbarHComfortable}, // statusbar-h-comfortable
    KeyInfo{.name = "ruler-w", .type = TokenType::Size, .rule = Rule::Value, .slot = 42, .first = TokenKey::RulerW, .second = TokenKey::RulerW}, // ruler-w
    KeyInfo{.name = "icon-sm", .type = TokenType::Size, .rule = Rule::Value, .slot = 43, .first = TokenKey::IconSm, .second = TokenKey::IconSm}, // icon-sm
    KeyInfo{.name = "icon-md", .type = TokenType::Size, .rule = Rule::Value, .slot = 44, .first = TokenKey::IconMd, .second = TokenKey::IconMd}, // icon-md
    KeyInfo{.name = "icon-stroke", .type = TokenType::Size, .rule = Rule::Value, .slot = 45, .first = TokenKey::IconStroke, .second = TokenKey::IconStroke}, // icon-stroke
    KeyInfo{.name = "check-size-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 46, .first = TokenKey::CheckSizeCompact, .second = TokenKey::CheckSizeCompact}, // check-size-compact
    KeyInfo{.name = "check-size-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 47, .first = TokenKey::CheckSizeComfortable, .second = TokenKey::CheckSizeComfortable}, // check-size-comfortable
    KeyInfo{.name = "toggle-w", .type = TokenType::Size, .rule = Rule::Value, .slot = 48, .first = TokenKey::ToggleW, .second = TokenKey::ToggleW}, // toggle-w
    KeyInfo{.name = "slider-track-h", .type = TokenType::Size, .rule = Rule::Value, .slot = 49, .first = TokenKey::SliderTrackH, .second = TokenKey::SliderTrackH}, // slider-track-h
    KeyInfo{.name = "slider-thumb", .type = TokenType::Size, .rule = Rule::Value, .slot = 50, .first = TokenKey::SliderThumb, .second = TokenKey::SliderThumb}, // slider-thumb
    KeyInfo{.name = "scrollbar-w-rest", .type = TokenType::Size, .rule = Rule::Value, .slot = 51, .first = TokenKey::ScrollbarWRest, .second = TokenKey::ScrollbarWRest}, // scrollbar-w-rest
    KeyInfo{.name = "scrollbar-w-hover", .type = TokenType::Size, .rule = Rule::Value, .slot = 52, .first = TokenKey::ScrollbarWHover, .second = TokenKey::ScrollbarWHover}, // scrollbar-w-hover
    KeyInfo{.name = "swatch-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 53, .first = TokenKey::SwatchCompact, .second = TokenKey::SwatchCompact}, // swatch-compact
    KeyInfo{.name = "swatch-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 54, .first = TokenKey::SwatchComfortable, .second = TokenKey::SwatchComfortable}, // swatch-comfortable
    KeyInfo{.name = "color-chip", .type = TokenType::Size, .rule = Rule::Value, .slot = 55, .first = TokenKey::ColorChip, .second = TokenKey::ColorChip}, // color-chip
    KeyInfo{.name = "focus-ring-w", .type = TokenType::Size, .rule = Rule::Value, .slot = 56, .first = TokenKey::FocusRingW, .second = TokenKey::FocusRingW}, // focus-ring-w
    KeyInfo{.name = "handle-size", .type = TokenType::Size, .rule = Rule::Value, .slot = 57, .first = TokenKey::HandleSize, .second = TokenKey::HandleSize}, // handle-size
    KeyInfo{.name = "checker-tile", .type = TokenType::Size, .rule = Rule::Value, .slot = 58, .first = TokenKey::CheckerTile, .second = TokenKey::CheckerTile}, // checker-tile
    KeyInfo{.name = "type-caption", .type = TokenType::Size, .rule = Rule::Value, .slot = 59, .first = TokenKey::TypeCaption, .second = TokenKey::TypeCaption}, // type-caption
    KeyInfo{.name = "type-body-compact", .type = TokenType::Size, .rule = Rule::Value, .slot = 60, .first = TokenKey::TypeBodyCompact, .second = TokenKey::TypeBodyCompact}, // type-body-compact
    KeyInfo{.name = "type-body-comfortable", .type = TokenType::Size, .rule = Rule::Value, .slot = 61, .first = TokenKey::TypeBodyComfortable, .second = TokenKey::TypeBodyComfortable}, // type-body-comfortable
    KeyInfo{.name = "type-title", .type = TokenType::Size, .rule = Rule::Value, .slot = 62, .first = TokenKey::TypeTitle, .second = TokenKey::TypeTitle}, // type-title
    KeyInfo{.name = "duration-fast", .type = TokenType::Duration, .rule = Rule::Value, .slot = 0, .first = TokenKey::DurationFast, .second = TokenKey::DurationFast}, // duration-fast
    KeyInfo{.name = "duration-standard", .type = TokenType::Duration, .rule = Rule::Value, .slot = 1, .first = TokenKey::DurationStandard, .second = TokenKey::DurationStandard}, // duration-standard
    KeyInfo{.name = "duration-slow", .type = TokenType::Duration, .rule = Rule::Value, .slot = 2, .first = TokenKey::DurationSlow, .second = TokenKey::DurationSlow}, // duration-slow
    KeyInfo{.name = "tooltip-delay", .type = TokenType::Duration, .rule = Rule::Value, .slot = 3, .first = TokenKey::TooltipDelay, .second = TokenKey::TooltipDelay}, // tooltip-delay
    KeyInfo{.name = "ease-out", .type = TokenType::Easing, .rule = Rule::Value, .slot = 0, .first = TokenKey::EaseOut, .second = TokenKey::EaseOut}, // ease-out
    KeyInfo{.name = "caption", .type = TokenType::TypeStyle, .rule = Rule::Density, .slot = 0, .first = TokenKey::CaptionCompact, .second = TokenKey::CaptionComfortable}, // caption
    KeyInfo{.name = "body", .type = TokenType::TypeStyle, .rule = Rule::Density, .slot = 0, .first = TokenKey::BodyCompact, .second = TokenKey::BodyComfortable}, // body
    KeyInfo{.name = "body-strong", .type = TokenType::TypeStyle, .rule = Rule::Density, .slot = 0, .first = TokenKey::BodyStrongCompact, .second = TokenKey::BodyStrongComfortable}, // body-strong
    KeyInfo{.name = "section-header", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 3, .first = TokenKey::SectionHeader, .second = TokenKey::SectionHeader}, // section-header
    KeyInfo{.name = "title", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 4, .first = TokenKey::Title, .second = TokenKey::Title}, // title
    KeyInfo{.name = "dialog-title", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 5, .first = TokenKey::DialogTitle, .second = TokenKey::DialogTitle}, // dialog-title
    KeyInfo{.name = "caption-comfortable", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 6, .first = TokenKey::CaptionComfortable, .second = TokenKey::CaptionComfortable}, // caption-comfortable
    KeyInfo{.name = "body-comfortable", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 7, .first = TokenKey::BodyComfortable, .second = TokenKey::BodyComfortable}, // body-comfortable
    KeyInfo{.name = "body-strong-comfortable", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 8, .first = TokenKey::BodyStrongComfortable, .second = TokenKey::BodyStrongComfortable}, // body-strong-comfortable
    KeyInfo{.name = "display", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 9, .first = TokenKey::Display, .second = TokenKey::Display}, // display
    KeyInfo{.name = "mono", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 10, .first = TokenKey::Mono, .second = TokenKey::Mono}, // mono
    KeyInfo{.name = "mono-body", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 11, .first = TokenKey::MonoBody, .second = TokenKey::MonoBody}, // mono-body
    KeyInfo{.name = "control-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::ControlHCompact, .second = TokenKey::ControlHComfortable}, // control-h
    KeyInfo{.name = "menu-row-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::MenuRowHCompact, .second = TokenKey::MenuRowHComfortable}, // menu-row-h
    KeyInfo{.name = "optionsbar-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::OptionsbarHCompact, .second = TokenKey::OptionsbarHComfortable}, // optionsbar-h
    KeyInfo{.name = "doctab-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::DoctabHCompact, .second = TokenKey::DoctabHComfortable}, // doctab-h
    KeyInfo{.name = "tool-button", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::ToolButtonCompact, .second = TokenKey::ToolButtonComfortable}, // tool-button
    KeyInfo{.name = "toolrail-w", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::ToolrailWCompact, .second = TokenKey::ToolrailWComfortable}, // toolrail-w
    KeyInfo{.name = "panel-tab-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::PanelTabHCompact, .second = TokenKey::PanelTabHComfortable}, // panel-tab-h
    KeyInfo{.name = "row-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::RowHCompact, .second = TokenKey::RowHComfortable}, // row-h
    KeyInfo{.name = "layer-row-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::LayerRowHCompact, .second = TokenKey::LayerRowHComfortable}, // layer-row-h
    KeyInfo{.name = "statusbar-h", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::StatusbarHCompact, .second = TokenKey::StatusbarHComfortable}, // statusbar-h
    KeyInfo{.name = "check-size", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::CheckSizeCompact, .second = TokenKey::CheckSizeComfortable}, // check-size
    KeyInfo{.name = "swatch", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::SwatchCompact, .second = TokenKey::SwatchComfortable}, // swatch
    KeyInfo{.name = "type-body", .type = TokenType::Size, .rule = Rule::Density, .slot = 0, .first = TokenKey::TypeBodyCompact, .second = TokenKey::TypeBodyComfortable}, // type-body
    KeyInfo{.name = "caption-compact", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 0, .first = TokenKey::CaptionCompact, .second = TokenKey::CaptionCompact}, // caption-compact
    KeyInfo{.name = "body-compact", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 1, .first = TokenKey::BodyCompact, .second = TokenKey::BodyCompact}, // body-compact
    KeyInfo{.name = "body-strong-compact", .type = TokenType::TypeStyle, .rule = Rule::Value, .slot = 2, .first = TokenKey::BodyStrongCompact, .second = TokenKey::BodyStrongCompact}, // body-strong-compact
}};

const std::array<std::array<Color, kColorCount>, kBrightnessCount> kColors{{
    {{ // Dark
        Color{.red = 40, .green = 40, .blue = 40, .alpha = 255}, // frame (dark)
        Color{.red = 50, .green = 50, .blue = 50, .alpha = 255}, // surface-panel (dark)
        Color{.red = 43, .green = 43, .blue = 43, .alpha = 255}, // surface-tabstrip (dark)
        Color{.red = 58, .green = 58, .blue = 58, .alpha = 255}, // surface-raised (dark)
        Color{.red = 38, .green = 38, .blue = 38, .alpha = 255}, // surface-field (dark)
        Color{.red = 69, .green = 69, .blue = 69, .alpha = 255}, // surface-control (dark)
        Color{.red = 80, .green = 80, .blue = 80, .alpha = 255}, // surface-control-hover (dark)
        Color{.red = 42, .green = 42, .blue = 42, .alpha = 255}, // surface-control-pressed (dark)
        Color{.red = 61, .green = 61, .blue = 61, .alpha = 255}, // surface-hover (dark)
        Color{.red = 30, .green = 30, .blue = 30, .alpha = 255}, // canvas-surround (dark)
        Color{.red = 43, .green = 43, .blue = 43, .alpha = 255}, // ruler-surface (dark)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 153}, // scrim (dark)
        Color{.red = 62, .green = 62, .blue = 62, .alpha = 255}, // divider (dark)
        Color{.red = 74, .green = 74, .blue = 74, .alpha = 255}, // divider-strong (dark)
        Color{.red = 133, .green = 133, .blue = 133, .alpha = 255}, // border-control (dark)
        Color{.red = 154, .green = 154, .blue = 154, .alpha = 255}, // border-control-hover (dark)
        Color{.red = 85, .green = 85, .blue = 85, .alpha = 255}, // border-popup (dark)
        Color{.red = 94, .green = 94, .blue = 94, .alpha = 255}, // scroll-thumb (dark)
        Color{.red = 138, .green = 138, .blue = 138, .alpha = 255}, // scroll-thumb-hover (dark)
        Color{.red = 227, .green = 227, .blue = 227, .alpha = 255}, // text-primary (dark)
        Color{.red = 176, .green = 176, .blue = 176, .alpha = 255}, // text-secondary (dark)
        Color{.red = 111, .green = 111, .blue = 111, .alpha = 255}, // text-disabled (dark)
        Color{.red = 140, .green = 140, .blue = 140, .alpha = 255}, // text-placeholder (dark)
        Color{.red = 20, .green = 115, .blue = 230, .alpha = 255}, // state (dark)
        Color{.red = 13, .green = 102, .blue = 208, .alpha = 255}, // state-hover (dark)
        Color{.red = 10, .green = 87, .blue = 180, .alpha = 255}, // state-pressed (dark)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // state-on (dark)
        Color{.red = 37, .green = 65, .blue = 95, .alpha = 255}, // state-subtle (dark)
        Color{.red = 20, .green = 115, .blue = 230, .alpha = 51}, // state-tint (dark)
        Color{.red = 86, .green = 165, .blue = 255, .alpha = 255}, // state-line (dark)
        Color{.red = 90, .green = 171, .blue = 255, .alpha = 255}, // state-text (dark)
        Color{.red = 70, .green = 70, .blue = 70, .alpha = 255}, // selection-inactive (dark)
        Color{.red = 255, .green = 107, .blue = 53, .alpha = 255}, // state-orange (dark)
        Color{.red = 255, .green = 130, .blue = 79, .alpha = 255}, // state-orange-hover (dark)
        Color{.red = 232, .green = 90, .blue = 36, .alpha = 255}, // state-orange-pressed (dark)
        Color{.red = 20, .green = 20, .blue = 20, .alpha = 255}, // state-orange-on (dark)
        Color{.red = 90, .green = 53, .blue = 37, .alpha = 255}, // state-orange-subtle (dark)
        Color{.red = 255, .green = 107, .blue = 53, .alpha = 41}, // state-orange-tint (dark)
        Color{.red = 255, .green = 122, .blue = 71, .alpha = 255}, // state-orange-line (dark)
        Color{.red = 255, .green = 138, .blue = 92, .alpha = 255}, // state-orange-text (dark)
        Color{.red = 41, .green = 197, .blue = 230, .alpha = 255}, // accent-stilus (dark)
        Color{.red = 82, .green = 210, .blue = 237, .alpha = 255}, // accent-stilus-hover (dark)
        Color{.red = 15, .green = 20, .blue = 22, .alpha = 255}, // accent-stilus-on (dark)
        Color{.red = 245, .green = 146, .blue = 62, .alpha = 255}, // accent-gesso (dark)
        Color{.red = 247, .green = 166, .blue = 96, .alpha = 255}, // accent-gesso-hover (dark)
        Color{.red = 26, .green = 20, .blue = 16, .alpha = 255}, // accent-gesso-on (dark)
        Color{.red = 76, .green = 196, .blue = 122, .alpha = 255}, // accent-albumen (dark)
        Color{.red = 110, .green = 208, .blue = 146, .alpha = 255}, // accent-albumen-hover (dark)
        Color{.red = 15, .green = 22, .blue = 18, .alpha = 255}, // accent-albumen-on (dark)
        Color{.red = 255, .green = 123, .blue = 114, .alpha = 255}, // status-error (dark)
        Color{.red = 74, .green = 40, .blue = 38, .alpha = 255}, // status-error-subtle (dark)
        Color{.red = 242, .green = 193, .blue = 78, .alpha = 255}, // status-warning (dark)
        Color{.red = 70, .green = 60, .blue = 34, .alpha = 255}, // status-warning-subtle (dark)
        Color{.red = 95, .green = 208, .blue = 138, .alpha = 255}, // status-success (dark)
        Color{.red = 35, .green = 63, .blue = 46, .alpha = 255}, // status-success-subtle (dark)
        Color{.red = 108, .green = 180, .blue = 255, .alpha = 255}, // status-info (dark)
        Color{.red = 35, .green = 58, .blue = 84, .alpha = 255}, // status-info-subtle (dark)
        Color{.red = 196, .green = 43, .blue = 28, .alpha = 255}, // caption-close-hover (dark)
        Color{.red = 178, .green = 42, .blue = 27, .alpha = 255}, // caption-close-pressed (dark)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // caption-close-on (dark)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // checker-light (dark)
        Color{.red = 204, .green = 204, .blue = 204, .alpha = 255}, // checker-dark (dark)
        Color{.red = 0, .green = 200, .blue = 255, .alpha = 255}, // guide (dark)
        Color{.red = 255, .green = 61, .blue = 220, .alpha = 255}, // guide-smart (dark)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // ants-light (dark)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 255}, // ants-dark (dark)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // handle-fill (dark)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // artboard (dark)
    }},
    {{ // Darkest
        Color{.red = 21, .green = 21, .blue = 21, .alpha = 255}, // frame (darkest)
        Color{.red = 30, .green = 30, .blue = 30, .alpha = 255}, // surface-panel (darkest)
        Color{.red = 25, .green = 25, .blue = 25, .alpha = 255}, // surface-tabstrip (darkest)
        Color{.red = 38, .green = 38, .blue = 38, .alpha = 255}, // surface-raised (darkest)
        Color{.red = 18, .green = 18, .blue = 18, .alpha = 255}, // surface-field (darkest)
        Color{.red = 46, .green = 46, .blue = 46, .alpha = 255}, // surface-control (darkest)
        Color{.red = 56, .green = 56, .blue = 56, .alpha = 255}, // surface-control-hover (darkest)
        Color{.red = 23, .green = 23, .blue = 23, .alpha = 255}, // surface-control-pressed (darkest)
        Color{.red = 40, .green = 40, .blue = 40, .alpha = 255}, // surface-hover (darkest)
        Color{.red = 16, .green = 16, .blue = 16, .alpha = 255}, // canvas-surround (darkest)
        Color{.red = 24, .green = 24, .blue = 24, .alpha = 255}, // ruler-surface (darkest)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 166}, // scrim (darkest)
        Color{.red = 42, .green = 42, .blue = 42, .alpha = 255}, // divider (darkest)
        Color{.red = 54, .green = 54, .blue = 54, .alpha = 255}, // divider-strong (darkest)
        Color{.red = 112, .green = 112, .blue = 112, .alpha = 255}, // border-control (darkest)
        Color{.red = 138, .green = 138, .blue = 138, .alpha = 255}, // border-control-hover (darkest)
        Color{.red = 60, .green = 60, .blue = 60, .alpha = 255}, // border-popup (darkest)
        Color{.red = 74, .green = 74, .blue = 74, .alpha = 255}, // scroll-thumb (darkest)
        Color{.red = 116, .green = 116, .blue = 116, .alpha = 255}, // scroll-thumb-hover (darkest)
        Color{.red = 220, .green = 220, .blue = 220, .alpha = 255}, // text-primary (darkest)
        Color{.red = 166, .green = 166, .blue = 166, .alpha = 255}, // text-secondary (darkest)
        Color{.red = 89, .green = 89, .blue = 89, .alpha = 255}, // text-disabled (darkest)
        Color{.red = 126, .green = 126, .blue = 126, .alpha = 255}, // text-placeholder (darkest)
        Color{.red = 20, .green = 115, .blue = 230, .alpha = 255}, // state (darkest)
        Color{.red = 13, .green = 102, .blue = 208, .alpha = 255}, // state-hover (darkest)
        Color{.red = 10, .green = 87, .blue = 180, .alpha = 255}, // state-pressed (darkest)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // state-on (darkest)
        Color{.red = 29, .green = 53, .blue = 83, .alpha = 255}, // state-subtle (darkest)
        Color{.red = 20, .green = 115, .blue = 230, .alpha = 64}, // state-tint (darkest)
        Color{.red = 61, .green = 143, .blue = 240, .alpha = 255}, // state-line (darkest)
        Color{.red = 77, .green = 157, .blue = 250, .alpha = 255}, // state-text (darkest)
        Color{.red = 48, .green = 48, .blue = 48, .alpha = 255}, // selection-inactive (darkest)
        Color{.red = 255, .green = 107, .blue = 53, .alpha = 255}, // state-orange (darkest)
        Color{.red = 255, .green = 130, .blue = 79, .alpha = 255}, // state-orange-hover (darkest)
        Color{.red = 232, .green = 90, .blue = 36, .alpha = 255}, // state-orange-pressed (darkest)
        Color{.red = 20, .green = 20, .blue = 20, .alpha = 255}, // state-orange-on (darkest)
        Color{.red = 68, .green = 38, .blue = 26, .alpha = 255}, // state-orange-subtle (darkest)
        Color{.red = 255, .green = 107, .blue = 53, .alpha = 51}, // state-orange-tint (darkest)
        Color{.red = 255, .green = 107, .blue = 53, .alpha = 255}, // state-orange-line (darkest)
        Color{.red = 255, .green = 122, .blue = 71, .alpha = 255}, // state-orange-text (darkest)
        Color{.red = 41, .green = 197, .blue = 230, .alpha = 255}, // accent-stilus (darkest)
        Color{.red = 82, .green = 210, .blue = 237, .alpha = 255}, // accent-stilus-hover (darkest)
        Color{.red = 15, .green = 20, .blue = 22, .alpha = 255}, // accent-stilus-on (darkest)
        Color{.red = 245, .green = 146, .blue = 62, .alpha = 255}, // accent-gesso (darkest)
        Color{.red = 247, .green = 166, .blue = 96, .alpha = 255}, // accent-gesso-hover (darkest)
        Color{.red = 26, .green = 20, .blue = 16, .alpha = 255}, // accent-gesso-on (darkest)
        Color{.red = 76, .green = 196, .blue = 122, .alpha = 255}, // accent-albumen (darkest)
        Color{.red = 110, .green = 208, .blue = 146, .alpha = 255}, // accent-albumen-hover (darkest)
        Color{.red = 15, .green = 22, .blue = 18, .alpha = 255}, // accent-albumen-on (darkest)
        Color{.red = 255, .green = 110, .blue = 100, .alpha = 255}, // status-error (darkest)
        Color{.red = 58, .green = 29, .blue = 27, .alpha = 255}, // status-error-subtle (darkest)
        Color{.red = 240, .green = 185, .blue = 58, .alpha = 255}, // status-warning (darkest)
        Color{.red = 53, .green = 44, .blue = 21, .alpha = 255}, // status-warning-subtle (darkest)
        Color{.red = 82, .green = 198, .blue = 126, .alpha = 255}, // status-success (darkest)
        Color{.red = 22, .green = 48, .blue = 31, .alpha = 255}, // status-success-subtle (darkest)
        Color{.red = 90, .green = 168, .blue = 255, .alpha = 255}, // status-info (darkest)
        Color{.red = 23, .green = 42, .blue = 64, .alpha = 255}, // status-info-subtle (darkest)
        Color{.red = 196, .green = 43, .blue = 28, .alpha = 255}, // caption-close-hover (darkest)
        Color{.red = 178, .green = 42, .blue = 27, .alpha = 255}, // caption-close-pressed (darkest)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // caption-close-on (darkest)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // checker-light (darkest)
        Color{.red = 204, .green = 204, .blue = 204, .alpha = 255}, // checker-dark (darkest)
        Color{.red = 0, .green = 200, .blue = 255, .alpha = 255}, // guide (darkest)
        Color{.red = 255, .green = 61, .blue = 220, .alpha = 255}, // guide-smart (darkest)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // ants-light (darkest)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 255}, // ants-dark (darkest)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // handle-fill (darkest)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // artboard (darkest)
    }},
    {{ // MediumGray
        Color{.red = 69, .green = 69, .blue = 69, .alpha = 255}, // frame (medium)
        Color{.red = 83, .green = 83, .blue = 83, .alpha = 255}, // surface-panel (medium)
        Color{.red = 74, .green = 74, .blue = 74, .alpha = 255}, // surface-tabstrip (medium)
        Color{.red = 76, .green = 76, .blue = 76, .alpha = 255}, // surface-raised (medium)
        Color{.red = 62, .green = 62, .blue = 62, .alpha = 255}, // surface-field (medium)
        Color{.red = 100, .green = 100, .blue = 100, .alpha = 255}, // surface-control (medium)
        Color{.red = 108, .green = 108, .blue = 108, .alpha = 255}, // surface-control-hover (medium)
        Color{.red = 71, .green = 71, .blue = 71, .alpha = 255}, // surface-control-pressed (medium)
        Color{.red = 92, .green = 92, .blue = 92, .alpha = 255}, // surface-hover (medium)
        Color{.red = 59, .green = 59, .blue = 59, .alpha = 255}, // canvas-surround (medium)
        Color{.red = 74, .green = 74, .blue = 74, .alpha = 255}, // ruler-surface (medium)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 140}, // scrim (medium)
        Color{.red = 98, .green = 98, .blue = 98, .alpha = 255}, // divider (medium)
        Color{.red = 110, .green = 110, .blue = 110, .alpha = 255}, // divider-strong (medium)
        Color{.red = 163, .green = 163, .blue = 163, .alpha = 255}, // border-control (medium)
        Color{.red = 189, .green = 189, .blue = 189, .alpha = 255}, // border-control-hover (medium)
        Color{.red = 111, .green = 111, .blue = 111, .alpha = 255}, // border-popup (medium)
        Color{.red = 124, .green = 124, .blue = 124, .alpha = 255}, // scroll-thumb (medium)
        Color{.red = 166, .green = 166, .blue = 166, .alpha = 255}, // scroll-thumb-hover (medium)
        Color{.red = 245, .green = 245, .blue = 245, .alpha = 255}, // text-primary (medium)
        Color{.red = 218, .green = 218, .blue = 218, .alpha = 255}, // text-secondary (medium)
        Color{.red = 140, .green = 140, .blue = 140, .alpha = 255}, // text-disabled (medium)
        Color{.red = 184, .green = 184, .blue = 184, .alpha = 255}, // text-placeholder (medium)
        Color{.red = 18, .green = 103, .blue = 208, .alpha = 255}, // state (medium)
        Color{.red = 15, .green = 95, .blue = 192, .alpha = 255}, // state-hover (medium)
        Color{.red = 11, .green = 82, .blue = 168, .alpha = 255}, // state-pressed (medium)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // state-on (medium)
        Color{.red = 58, .green = 95, .blue = 140, .alpha = 255}, // state-subtle (medium)
        Color{.red = 20, .green = 115, .blue = 230, .alpha = 64}, // state-tint (medium)
        Color{.red = 159, .green = 205, .blue = 255, .alpha = 255}, // state-line (medium)
        Color{.red = 169, .green = 211, .blue = 255, .alpha = 255}, // state-text (medium)
        Color{.red = 102, .green = 102, .blue = 102, .alpha = 255}, // selection-inactive (medium)
        Color{.red = 255, .green = 122, .blue = 71, .alpha = 255}, // state-orange (medium)
        Color{.red = 255, .green = 143, .blue = 96, .alpha = 255}, // state-orange-hover (medium)
        Color{.red = 240, .green = 106, .blue = 54, .alpha = 255}, // state-orange-pressed (medium)
        Color{.red = 20, .green = 20, .blue = 20, .alpha = 255}, // state-orange-on (medium)
        Color{.red = 122, .green = 74, .blue = 54, .alpha = 255}, // state-orange-subtle (medium)
        Color{.red = 255, .green = 107, .blue = 53, .alpha = 56}, // state-orange-tint (medium)
        Color{.red = 255, .green = 184, .blue = 153, .alpha = 255}, // state-orange-line (medium)
        Color{.red = 255, .green = 194, .blue = 168, .alpha = 255}, // state-orange-text (medium)
        Color{.red = 41, .green = 197, .blue = 230, .alpha = 255}, // accent-stilus (medium)
        Color{.red = 82, .green = 210, .blue = 237, .alpha = 255}, // accent-stilus-hover (medium)
        Color{.red = 15, .green = 20, .blue = 22, .alpha = 255}, // accent-stilus-on (medium)
        Color{.red = 245, .green = 146, .blue = 62, .alpha = 255}, // accent-gesso (medium)
        Color{.red = 247, .green = 166, .blue = 96, .alpha = 255}, // accent-gesso-hover (medium)
        Color{.red = 26, .green = 20, .blue = 16, .alpha = 255}, // accent-gesso-on (medium)
        Color{.red = 76, .green = 196, .blue = 122, .alpha = 255}, // accent-albumen (medium)
        Color{.red = 110, .green = 208, .blue = 146, .alpha = 255}, // accent-albumen-hover (medium)
        Color{.red = 15, .green = 22, .blue = 18, .alpha = 255}, // accent-albumen-on (medium)
        Color{.red = 255, .green = 186, .blue = 180, .alpha = 255}, // status-error (medium)
        Color{.red = 109, .green = 68, .blue = 65, .alpha = 255}, // status-error-subtle (medium)
        Color{.red = 255, .green = 219, .blue = 138, .alpha = 255}, // status-warning (medium)
        Color{.red = 106, .green = 92, .blue = 58, .alpha = 255}, // status-warning-subtle (medium)
        Color{.red = 166, .green = 232, .blue = 189, .alpha = 255}, // status-success (medium)
        Color{.red = 64, .green = 98, .blue = 77, .alpha = 255}, // status-success-subtle (medium)
        Color{.red = 176, .green = 214, .blue = 255, .alpha = 255}, // status-info (medium)
        Color{.red = 63, .green = 90, .blue = 120, .alpha = 255}, // status-info-subtle (medium)
        Color{.red = 196, .green = 43, .blue = 28, .alpha = 255}, // caption-close-hover (medium)
        Color{.red = 178, .green = 42, .blue = 27, .alpha = 255}, // caption-close-pressed (medium)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // caption-close-on (medium)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // checker-light (medium)
        Color{.red = 204, .green = 204, .blue = 204, .alpha = 255}, // checker-dark (medium)
        Color{.red = 0, .green = 200, .blue = 255, .alpha = 255}, // guide (medium)
        Color{.red = 255, .green = 61, .blue = 220, .alpha = 255}, // guide-smart (medium)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // ants-light (medium)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 255}, // ants-dark (medium)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // handle-fill (medium)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // artboard (medium)
    }},
    {{ // Light
        Color{.red = 196, .green = 196, .blue = 196, .alpha = 255}, // frame (light)
        Color{.red = 214, .green = 214, .blue = 214, .alpha = 255}, // surface-panel (light)
        Color{.red = 205, .green = 205, .blue = 205, .alpha = 255}, // surface-tabstrip (light)
        Color{.red = 235, .green = 235, .blue = 235, .alpha = 255}, // surface-raised (light)
        Color{.red = 247, .green = 247, .blue = 247, .alpha = 255}, // surface-field (light)
        Color{.red = 228, .green = 228, .blue = 228, .alpha = 255}, // surface-control (light)
        Color{.red = 240, .green = 240, .blue = 240, .alpha = 255}, // surface-control-hover (light)
        Color{.red = 196, .green = 196, .blue = 196, .alpha = 255}, // surface-control-pressed (light)
        Color{.red = 201, .green = 201, .blue = 201, .alpha = 255}, // surface-hover (light)
        Color{.red = 163, .green = 163, .blue = 163, .alpha = 255}, // canvas-surround (light)
        Color{.red = 203, .green = 203, .blue = 203, .alpha = 255}, // ruler-surface (light)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 89}, // scrim (light)
        Color{.red = 188, .green = 188, .blue = 188, .alpha = 255}, // divider (light)
        Color{.red = 169, .green = 169, .blue = 169, .alpha = 255}, // divider-strong (light)
        Color{.red = 107, .green = 107, .blue = 107, .alpha = 255}, // border-control (light)
        Color{.red = 89, .green = 89, .blue = 89, .alpha = 255}, // border-control-hover (light)
        Color{.red = 158, .green = 158, .blue = 158, .alpha = 255}, // border-popup (light)
        Color{.red = 154, .green = 154, .blue = 154, .alpha = 255}, // scroll-thumb (light)
        Color{.red = 110, .green = 110, .blue = 110, .alpha = 255}, // scroll-thumb-hover (light)
        Color{.red = 26, .green = 26, .blue = 26, .alpha = 255}, // text-primary (light)
        Color{.red = 63, .green = 63, .blue = 63, .alpha = 255}, // text-secondary (light)
        Color{.red = 142, .green = 142, .blue = 142, .alpha = 255}, // text-disabled (light)
        Color{.red = 107, .green = 107, .blue = 107, .alpha = 255}, // text-placeholder (light)
        Color{.red = 20, .green = 115, .blue = 230, .alpha = 255}, // state (light)
        Color{.red = 13, .green = 102, .blue = 208, .alpha = 255}, // state-hover (light)
        Color{.red = 10, .green = 87, .blue = 180, .alpha = 255}, // state-pressed (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // state-on (light)
        Color{.red = 189, .green = 213, .blue = 243, .alpha = 255}, // state-subtle (light)
        Color{.red = 20, .green = 115, .blue = 230, .alpha = 46}, // state-tint (light)
        Color{.red = 15, .green = 99, .blue = 201, .alpha = 255}, // state-line (light)
        Color{.red = 10, .green = 87, .blue = 180, .alpha = 255}, // state-text (light)
        Color{.red = 180, .green = 180, .blue = 180, .alpha = 255}, // selection-inactive (light)
        Color{.red = 184, .green = 61, .blue = 11, .alpha = 255}, // state-orange (light)
        Color{.red = 163, .green = 53, .blue = 8, .alpha = 255}, // state-orange-hover (light)
        Color{.red = 142, .green = 46, .blue = 6, .alpha = 255}, // state-orange-pressed (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // state-orange-on (light)
        Color{.red = 244, .green = 205, .blue = 185, .alpha = 255}, // state-orange-subtle (light)
        Color{.red = 184, .green = 61, .blue = 11, .alpha = 36}, // state-orange-tint (light)
        Color{.red = 184, .green = 61, .blue = 11, .alpha = 255}, // state-orange-line (light)
        Color{.red = 163, .green = 53, .blue = 8, .alpha = 255}, // state-orange-text (light)
        Color{.red = 0, .green = 117, .blue = 140, .alpha = 255}, // accent-stilus (light)
        Color{.red = 0, .green = 104, .blue = 124, .alpha = 255}, // accent-stilus-hover (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // accent-stilus-on (light)
        Color{.red = 176, .green = 79, .blue = 0, .alpha = 255}, // accent-gesso (light)
        Color{.red = 154, .green = 69, .blue = 0, .alpha = 255}, // accent-gesso-hover (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // accent-gesso-on (light)
        Color{.red = 27, .green = 122, .blue = 61, .alpha = 255}, // accent-albumen (light)
        Color{.red = 22, .green = 106, .blue = 52, .alpha = 255}, // accent-albumen-hover (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // accent-albumen-on (light)
        Color{.red = 173, .green = 36, .blue = 24, .alpha = 255}, // status-error (light)
        Color{.red = 247, .green = 216, .blue = 213, .alpha = 255}, // status-error-subtle (light)
        Color{.red = 122, .green = 80, .blue = 0, .alpha = 255}, // status-warning (light)
        Color{.red = 246, .green = 231, .blue = 192, .alpha = 255}, // status-warning-subtle (light)
        Color{.red = 22, .green = 102, .blue = 40, .alpha = 255}, // status-success (light)
        Color{.red = 211, .green = 238, .blue = 219, .alpha = 255}, // status-success-subtle (light)
        Color{.red = 10, .green = 87, .blue = 180, .alpha = 255}, // status-info (light)
        Color{.red = 214, .green = 230, .blue = 248, .alpha = 255}, // status-info-subtle (light)
        Color{.red = 196, .green = 43, .blue = 28, .alpha = 255}, // caption-close-hover (light)
        Color{.red = 178, .green = 42, .blue = 27, .alpha = 255}, // caption-close-pressed (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // caption-close-on (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // checker-light (light)
        Color{.red = 204, .green = 204, .blue = 204, .alpha = 255}, // checker-dark (light)
        Color{.red = 0, .green = 200, .blue = 255, .alpha = 255}, // guide (light)
        Color{.red = 255, .green = 61, .blue = 220, .alpha = 255}, // guide-smart (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // ants-light (light)
        Color{.red = 0, .green = 0, .blue = 0, .alpha = 255}, // ants-dark (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // handle-fill (light)
        Color{.red = 255, .green = 255, .blue = 255, .alpha = 255}, // artboard (light)
    }},
}};

const std::array<std::array<Shadow, kShadowCount>, kBrightnessCount> kShadows{{
    {{ // Dark
        Shadow{.offset_x = 0.0F, .offset_y = 2.0F, .blur = 8.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 77}}, // shadow-tooltip (dark)
        Shadow{.offset_x = 0.0F, .offset_y = 4.0F, .blur = 16.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 115}}, // shadow-popup (dark)
        Shadow{.offset_x = 0.0F, .offset_y = 12.0F, .blur = 40.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 153}}, // shadow-dialog (dark)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 8.0F, .color = Color{.red = 20, .green = 115, .blue = 230, .alpha = 128}}, // glow-state (dark)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 8.0F, .color = Color{.red = 255, .green = 107, .blue = 53, .alpha = 128}}, // glow-state-orange (dark)
    }},
    {{ // Darkest
        Shadow{.offset_x = 0.0F, .offset_y = 2.0F, .blur = 8.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 102}}, // shadow-tooltip (darkest)
        Shadow{.offset_x = 0.0F, .offset_y = 4.0F, .blur = 16.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 140}}, // shadow-popup (darkest)
        Shadow{.offset_x = 0.0F, .offset_y = 12.0F, .blur = 40.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 179}}, // shadow-dialog (darkest)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 8.0F, .color = Color{.red = 20, .green = 115, .blue = 230, .alpha = 153}}, // glow-state (darkest)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 8.0F, .color = Color{.red = 255, .green = 107, .blue = 53, .alpha = 153}}, // glow-state-orange (darkest)
    }},
    {{ // MediumGray
        Shadow{.offset_x = 0.0F, .offset_y = 2.0F, .blur = 8.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 64}}, // shadow-tooltip (medium)
        Shadow{.offset_x = 0.0F, .offset_y = 4.0F, .blur = 16.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 89}}, // shadow-popup (medium)
        Shadow{.offset_x = 0.0F, .offset_y = 12.0F, .blur = 40.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 115}}, // shadow-dialog (medium)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 8.0F, .color = Color{.red = 20, .green = 115, .blue = 230, .alpha = 115}}, // glow-state (medium)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 8.0F, .color = Color{.red = 255, .green = 107, .blue = 53, .alpha = 115}}, // glow-state-orange (medium)
    }},
    {{ // Light
        Shadow{.offset_x = 0.0F, .offset_y = 2.0F, .blur = 8.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 41}}, // shadow-tooltip (light)
        Shadow{.offset_x = 0.0F, .offset_y = 4.0F, .blur = 14.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 56}}, // shadow-popup (light)
        Shadow{.offset_x = 0.0F, .offset_y = 12.0F, .blur = 32.0F, .color = Color{.red = 0, .green = 0, .blue = 0, .alpha = 71}}, // shadow-dialog (light)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 6.0F, .color = Color{.red = 20, .green = 115, .blue = 230, .alpha = 89}}, // glow-state (light)
        Shadow{.offset_x = 0.0F, .offset_y = 0.0F, .blur = 6.0F, .color = Color{.red = 184, .green = 61, .blue = 11, .alpha = 89}}, // glow-state-orange (light)
    }},
}};

const std::array<float, kSizeCount> kSizes{{
    2.0F, // space-hair
    4.0F, // space-1
    6.0F, // space-1-5
    8.0F, // space-2
    12.0F, // space-3
    16.0F, // space-4
    24.0F, // space-6
    2.0F, // radius-sm
    4.0F, // radius-md
    6.0F, // radius-lg
    9999.0F, // radius-round
    24.0F, // control-h-compact
    30.0F, // control-h-comfortable
    28.0F, // control-h-dialog
    32.0F, // titlebar-h
    46.0F, // caption-button-w
    24.0F, // menu-row-h-compact
    30.0F, // menu-row-h-comfortable
    200.0F, // menu-w-min
    32.0F, // optionsbar-h-compact
    40.0F, // optionsbar-h-comfortable
    28.0F, // infobar-h
    28.0F, // doctab-h-compact
    32.0F, // doctab-h-comfortable
    240.0F, // doctab-w-max
    32.0F, // tool-button-compact
    40.0F, // tool-button-comfortable
    40.0F, // toolrail-w-compact
    48.0F, // toolrail-w-comfortable
    260.0F, // panel-w-min
    280.0F, // panel-w-default
    300.0F, // panel-w-max
    26.0F, // panel-tab-h-compact
    32.0F, // panel-tab-h-comfortable
    36.0F, // panel-iconstrip-w
    28.0F, // section-header-h
    22.0F, // row-h-compact
    28.0F, // row-h-comfortable
    36.0F, // layer-row-h-compact
    44.0F, // layer-row-h-comfortable
    22.0F, // statusbar-h-compact
    26.0F, // statusbar-h-comfortable
    18.0F, // ruler-w
    16.0F, // icon-sm
    20.0F, // icon-md
    1.5F, // icon-stroke
    14.0F, // check-size-compact
    16.0F, // check-size-comfortable
    32.0F, // toggle-w
    2.0F, // slider-track-h
    10.0F, // slider-thumb
    4.0F, // scrollbar-w-rest
    10.0F, // scrollbar-w-hover
    16.0F, // swatch-compact
    20.0F, // swatch-comfortable
    24.0F, // color-chip
    2.0F, // focus-ring-w
    7.0F, // handle-size
    8.0F, // checker-tile
    11.0F, // type-caption
    12.0F, // type-body-compact
    13.0F, // type-body-comfortable
    14.0F, // type-title
}};

const std::array<std::int32_t, kDurationCount> kDurations{{
    100, // duration-fast
    200, // duration-standard
    400, // duration-slow
    400, // tooltip-delay
}};

const std::array<Easing, kEasingCount> kEasings{{
    Easing{.x1 = 0.33F, .y1 = 1.0F, .x2 = 0.68F, .y2 = 1.0F}, // ease-out
}};

const std::array<TypeStyle, kTypeStyleCount> kTypeStyles{{
    TypeStyle{.family = FontFamily::Sans, .size = 11.0F, .line_height = 14.0F, .weight = 400, .letter_spacing = 0.0F}, // caption-compact
    TypeStyle{.family = FontFamily::Sans, .size = 12.0F, .line_height = 16.0F, .weight = 400, .letter_spacing = 0.0F}, // body-compact
    TypeStyle{.family = FontFamily::Sans, .size = 12.0F, .line_height = 16.0F, .weight = 600, .letter_spacing = 0.0F}, // body-strong-compact
    TypeStyle{.family = FontFamily::Sans, .size = 11.0F, .line_height = 14.0F, .weight = 600, .letter_spacing = 0.44F}, // section-header
    TypeStyle{.family = FontFamily::Sans, .size = 14.0F, .line_height = 20.0F, .weight = 400, .letter_spacing = 0.0F}, // title
    TypeStyle{.family = FontFamily::Sans, .size = 14.0F, .line_height = 20.0F, .weight = 600, .letter_spacing = 0.0F}, // dialog-title
    TypeStyle{.family = FontFamily::Sans, .size = 12.0F, .line_height = 16.0F, .weight = 400, .letter_spacing = 0.0F}, // caption-comfortable
    TypeStyle{.family = FontFamily::Sans, .size = 13.0F, .line_height = 18.0F, .weight = 400, .letter_spacing = 0.0F}, // body-comfortable
    TypeStyle{.family = FontFamily::Sans, .size = 13.0F, .line_height = 18.0F, .weight = 600, .letter_spacing = 0.0F}, // body-strong-comfortable
    TypeStyle{.family = FontFamily::Display, .size = 46.0F, .line_height = 56.0F, .weight = 600, .letter_spacing = -0.5F}, // display
    TypeStyle{.family = FontFamily::Mono, .size = 11.0F, .line_height = 14.0F, .weight = 400, .letter_spacing = 0.0F}, // mono
    TypeStyle{.family = FontFamily::Mono, .size = 12.0F, .line_height = 16.0F, .weight = 400, .letter_spacing = 0.0F}, // mono-body
}};

const std::array<TokenKey, kTokenCount> kIsotoneOrange{{
    TokenKey::Frame, // frame
    TokenKey::SurfacePanel, // surface-panel
    TokenKey::SurfaceTabstrip, // surface-tabstrip
    TokenKey::SurfaceRaised, // surface-raised
    TokenKey::SurfaceField, // surface-field
    TokenKey::SurfaceControl, // surface-control
    TokenKey::SurfaceControlHover, // surface-control-hover
    TokenKey::SurfaceControlPressed, // surface-control-pressed
    TokenKey::SurfaceHover, // surface-hover
    TokenKey::CanvasSurround, // canvas-surround
    TokenKey::RulerSurface, // ruler-surface
    TokenKey::Scrim, // scrim
    TokenKey::Divider, // divider
    TokenKey::DividerStrong, // divider-strong
    TokenKey::BorderControl, // border-control
    TokenKey::BorderControlHover, // border-control-hover
    TokenKey::BorderPopup, // border-popup
    TokenKey::ScrollThumb, // scroll-thumb
    TokenKey::ScrollThumbHover, // scroll-thumb-hover
    TokenKey::TextPrimary, // text-primary
    TokenKey::TextSecondary, // text-secondary
    TokenKey::TextDisabled, // text-disabled
    TokenKey::TextPlaceholder, // text-placeholder
    TokenKey::Icon, // icon
    TokenKey::StateOrange, // state
    TokenKey::StateOrangeHover, // state-hover
    TokenKey::StateOrangePressed, // state-pressed
    TokenKey::StateOrangeOn, // state-on
    TokenKey::StateOrangeSubtle, // state-subtle
    TokenKey::StateOrangeTint, // state-tint
    TokenKey::StateOrangeLine, // state-line
    TokenKey::StateOrangeText, // state-text
    TokenKey::FocusRing, // focus-ring
    TokenKey::SelectionInactive, // selection-inactive
    TokenKey::StateOrange, // state-orange
    TokenKey::StateOrangeHover, // state-orange-hover
    TokenKey::StateOrangePressed, // state-orange-pressed
    TokenKey::StateOrangeOn, // state-orange-on
    TokenKey::StateOrangeSubtle, // state-orange-subtle
    TokenKey::StateOrangeTint, // state-orange-tint
    TokenKey::StateOrangeLine, // state-orange-line
    TokenKey::StateOrangeText, // state-orange-text
    TokenKey::AccentStilus, // accent-stilus
    TokenKey::AccentStilusHover, // accent-stilus-hover
    TokenKey::AccentStilusOn, // accent-stilus-on
    TokenKey::AccentGesso, // accent-gesso
    TokenKey::AccentGessoHover, // accent-gesso-hover
    TokenKey::AccentGessoOn, // accent-gesso-on
    TokenKey::AccentAlbumen, // accent-albumen
    TokenKey::AccentAlbumenHover, // accent-albumen-hover
    TokenKey::AccentAlbumenOn, // accent-albumen-on
    TokenKey::StatusError, // status-error
    TokenKey::StatusErrorSubtle, // status-error-subtle
    TokenKey::StatusWarning, // status-warning
    TokenKey::StatusWarningSubtle, // status-warning-subtle
    TokenKey::StatusSuccess, // status-success
    TokenKey::StatusSuccessSubtle, // status-success-subtle
    TokenKey::StatusInfo, // status-info
    TokenKey::StatusInfoSubtle, // status-info-subtle
    TokenKey::CaptionCloseHover, // caption-close-hover
    TokenKey::CaptionClosePressed, // caption-close-pressed
    TokenKey::CaptionCloseOn, // caption-close-on
    TokenKey::CheckerLight, // checker-light
    TokenKey::CheckerDark, // checker-dark
    TokenKey::Guide, // guide
    TokenKey::GuideSmart, // guide-smart
    TokenKey::AntsLight, // ants-light
    TokenKey::AntsDark, // ants-dark
    TokenKey::HandleFill, // handle-fill
    TokenKey::HandleStroke, // handle-stroke
    TokenKey::Artboard, // artboard
    TokenKey::ShadowTooltip, // shadow-tooltip
    TokenKey::ShadowPopup, // shadow-popup
    TokenKey::ShadowDialog, // shadow-dialog
    TokenKey::GlowStateOrange, // glow-state
    TokenKey::GlowStateOrange, // glow-state-orange
    TokenKey::SpaceHair, // space-hair
    TokenKey::Space1, // space-1
    TokenKey::Space15, // space-1-5
    TokenKey::Space2, // space-2
    TokenKey::Space3, // space-3
    TokenKey::Space4, // space-4
    TokenKey::Space6, // space-6
    TokenKey::RadiusSm, // radius-sm
    TokenKey::RadiusMd, // radius-md
    TokenKey::RadiusLg, // radius-lg
    TokenKey::RadiusRound, // radius-round
    TokenKey::ControlHCompact, // control-h-compact
    TokenKey::ControlHComfortable, // control-h-comfortable
    TokenKey::ControlHDialog, // control-h-dialog
    TokenKey::TitlebarH, // titlebar-h
    TokenKey::CaptionButtonW, // caption-button-w
    TokenKey::MenuRowHCompact, // menu-row-h-compact
    TokenKey::MenuRowHComfortable, // menu-row-h-comfortable
    TokenKey::MenuWMin, // menu-w-min
    TokenKey::OptionsbarHCompact, // optionsbar-h-compact
    TokenKey::OptionsbarHComfortable, // optionsbar-h-comfortable
    TokenKey::InfobarH, // infobar-h
    TokenKey::DoctabHCompact, // doctab-h-compact
    TokenKey::DoctabHComfortable, // doctab-h-comfortable
    TokenKey::DoctabWMax, // doctab-w-max
    TokenKey::ToolButtonCompact, // tool-button-compact
    TokenKey::ToolButtonComfortable, // tool-button-comfortable
    TokenKey::ToolrailWCompact, // toolrail-w-compact
    TokenKey::ToolrailWComfortable, // toolrail-w-comfortable
    TokenKey::PanelWMin, // panel-w-min
    TokenKey::PanelWDefault, // panel-w-default
    TokenKey::PanelWMax, // panel-w-max
    TokenKey::PanelTabHCompact, // panel-tab-h-compact
    TokenKey::PanelTabHComfortable, // panel-tab-h-comfortable
    TokenKey::PanelIconstripW, // panel-iconstrip-w
    TokenKey::SectionHeaderH, // section-header-h
    TokenKey::RowHCompact, // row-h-compact
    TokenKey::RowHComfortable, // row-h-comfortable
    TokenKey::LayerRowHCompact, // layer-row-h-compact
    TokenKey::LayerRowHComfortable, // layer-row-h-comfortable
    TokenKey::StatusbarHCompact, // statusbar-h-compact
    TokenKey::StatusbarHComfortable, // statusbar-h-comfortable
    TokenKey::RulerW, // ruler-w
    TokenKey::IconSm, // icon-sm
    TokenKey::IconMd, // icon-md
    TokenKey::IconStroke, // icon-stroke
    TokenKey::CheckSizeCompact, // check-size-compact
    TokenKey::CheckSizeComfortable, // check-size-comfortable
    TokenKey::ToggleW, // toggle-w
    TokenKey::SliderTrackH, // slider-track-h
    TokenKey::SliderThumb, // slider-thumb
    TokenKey::ScrollbarWRest, // scrollbar-w-rest
    TokenKey::ScrollbarWHover, // scrollbar-w-hover
    TokenKey::SwatchCompact, // swatch-compact
    TokenKey::SwatchComfortable, // swatch-comfortable
    TokenKey::ColorChip, // color-chip
    TokenKey::FocusRingW, // focus-ring-w
    TokenKey::HandleSize, // handle-size
    TokenKey::CheckerTile, // checker-tile
    TokenKey::TypeCaption, // type-caption
    TokenKey::TypeBodyCompact, // type-body-compact
    TokenKey::TypeBodyComfortable, // type-body-comfortable
    TokenKey::TypeTitle, // type-title
    TokenKey::DurationFast, // duration-fast
    TokenKey::DurationStandard, // duration-standard
    TokenKey::DurationSlow, // duration-slow
    TokenKey::TooltipDelay, // tooltip-delay
    TokenKey::EaseOut, // ease-out
    TokenKey::Caption, // caption
    TokenKey::Body, // body
    TokenKey::BodyStrong, // body-strong
    TokenKey::SectionHeader, // section-header
    TokenKey::Title, // title
    TokenKey::DialogTitle, // dialog-title
    TokenKey::CaptionComfortable, // caption-comfortable
    TokenKey::BodyComfortable, // body-comfortable
    TokenKey::BodyStrongComfortable, // body-strong-comfortable
    TokenKey::Display, // display
    TokenKey::Mono, // mono
    TokenKey::MonoBody, // mono-body
    TokenKey::ControlH, // control-h
    TokenKey::MenuRowH, // menu-row-h
    TokenKey::OptionsbarH, // optionsbar-h
    TokenKey::DoctabH, // doctab-h
    TokenKey::ToolButton, // tool-button
    TokenKey::ToolrailW, // toolrail-w
    TokenKey::PanelTabH, // panel-tab-h
    TokenKey::RowH, // row-h
    TokenKey::LayerRowH, // layer-row-h
    TokenKey::StatusbarH, // statusbar-h
    TokenKey::CheckSize, // check-size
    TokenKey::Swatch, // swatch
    TokenKey::TypeBody, // type-body
    TokenKey::CaptionCompact, // caption-compact
    TokenKey::BodyCompact, // body-compact
    TokenKey::BodyStrongCompact, // body-strong-compact
}};

const std::array<Contrast, kTokenCount> kHighContrast{{
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // frame
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // surface-panel
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // surface-tabstrip
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // surface-raised
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // surface-field
    Contrast{.rule = ContrastRule::System, .system = SystemColor::ButtonFace}, // surface-control
    Contrast{.rule = ContrastRule::System, .system = SystemColor::ButtonFace}, // surface-control-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::ButtonFace}, // surface-control-pressed
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // surface-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // canvas-surround
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Window}, // ruler-surface
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // scrim
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // divider
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // divider-strong
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // border-control
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // border-control-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // border-popup
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // scroll-thumb
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // scroll-thumb-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // text-primary
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // text-secondary
    Contrast{.rule = ContrastRule::System, .system = SystemColor::GrayText}, // text-disabled
    Contrast{.rule = ContrastRule::System, .system = SystemColor::GrayText}, // text-placeholder
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // icon
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-pressed
    Contrast{.rule = ContrastRule::System, .system = SystemColor::HighlightText}, // state-on
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-subtle
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-tint
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-line
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Hotlight}, // state-text
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // focus-ring
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // selection-inactive
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-orange
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-orange-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-orange-pressed
    Contrast{.rule = ContrastRule::System, .system = SystemColor::HighlightText}, // state-orange-on
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-orange-subtle
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-orange-tint
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // state-orange-line
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Hotlight}, // state-orange-text
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // accent-stilus
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // accent-stilus-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // accent-stilus-on
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // accent-gesso
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // accent-gesso-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // accent-gesso-on
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // accent-albumen
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // accent-albumen-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // accent-albumen-on
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // status-error
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // status-error-subtle
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // status-warning
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // status-warning-subtle
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // status-success
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // status-success-subtle
    Contrast{.rule = ContrastRule::System, .system = SystemColor::WindowText}, // status-info
    Contrast{.rule = ContrastRule::None, .system = SystemColor::Window}, // status-info-subtle
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // caption-close-hover
    Contrast{.rule = ContrastRule::System, .system = SystemColor::Highlight}, // caption-close-pressed
    Contrast{.rule = ContrastRule::System, .system = SystemColor::HighlightText}, // caption-close-on
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // checker-light
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // checker-dark
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // guide
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // guide-smart
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // ants-light
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // ants-dark
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // handle-fill
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // handle-stroke
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // artboard
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // shadow-tooltip
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // shadow-popup
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // shadow-dialog
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // glow-state
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // glow-state-orange
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // space-hair
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // space-1
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // space-1-5
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // space-2
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // space-3
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // space-4
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // space-6
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // radius-sm
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // radius-md
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // radius-lg
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // radius-round
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // control-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // control-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // control-h-dialog
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // titlebar-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // caption-button-w
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // menu-row-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // menu-row-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // menu-w-min
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // optionsbar-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // optionsbar-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // infobar-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // doctab-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // doctab-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // doctab-w-max
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // tool-button-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // tool-button-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // toolrail-w-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // toolrail-w-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // panel-w-min
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // panel-w-default
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // panel-w-max
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // panel-tab-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // panel-tab-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // panel-iconstrip-w
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // section-header-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // row-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // row-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // layer-row-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // layer-row-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // statusbar-h-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // statusbar-h-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // ruler-w
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // icon-sm
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // icon-md
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // icon-stroke
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // check-size-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // check-size-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // toggle-w
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // slider-track-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // slider-thumb
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // scrollbar-w-rest
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // scrollbar-w-hover
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // swatch-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // swatch-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // color-chip
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // focus-ring-w
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // handle-size
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // checker-tile
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // type-caption
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // type-body-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // type-body-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // type-title
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // duration-fast
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // duration-standard
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // duration-slow
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // tooltip-delay
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // ease-out
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // caption
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // body
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // body-strong
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // section-header
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // title
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // dialog-title
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // caption-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // body-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // body-strong-comfortable
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // display
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // mono
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // mono-body
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // control-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // menu-row-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // optionsbar-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // doctab-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // tool-button
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // toolrail-w
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // panel-tab-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // row-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // layer-row-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // statusbar-h
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // check-size
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // swatch
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // type-body
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // caption-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // body-compact
    Contrast{.rule = ContrastRule::Keep, .system = SystemColor::Window}, // body-strong-compact
}};

const std::array<float, 256> kSrgbToLinear{{
    std::bit_cast<float>(std::uint32_t{0x00000000U}), // 0: 0.000000000
    std::bit_cast<float>(std::uint32_t{0x399F22B4U}), // 1: 0.000303527
    std::bit_cast<float>(std::uint32_t{0x3A1F22B4U}), // 2: 0.000607054
    std::bit_cast<float>(std::uint32_t{0x3A6EB40EU}), // 3: 0.000910581
    std::bit_cast<float>(std::uint32_t{0x3A9F22B4U}), // 4: 0.001214108
    std::bit_cast<float>(std::uint32_t{0x3AC6EB61U}), // 5: 0.001517635
    std::bit_cast<float>(std::uint32_t{0x3AEEB40EU}), // 6: 0.001821162
    std::bit_cast<float>(std::uint32_t{0x3B0B3E5DU}), // 7: 0.002124689
    std::bit_cast<float>(std::uint32_t{0x3B1F22B4U}), // 8: 0.002428216
    std::bit_cast<float>(std::uint32_t{0x3B33070AU}), // 9: 0.002731743
    std::bit_cast<float>(std::uint32_t{0x3B46EB61U}), // 10: 0.003035270
    std::bit_cast<float>(std::uint32_t{0x3B5B518EU}), // 11: 0.003346536
    std::bit_cast<float>(std::uint32_t{0x3B70F18FU}), // 12: 0.003676507
    std::bit_cast<float>(std::uint32_t{0x3B83E1C6U}), // 13: 0.004024717
    std::bit_cast<float>(std::uint32_t{0x3B8FE616U}), // 14: 0.004391442
    std::bit_cast<float>(std::uint32_t{0x3B9C87FDU}), // 15: 0.004776953
    std::bit_cast<float>(std::uint32_t{0x3BA9C9B6U}), // 16: 0.005181517
    std::bit_cast<float>(std::uint32_t{0x3BB7AD6FU}), // 17: 0.005605392
    std::bit_cast<float>(std::uint32_t{0x3BC6354AU}), // 18: 0.006048833
    std::bit_cast<float>(std::uint32_t{0x3BD56360U}), // 19: 0.006512091
    std::bit_cast<float>(std::uint32_t{0x3BE539C1U}), // 20: 0.006995410
    std::bit_cast<float>(std::uint32_t{0x3BF5BA71U}), // 21: 0.007499032
    std::bit_cast<float>(std::uint32_t{0x3C0373B6U}), // 22: 0.008023193
    std::bit_cast<float>(std::uint32_t{0x3C0C6153U}), // 23: 0.008568126
    std::bit_cast<float>(std::uint32_t{0x3C15A705U}), // 24: 0.009134059
    std::bit_cast<float>(std::uint32_t{0x3C1F45BEU}), // 25: 0.009721217
    std::bit_cast<float>(std::uint32_t{0x3C293E6BU}), // 26: 0.010329823
    std::bit_cast<float>(std::uint32_t{0x3C3391F7U}), // 27: 0.010960094
    std::bit_cast<float>(std::uint32_t{0x3C3E4149U}), // 28: 0.011612245
    std::bit_cast<float>(std::uint32_t{0x3C494D44U}), // 29: 0.012286488
    std::bit_cast<float>(std::uint32_t{0x3C54B6C9U}), // 30: 0.012983032
    std::bit_cast<float>(std::uint32_t{0x3C607EB4U}), // 31: 0.013702083
    std::bit_cast<float>(std::uint32_t{0x3C6CA5DFU}), // 32: 0.014443844
    std::bit_cast<float>(std::uint32_t{0x3C792D22U}), // 33: 0.015208514
    std::bit_cast<float>(std::uint32_t{0x3C830AA9U}), // 34: 0.015996293
    std::bit_cast<float>(std::uint32_t{0x3C89AF9FU}), // 35: 0.016807376
    std::bit_cast<float>(std::uint32_t{0x3C9085DCU}), // 36: 0.017641954
    std::bit_cast<float>(std::uint32_t{0x3C978DC6U}), // 37: 0.018500220
    std::bit_cast<float>(std::uint32_t{0x3C9EC7C2U}), // 38: 0.019382361
    std::bit_cast<float>(std::uint32_t{0x3CA63433U}), // 39: 0.020288563
    std::bit_cast<float>(std::uint32_t{0x3CADD37DU}), // 40: 0.021219010
    std::bit_cast<float>(std::uint32_t{0x3CB5A602U}), // 41: 0.022173885
    std::bit_cast<float>(std::uint32_t{0x3CBDAC21U}), // 42: 0.023153366
    std::bit_cast<float>(std::uint32_t{0x3CC5E63AU}), // 43: 0.024157632
    std::bit_cast<float>(std::uint32_t{0x3CCE54ACU}), // 44: 0.025186860
    std::bit_cast<float>(std::uint32_t{0x3CD6F7D5U}), // 45: 0.026241222
    std::bit_cast<float>(std::uint32_t{0x3CDFD010U}), // 46: 0.027320892
    std::bit_cast<float>(std::uint32_t{0x3CE8DDBAU}), // 47: 0.028426040
    std::bit_cast<float>(std::uint32_t{0x3CF2212DU}), // 48: 0.029556834
    std::bit_cast<float>(std::uint32_t{0x3CFB9AC3U}), // 49: 0.030713444
    std::bit_cast<float>(std::uint32_t{0x3D02A56AU}), // 50: 0.031896033
    std::bit_cast<float>(std::uint32_t{0x3D0798DDU}), // 51: 0.033104767
    std::bit_cast<float>(std::uint32_t{0x3D0CA7E6U}), // 52: 0.034339807
    std::bit_cast<float>(std::uint32_t{0x3D11D2AFU}), // 53: 0.035601315
    std::bit_cast<float>(std::uint32_t{0x3D171964U}), // 54: 0.036889450
    std::bit_cast<float>(std::uint32_t{0x3D1C7C30U}), // 55: 0.038204372
    std::bit_cast<float>(std::uint32_t{0x3D21FB3CU}), // 56: 0.039546235
    std::bit_cast<float>(std::uint32_t{0x3D2796B2U}), // 57: 0.040915197
    std::bit_cast<float>(std::uint32_t{0x3D2D4EBBU}), // 58: 0.042311411
    std::bit_cast<float>(std::uint32_t{0x3D332381U}), // 59: 0.043735029
    std::bit_cast<float>(std::uint32_t{0x3D39152BU}), // 60: 0.045186204
    std::bit_cast<float>(std::uint32_t{0x3D3F23E4U}), // 61: 0.046665086
    std::bit_cast<float>(std::uint32_t{0x3D454FD2U}), // 62: 0.048171824
    std::bit_cast<float>(std::uint32_t{0x3D4B991DU}), // 63: 0.049706566
    std::bit_cast<float>(std::uint32_t{0x3D51FFECU}), // 64: 0.051269458
    std::bit_cast<float>(std::uint32_t{0x3D588468U}), // 65: 0.052860647
    std::bit_cast<float>(std::uint32_t{0x3D5F26B6U}), // 66: 0.054480276
    std::bit_cast<float>(std::uint32_t{0x3D65E6FDU}), // 67: 0.056128490
    std::bit_cast<float>(std::uint32_t{0x3D6CC563U}), // 68: 0.057805430
    std::bit_cast<float>(std::uint32_t{0x3D73C20EU}), // 69: 0.059511238
    std::bit_cast<float>(std::uint32_t{0x3D7ADD24U}), // 70: 0.061246054
    std::bit_cast<float>(std::uint32_t{0x3D810B65U}), // 71: 0.063010018
    std::bit_cast<float>(std::uint32_t{0x3D84B793U}), // 72: 0.064803267
    std::bit_cast<float>(std::uint32_t{0x3D88732EU}), // 73: 0.066625939
    std::bit_cast<float>(std::uint32_t{0x3D8C3E48U}), // 74: 0.068478170
    std::bit_cast<float>(std::uint32_t{0x3D9018F4U}), // 75: 0.070360096
    std::bit_cast<float>(std::uint32_t{0x3D940344U}), // 76: 0.072271851
    std::bit_cast<float>(std::uint32_t{0x3D97FD49U}), // 77: 0.074213568
    std::bit_cast<float>(std::uint32_t{0x3D9C0715U}), // 78: 0.076185381
    std::bit_cast<float>(std::uint32_t{0x3DA020BAU}), // 79: 0.078187422
    std::bit_cast<float>(std::uint32_t{0x3DA44A4AU}), // 80: 0.080219820
    std::bit_cast<float>(std::uint32_t{0x3DA883D6U}), // 81: 0.082282707
    std::bit_cast<float>(std::uint32_t{0x3DACCD6FU}), // 82: 0.084376212
    std::bit_cast<float>(std::uint32_t{0x3DB12727U}), // 83: 0.086500462
    std::bit_cast<float>(std::uint32_t{0x3DB5910FU}), // 84: 0.088655586
    std::bit_cast<float>(std::uint32_t{0x3DBA0B38U}), // 85: 0.090841711
    std::bit_cast<float>(std::uint32_t{0x3DBE95B3U}), // 86: 0.093058963
    std::bit_cast<float>(std::uint32_t{0x3DC33090U}), // 87: 0.095307467
    std::bit_cast<float>(std::uint32_t{0x3DC7DBE0U}), // 88: 0.097587347
    std::bit_cast<float>(std::uint32_t{0x3DCC97B4U}), // 89: 0.099898728
    std::bit_cast<float>(std::uint32_t{0x3DD1641DU}), // 90: 0.102241733
    std::bit_cast<float>(std::uint32_t{0x3DD6412BU}), // 91: 0.104616484
    std::bit_cast<float>(std::uint32_t{0x3DDB2EEEU}), // 92: 0.107023103
    std::bit_cast<float>(std::uint32_t{0x3DE02D76U}), // 93: 0.109461711
    std::bit_cast<float>(std::uint32_t{0x3DE53CD4U}), // 94: 0.111932428
    std::bit_cast<float>(std::uint32_t{0x3DEA5D18U}), // 95: 0.114435374
    std::bit_cast<float>(std::uint32_t{0x3DEF8E51U}), // 96: 0.116970668
    std::bit_cast<float>(std::uint32_t{0x3DF4D090U}), // 97: 0.119538428
    std::bit_cast<float>(std::uint32_t{0x3DFA23E5U}), // 98: 0.122138772
    std::bit_cast<float>(std::uint32_t{0x3DFF885EU}), // 99: 0.124771818
    std::bit_cast<float>(std::uint32_t{0x3E027F06U}), // 100: 0.127437680
    std::bit_cast<float>(std::uint32_t{0x3E05427FU}), // 101: 0.130136477
    std::bit_cast<float>(std::uint32_t{0x3E080EA2U}), // 102: 0.132868322
    std::bit_cast<float>(std::uint32_t{0x3E0AE377U}), // 103: 0.135633330
    std::bit_cast<float>(std::uint32_t{0x3E0DC104U}), // 104: 0.138431615
    std::bit_cast<float>(std::uint32_t{0x3E10A753U}), // 105: 0.141263291
    std::bit_cast<float>(std::uint32_t{0x3E13966AU}), // 106: 0.144128471
    std::bit_cast<float>(std::uint32_t{0x3E168E51U}), // 107: 0.147027266
    std::bit_cast<float>(std::uint32_t{0x3E198F0FU}), // 108: 0.149959790
    std::bit_cast<float>(std::uint32_t{0x3E1C98ACU}), // 109: 0.152926152
    std::bit_cast<float>(std::uint32_t{0x3E1FAB30U}), // 110: 0.155926464
    std::bit_cast<float>(std::uint32_t{0x3E22C6A1U}), // 111: 0.158960835
    std::bit_cast<float>(std::uint32_t{0x3E25EB07U}), // 112: 0.162029376
    std::bit_cast<float>(std::uint32_t{0x3E29186AU}), // 113: 0.165132195
    std::bit_cast<float>(std::uint32_t{0x3E2C4ED0U}), // 114: 0.168269400
    std::bit_cast<float>(std::uint32_t{0x3E2F8E42U}), // 115: 0.171441101
    std::bit_cast<float>(std::uint32_t{0x3E32D6C5U}), // 116: 0.174647404
    std::bit_cast<float>(std::uint32_t{0x3E362862U}), // 117: 0.177888416
    std::bit_cast<float>(std::uint32_t{0x3E39831FU}), // 118: 0.181164244
    std::bit_cast<float>(std::uint32_t{0x3E3CE703U}), // 119: 0.184474995
    std::bit_cast<float>(std::uint32_t{0x3E405417U}), // 120: 0.187820772
    std::bit_cast<float>(std::uint32_t{0x3E43CA60U}), // 121: 0.191201683
    std::bit_cast<float>(std::uint32_t{0x3E4749E6U}), // 122: 0.194617830
    std::bit_cast<float>(std::uint32_t{0x3E4AD2AFU}), // 123: 0.198069320
    std::bit_cast<float>(std::uint32_t{0x3E4E64C3U}), // 124: 0.201556254
    std::bit_cast<float>(std::uint32_t{0x3E520029U}), // 125: 0.205078736
    std::bit_cast<float>(std::uint32_t{0x3E55A4E7U}), // 126: 0.208636870
    std::bit_cast<float>(std::uint32_t{0x3E595305U}), // 127: 0.212230757
    std::bit_cast<float>(std::uint32_t{0x3E5D0A89U}), // 128: 0.215860500
    std::bit_cast<float>(std::uint32_t{0x3E60CB7AU}), // 129: 0.219526200
    std::bit_cast<float>(std::uint32_t{0x3E6495DFU}), // 130: 0.223227957
    std::bit_cast<float>(std::uint32_t{0x3E6869BEU}), // 131: 0.226965874
    std::bit_cast<float>(std::uint32_t{0x3E6C471FU}), // 132: 0.230740049
    std::bit_cast<float>(std::uint32_t{0x3E702E07U}), // 133: 0.234550582
    std::bit_cast<float>(std::uint32_t{0x3E741E7EU}), // 134: 0.238397574
    std::bit_cast<float>(std::uint32_t{0x3E78188BU}), // 135: 0.242281122
    std::bit_cast<float>(std::uint32_t{0x3E7C1C33U}), // 136: 0.246201327
    std::bit_cast<float>(std::uint32_t{0x3E8014BFU}), // 137: 0.250158285
    std::bit_cast<float>(std::uint32_t{0x3E822039U}), // 138: 0.254152094
    std::bit_cast<float>(std::uint32_t{0x3E84308BU}), // 139: 0.258182853
    std::bit_cast<float>(std::uint32_t{0x3E8645B8U}), // 140: 0.262250658
    std::bit_cast<float>(std::uint32_t{0x3E885FC3U}), // 141: 0.266355605
    std::bit_cast<float>(std::uint32_t{0x3E8A7EB0U}), // 142: 0.270497791
    std::bit_cast<float>(std::uint32_t{0x3E8CA281U}), // 143: 0.274677312
    std::bit_cast<float>(std::uint32_t{0x3E8ECB3BU}), // 144: 0.278894263
    std::bit_cast<float>(std::uint32_t{0x3E90F8DFU}), // 145: 0.283148740
    std::bit_cast<float>(std::uint32_t{0x3E932B72U}), // 146: 0.287440838
    std::bit_cast<float>(std::uint32_t{0x3E9562F6U}), // 147: 0.291770650
    std::bit_cast<float>(std::uint32_t{0x3E979F6FU}), // 148: 0.296138271
    std::bit_cast<float>(std::uint32_t{0x3E99E0E0U}), // 149: 0.300543794
    std::bit_cast<float>(std::uint32_t{0x3E9C274CU}), // 150: 0.304987314
    std::bit_cast<float>(std::uint32_t{0x3E9E72B6U}), // 151: 0.309468923
    std::bit_cast<float>(std::uint32_t{0x3EA0C321U}), // 152: 0.313988713
    std::bit_cast<float>(std::uint32_t{0x3EA31890U}), // 153: 0.318546778
    std::bit_cast<float>(std::uint32_t{0x3EA57307U}), // 154: 0.323143209
    std::bit_cast<float>(std::uint32_t{0x3EA7D288U}), // 155: 0.327778098
    std::bit_cast<float>(std::uint32_t{0x3EAA3716U}), // 156: 0.332451536
    std::bit_cast<float>(std::uint32_t{0x3EACA0B6U}), // 157: 0.337163615
    std::bit_cast<float>(std::uint32_t{0x3EAF0F68U}), // 158: 0.341914425
    std::bit_cast<float>(std::uint32_t{0x3EB18332U}), // 159: 0.346704056
    std::bit_cast<float>(std::uint32_t{0x3EB3FC15U}), // 160: 0.351532600
    std::bit_cast<float>(std::uint32_t{0x3EB67A14U}), // 161: 0.356400144
    std::bit_cast<float>(std::uint32_t{0x3EB8FD34U}), // 162: 0.361306780
    std::bit_cast<float>(std::uint32_t{0x3EBB8576U}), // 163: 0.366252596
    std::bit_cast<float>(std::uint32_t{0x3EBE12DEU}), // 164: 0.371237680
    std::bit_cast<float>(std::uint32_t{0x3EC0A56EU}), // 165: 0.376262123
    std::bit_cast<float>(std::uint32_t{0x3EC33D2AU}), // 166: 0.381326011
    std::bit_cast<float>(std::uint32_t{0x3EC5DA14U}), // 167: 0.386429434
    std::bit_cast<float>(std::uint32_t{0x3EC87C30U}), // 168: 0.391572478
    std::bit_cast<float>(std::uint32_t{0x3ECB2380U}), // 169: 0.396755231
    std::bit_cast<float>(std::uint32_t{0x3ECDD008U}), // 170: 0.401977780
    std::bit_cast<float>(std::uint32_t{0x3ED081CAU}), // 171: 0.407240212
    std::bit_cast<float>(std::uint32_t{0x3ED338C9U}), // 172: 0.412542613
    std::bit_cast<float>(std::uint32_t{0x3ED5F508U}), // 173: 0.417885071
    std::bit_cast<float>(std::uint32_t{0x3ED8B68AU}), // 174: 0.423267670
    std::bit_cast<float>(std::uint32_t{0x3EDB7D52U}), // 175: 0.428690497
    std::bit_cast<float>(std::uint32_t{0x3EDE4963U}), // 176: 0.434153636
    std::bit_cast<float>(std::uint32_t{0x3EE11ABFU}), // 177: 0.439657174
    std::bit_cast<float>(std::uint32_t{0x3EE3F169U}), // 178: 0.445201195
    std::bit_cast<float>(std::uint32_t{0x3EE6CD65U}), // 179: 0.450785783
    std::bit_cast<float>(std::uint32_t{0x3EE9AEB5U}), // 180: 0.456411023
    std::bit_cast<float>(std::uint32_t{0x3EEC955BU}), // 181: 0.462077000
    std::bit_cast<float>(std::uint32_t{0x3EEF815CU}), // 182: 0.467783796
    std::bit_cast<float>(std::uint32_t{0x3EF272B8U}), // 183: 0.473531496
    std::bit_cast<float>(std::uint32_t{0x3EF56974U}), // 184: 0.479320183
    std::bit_cast<float>(std::uint32_t{0x3EF86593U}), // 185: 0.485149940
    std::bit_cast<float>(std::uint32_t{0x3EFB6716U}), // 186: 0.491020850
    std::bit_cast<float>(std::uint32_t{0x3EFE6E00U}), // 187: 0.496932995
    std::bit_cast<float>(std::uint32_t{0x3F00BD2BU}), // 188: 0.502886458
    std::bit_cast<float>(std::uint32_t{0x3F02460CU}), // 189: 0.508881321
    std::bit_cast<float>(std::uint32_t{0x3F03D1A5U}), // 190: 0.514917665
    std::bit_cast<float>(std::uint32_t{0x3F055FF7U}), // 191: 0.520995573
    std::bit_cast<float>(std::uint32_t{0x3F06F104U}), // 192: 0.527115126
    std::bit_cast<float>(std::uint32_t{0x3F0884CDU}), // 193: 0.533276404
    std::bit_cast<float>(std::uint32_t{0x3F0A1B54U}), // 194: 0.539479489
    std::bit_cast<float>(std::uint32_t{0x3F0BB499U}), // 195: 0.545724461
    std::bit_cast<float>(std::uint32_t{0x3F0D509FU}), // 196: 0.552011402
    std::bit_cast<float>(std::uint32_t{0x3F0EEF65U}), // 197: 0.558340390
    std::bit_cast<float>(std::uint32_t{0x3F1090EFU}), // 198: 0.564711506
    std::bit_cast<float>(std::uint32_t{0x3F12353DU}), // 199: 0.571124829
    std::bit_cast<float>(std::uint32_t{0x3F13DC50U}), // 200: 0.577580440
    std::bit_cast<float>(std::uint32_t{0x3F15862AU}), // 201: 0.584078418
    std::bit_cast<float>(std::uint32_t{0x3F1732CCU}), // 202: 0.590618841
    std::bit_cast<float>(std::uint32_t{0x3F18E237U}), // 203: 0.597201788
    std::bit_cast<float>(std::uint32_t{0x3F1A946EU}), // 204: 0.603827339
    std::bit_cast<float>(std::uint32_t{0x3F1C4970U}), // 205: 0.610495571
    std::bit_cast<float>(std::uint32_t{0x3F1E0140U}), // 206: 0.617206562
    std::bit_cast<float>(std::uint32_t{0x3F1FBBDEU}), // 207: 0.623960392
    std::bit_cast<float>(std::uint32_t{0x3F21794DU}), // 208: 0.630757136
    std::bit_cast<float>(std::uint32_t{0x3F23398CU}), // 209: 0.637596874
    std::bit_cast<float>(std::uint32_t{0x3F24FC9FU}), // 210: 0.644479682
    std::bit_cast<float>(std::uint32_t{0x3F26C285U}), // 211: 0.651405637
    std::bit_cast<float>(std::uint32_t{0x3F288B41U}), // 212: 0.658374817
    std::bit_cast<float>(std::uint32_t{0x3F2A56D2U}), // 213: 0.665387298
    std::bit_cast<float>(std::uint32_t{0x3F2C253CU}), // 214: 0.672443157
    std::bit_cast<float>(std::uint32_t{0x3F2DF67FU}), // 215: 0.679542470
    std::bit_cast<float>(std::uint32_t{0x3F2FCA9CU}), // 216: 0.686685312
    std::bit_cast<float>(std::uint32_t{0x3F31A194U}), // 217: 0.693871761
    std::bit_cast<float>(std::uint32_t{0x3F337B6AU}), // 218: 0.701101892
    std::bit_cast<float>(std::uint32_t{0x3F35581DU}), // 219: 0.708375780
    std::bit_cast<float>(std::uint32_t{0x3F3737B0U}), // 220: 0.715693501
    std::bit_cast<float>(std::uint32_t{0x3F391A24U}), // 221: 0.723055129
    std::bit_cast<float>(std::uint32_t{0x3F3AFF7AU}), // 222: 0.730460740
    std::bit_cast<float>(std::uint32_t{0x3F3CE7B2U}), // 223: 0.737910409
    std::bit_cast<float>(std::uint32_t{0x3F3ED2CFU}), // 224: 0.745404210
    std::bit_cast<float>(std::uint32_t{0x3F40C0D2U}), // 225: 0.752942217
    std::bit_cast<float>(std::uint32_t{0x3F42B1BCU}), // 226: 0.760524505
    std::bit_cast<float>(std::uint32_t{0x3F44A58EU}), // 227: 0.768151147
    std::bit_cast<float>(std::uint32_t{0x3F469C49U}), // 228: 0.775822218
    std::bit_cast<float>(std::uint32_t{0x3F4895EFU}), // 229: 0.783537792
    std::bit_cast<float>(std::uint32_t{0x3F4A9280U}), // 230: 0.791297940
    std::bit_cast<float>(std::uint32_t{0x3F4C91FFU}), // 231: 0.799102738
    std::bit_cast<float>(std::uint32_t{0x3F4E946CU}), // 232: 0.806952258
    std::bit_cast<float>(std::uint32_t{0x3F5099C9U}), // 233: 0.814846572
    std::bit_cast<float>(std::uint32_t{0x3F52A216U}), // 234: 0.822785754
    std::bit_cast<float>(std::uint32_t{0x3F54AD56U}), // 235: 0.830769877
    std::bit_cast<float>(std::uint32_t{0x3F56BB88U}), // 236: 0.838799012
    std::bit_cast<float>(std::uint32_t{0x3F58CCAFU}), // 237: 0.846873232
    std::bit_cast<float>(std::uint32_t{0x3F5AE0CCU}), // 238: 0.854992608
    std::bit_cast<float>(std::uint32_t{0x3F5CF7DFU}), // 239: 0.863157213
    std::bit_cast<float>(std::uint32_t{0x3F5F11EAU}), // 240: 0.871367119
    std::bit_cast<float>(std::uint32_t{0x3F612EEFU}), // 241: 0.879622397
    std::bit_cast<float>(std::uint32_t{0x3F634EEEU}), // 242: 0.887923118
    std::bit_cast<float>(std::uint32_t{0x3F6571E9U}), // 243: 0.896269353
    std::bit_cast<float>(std::uint32_t{0x3F6797E0U}), // 244: 0.904661174
    std::bit_cast<float>(std::uint32_t{0x3F69C0D5U}), // 245: 0.913098652
    std::bit_cast<float>(std::uint32_t{0x3F6BECCAU}), // 246: 0.921581856
    std::bit_cast<float>(std::uint32_t{0x3F6E1BBFU}), // 247: 0.930110858
    std::bit_cast<float>(std::uint32_t{0x3F704DB5U}), // 248: 0.938685728
    std::bit_cast<float>(std::uint32_t{0x3F7282AEU}), // 249: 0.947306537
    std::bit_cast<float>(std::uint32_t{0x3F74BAABU}), // 250: 0.955973353
    std::bit_cast<float>(std::uint32_t{0x3F76F5AEU}), // 251: 0.964686248
    std::bit_cast<float>(std::uint32_t{0x3F7933B6U}), // 252: 0.973445290
    std::bit_cast<float>(std::uint32_t{0x3F7B74C6U}), // 253: 0.982250550
    std::bit_cast<float>(std::uint32_t{0x3F7DB8DEU}), // 254: 0.991102097
    std::bit_cast<float>(std::uint32_t{0x3F800000U}), // 255: 1.000000000
}};

namespace
{

constexpr std::array<std::wstring_view, 3> kSansFamilies{{L"Segoe UI Variable Text", L"Segoe UI Variable", L"Segoe UI"}}; // type.families.sans
constexpr std::array<std::wstring_view, 3> kDisplayFamilies{{L"Segoe UI Variable Display", L"Segoe UI Variable", L"Segoe UI"}}; // type.families.display
constexpr std::array<std::wstring_view, 2> kMonoFamilies{{L"Cascadia Mono", L"Consolas"}}; // type.families.mono

} // namespace

std::span<const std::wstring_view> font_families(FontFamily family) noexcept
{
    switch (family)
    {
    case FontFamily::Display:
        return kDisplayFamilies;
    case FontFamily::Mono:
        return kMonoFamilies;
    case FontFamily::Sans:
        break;
    }
    return kSansFamilies;
}

} // namespace isotone::ui::tokens
