// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "host.h"

#include "isotone/core/app_paths.h"
#include "isotone/core/atomic_file.h"
#include "isotone/core/build_info.h"
#include "isotone/core/error.h"
#include "isotone/core/log.h"
#include "isotone/core/settings.h"
#include "isotone/ui/dpi.h"
#include "isotone/ui/theme.h"
#include "isotone/ui/window.h"

#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <exception>
#include <format>
#include <functional>
#include <iterator>
#include <memory>
#include <optional>
#include <span>
#include <string>
#include <string_view>
#include <thread>
#include <type_traits>
#include <utility>
#include <variant>
#include <vector>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>

namespace isotone::foundation_host
{
namespace
{

using isotone::core::Error;
using isotone::core::Log;
using isotone::core::LogLevel;
using isotone::ui::Color;
using isotone::ui::Dip;
using isotone::ui::DipRect;
using isotone::ui::DpiAwareness;
using isotone::ui::PixelRect;
using isotone::ui::Theme;
using isotone::ui::TokenKey;
using isotone::ui::Window;
using Json = nlohmann::ordered_json;

constexpr std::string_view kAppName{"FoundationHost"};
constexpr std::string_view kCommandTemplate{"Command {command} invoked"};
constexpr int kReportSchema = 1;
// The placeholder window's client area, in DIPs.
constexpr isotone::ui::DipSize kClientSize{.width = 960.0F, .height = 600.0F};
// How long a scenario waits for the window to do what was asked before it reports a failure.
constexpr std::chrono::seconds kPatience{10};
constexpr std::chrono::milliseconds kPumpPause{5};

// One placeholder command: its menu id, its label, and the name its log line carries.
struct Command
{
    std::uint32_t id = 0;
    const wchar_t* label = nullptr;
    std::string_view name;
};

struct Menu
{
    const wchar_t* label = nullptr;
    std::array<Command, 2> commands;
};

// The placeholder menu bar: four menus with two commands each. The real menus are the Isotone title bar's (§3).
constexpr std::array<Menu, 4> kMenus{{
    {.label = L"&File",
     .commands = {{{.id = 1001, .label = L"&New", .name = "file.new"},
                   {.id = 1002, .label = L"&Open...", .name = "file.open"}}}},
    {.label = L"&Edit",
     .commands = {{{.id = 1101, .label = L"&Undo", .name = "edit.undo"},
                   {.id = 1102, .label = L"&Redo", .name = "edit.redo"}}}},
    {.label = L"&View",
     .commands = {{{.id = 1201, .label = L"Zoom &In", .name = "view.zoom-in"},
                   {.id = 1202, .label = L"Zoom &Out", .name = "view.zoom-out"}}}},
    {.label = L"&Help",
     .commands = {{{.id = 1301, .label = L"&Contents", .name = "help.contents"},
                   {.id = 1302, .label = L"&About", .name = "help.about"}}}},
}};

std::string utf8(std::wstring_view text)
{
    if (text.empty())
    {
        return {};
    }
    const int size =
        WideCharToMultiByte(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), nullptr, 0, nullptr, nullptr);
    std::string converted(static_cast<std::size_t>(size > 0 ? size : 0), '\0');
    WideCharToMultiByte(CP_UTF8, 0, text.data(), static_cast<int>(text.size()), converted.data(), size, nullptr,
                        nullptr);
    return converted;
}

std::string hex(Color color)
{
    return std::format("#{:02x}{:02x}{:02x}", color.red, color.green, color.blue);
}

std::string_view awareness_name(DpiAwareness awareness) noexcept
{
    switch (awareness)
    {
    case DpiAwareness::PerMonitorV2:
        return "per-monitor-v2";
    case DpiAwareness::PerMonitor:
        return "per-monitor";
    case DpiAwareness::System:
        return "system";
    case DpiAwareness::Unaware:
        return "unaware";
    case DpiAwareness::Unknown:
        break;
    }
    return "unknown";
}

// What a run works with: the log, the settings, and the switches.
struct Context
{
    Arguments arguments;
    Log* log = nullptr;
};

template <typename Value> Value token(const Theme& theme, TokenKey key)
{
    return std::get<Value>(theme.resolve(key));
}

// GDI resources, released when they go out of scope.
struct BrushDeleter
{
    void operator()(HBRUSH brush) const noexcept
    {
        DeleteObject(brush);
    }
};
using Brush = std::unique_ptr<std::remove_pointer_t<HBRUSH>, BrushDeleter>;

COLORREF colorref(Color color) noexcept
{
    constexpr unsigned kGreenShift = 8;
    constexpr unsigned kBlueShift = 16;
    return static_cast<COLORREF>(color.red) | (static_cast<COLORREF>(color.green) << kGreenShift) |
           (static_cast<COLORREF>(color.blue) << kBlueShift);
}

void fill(HDC surface, const PixelRect& rect, Color color)
{
    const Brush brush{CreateSolidBrush(colorref(color))};
    const RECT area{.left = rect.left, .top = rect.top, .right = rect.right, .bottom = rect.bottom};
    FillRect(surface, &area, brush.get());
}

// The host's window: the placeholder menu bar and two placeholder panels laid out in DIPs and filled with token
// colors. GDI stands in until the renderer (§2) draws them.
class HostWindow
{
  public:
    explicit HostWindow(Context& context, bool quiet, bool quit_on_destroy)
        : context_{&context}, window_{make_options(context, quiet, quit_on_destroy),
                                      [this](const isotone::ui::Message& message) { return handle(message); }}
    {
        attach_menu();
        // The menu bar took its height out of the client area: give the client area back the size that was asked.
        window_.resize_client(kClientSize);
        layout();
    }

    [[nodiscard]] Window& window() noexcept
    {
        return window_;
    }
    [[nodiscard]] HWND handle() const noexcept
    {
        return static_cast<HWND>(window_.native_handle());
    }
    [[nodiscard]] const PixelRect& left_panel() const noexcept
    {
        return left_;
    }
    [[nodiscard]] const PixelRect& right_panel() const noexcept
    {
        return right_;
    }
    [[nodiscard]] int layouts() const noexcept
    {
        return layouts_;
    }
    [[nodiscard]] int paints() const noexcept
    {
        return paints_;
    }
    [[nodiscard]] Color left_color() const
    {
        return token<Color>(theme_, TokenKey::SurfacePanel);
    }
    [[nodiscard]] Color right_color() const
    {
        return token<Color>(theme_, TokenKey::SurfaceTabstrip);
    }

    // Fills the client area: the frame, then the two panels.
    void paint(HDC surface) const
    {
        fill(surface, window_.client_rect(), token<Color>(theme_, TokenKey::Frame));
        fill(surface, left_, left_color());
        fill(surface, right_, right_color());
    }

  private:
    static Window::Options make_options(const Context& context, bool quiet, bool quit_on_destroy)
    {
        if (context.arguments.fail_window)
        {
            // The --fail-window test switch: the creation fails as CreateWindowExW would when Windows refuses.
            throw Error{"CreateWindowExW", ERROR_NOT_ENOUGH_MEMORY, "creating the host window (--fail-window)"};
        }
        return Window::Options{.title = L"Isotone foundation host",
                               .client_size = kClientSize,
                               .quiet = quiet,
                               .quit_on_destroy = quit_on_destroy};
    }

    void attach_menu() const
    {
        const HMENU bar = CreateMenu();
        if (bar == nullptr)
        {
            throw Error{"CreateMenu", GetLastError(), "building the placeholder menu bar"};
        }
        for (const Menu& menu : kMenus)
        {
            const HMENU popup = CreatePopupMenu();
            for (const Command& command : menu.commands)
            {
                AppendMenuW(popup, MF_STRING, command.id, command.label);
            }
            AppendMenuW(bar, MF_POPUP, std::bit_cast<UINT_PTR>(popup), menu.label);
        }
        // The window owns the menu from here and destroys it with itself.
        if (SetMenu(handle(), bar) == FALSE)
        {
            const DWORD code = GetLastError();
            DestroyMenu(bar);
            throw Error{"SetMenu", code, "attaching the placeholder menu bar"};
        }
    }

    // The two panels in DIPs, converted by their edges: a fixed-width panel on the left, the rest on the right,
    // with one gap around and between them.
    void layout()
    {
        const std::uint32_t dpi = window_.dpi();
        const DipRect client = isotone::ui::to_dips(window_.client_rect(), dpi);
        const auto gap = token<float>(theme_, TokenKey::Space1);
        const float split = gap + token<float>(theme_, TokenKey::PanelWDefault);
        left_ = isotone::ui::to_pixels(DipRect{.left = gap, .top = gap, .right = split, .bottom = client.bottom - gap},
                                       dpi);
        right_ = isotone::ui::to_pixels(
            DipRect{.left = split + gap, .top = gap, .right = client.right - gap, .bottom = client.bottom - gap}, dpi);
        ++layouts_;
    }

    std::optional<std::intptr_t> handle(const isotone::ui::Message& message)
    {
        constexpr std::uintptr_t kLowWord = 0xFFFF;
        if (message.id == WM_COMMAND && message.lparam == 0)
        {
            return command(static_cast<std::uint32_t>(message.wparam & kLowWord));
        }
        if (message.id == WM_SIZE && window_.alive())
        {
            layout();
            InvalidateRect(handle(), nullptr, TRUE);
            return 0;
        }
        if (message.id == WM_PAINT)
        {
            PAINTSTRUCT painting{};
            const HDC surface = BeginPaint(handle(), &painting);
            paint(surface);
            EndPaint(handle(), &painting);
            ++paints_;
            return 0;
        }
        if (message.id == WM_PRINTCLIENT)
        {
            paint(std::bit_cast<HDC>(message.wparam));
            return 0;
        }
        if (message.id == WM_ERASEBKGND)
        {
            // The paint covers the whole client area.
            return 1;
        }
        return std::nullopt;
    }

    // A menu command: one log line names it. The placeholders do nothing else.
    std::optional<std::intptr_t> command(std::uint32_t command_id)
    {
        for (const Menu& menu : kMenus)
        {
            for (const Command& candidate : menu.commands)
            {
                if (candidate.id == command_id)
                {
                    context_->log->write(LogLevel::Information, kCommandTemplate,
                                         {{"command", std::string{candidate.name}}});
                    return 0;
                }
            }
        }
        return std::nullopt;
    }

    Context* context_;
    Theme theme_;
    PixelRect left_;
    PixelRect right_;
    int layouts_ = 0;
    int paints_ = 0;
    // Last: its messages reach the members above from the moment it is created.
    Window window_;
};

// The newest log event's command name, when the newest event is a command line.
std::optional<std::string> last_command(const Log& log)
{
    const auto events = log.recent();
    if (events.empty() || events.back().message_template != kCommandTemplate || events.back().fields.empty())
    {
        return std::nullopt;
    }
    const auto* name = std::get_if<std::string>(&events.back().fields.front().value);
    return name == nullptr ? std::nullopt : std::optional<std::string>{*name};
}

void measure_window(const HostWindow& host, const Window& window, Report& report)
{
    const std::uint32_t dpi = window.dpi();
    const PixelRect client = window.client_rect();
    const DipRect client_dips = isotone::ui::to_dips(client, dpi);
    report.measure("dpi", dpi);
    report.measure("scale_percent", isotone::ui::scale_percent(dpi));
    report.measure("dpi_awareness", awareness_name(window.awareness()));
    report.measure("client_width_px", client.width());
    report.measure("client_height_px", client.height());
    report.measure("client_width_dip", client_dips.right);
    report.measure("client_height_dip", client_dips.bottom);
    report.measure("layouts", host.layouts());
    if (client.width() != isotone::ui::to_pixels(Dip{kClientSize.width}, dpi) ||
        client.height() != isotone::ui::to_pixels(Dip{kClientSize.height}, dpi))
    {
        report.fail(std::format("the client area is {} x {} px, not the {} x {} DIPs asked for at {} DPI",
                                client.width(), client.height(), kClientSize.width, kClientSize.height, dpi));
    }
    if (window.awareness() != DpiAwareness::PerMonitorV2)
    {
        report.fail(std::format("the window's DPI awareness is {}, not per-monitor-v2: the executable was built "
                                "without native/ui/app.manifest",
                                awareness_name(window.awareness())));
    }
}

// Reads the menu bar back from the window and invokes every command through the window's own message path.
void check_menus(HostWindow& host, const Log& log, Report& report)
{
    Json menus = Json::array();
    const HMENU bar = GetMenu(host.handle());
    if (bar == nullptr || GetMenuItemCount(bar) != static_cast<int>(kMenus.size()))
    {
        report.fail(std::format("the menu bar has {} menus, not {}", bar == nullptr ? 0 : GetMenuItemCount(bar),
                                kMenus.size()));
        return;
    }
    for (std::size_t index = 0; index < kMenus.size(); ++index)
    {
        const HMENU popup = GetSubMenu(bar, static_cast<int>(index));
        const Menu& expected = kMenus.at(index);
        Json commands = Json::array();
        if (popup == nullptr || GetMenuItemCount(popup) != static_cast<int>(expected.commands.size()))
        {
            report.fail(std::format("the menu {} does not hold its {} commands", utf8(expected.label),
                                    expected.commands.size()));
            continue;
        }
        for (std::size_t item = 0; item < expected.commands.size(); ++item)
        {
            const Command& command = expected.commands.at(item);
            const UINT menu_id = GetMenuItemID(popup, static_cast<int>(item));
            SendMessageW(host.handle(), WM_COMMAND, menu_id, 0);
            const auto logged = last_command(log);
            if (menu_id != command.id || logged != std::string{command.name})
            {
                report.fail(std::format("the command {} (menu_id {}) logged {} when invoked", command.name, menu_id,
                                        logged.value_or("nothing")));
            }
            commands.push_back(command.name);
        }
        menus.push_back(Json{{"label", utf8(expected.label)}, {"commands", std::move(commands)}});
    }
    report.measure("menus", std::move(menus));
}

struct SurfaceDeleter
{
    void operator()(HDC surface) const noexcept
    {
        DeleteDC(surface);
    }
};
struct BitmapDeleter
{
    void operator()(HBITMAP bitmap) const noexcept
    {
        DeleteObject(bitmap);
    }
};

std::optional<Color> pixel_at(HDC surface, POINT position)
{
    constexpr unsigned kByte = 0xFF;
    constexpr unsigned kGreenShift = 8;
    constexpr unsigned kBlueShift = 16;
    const COLORREF value = GetPixel(surface, position.x, position.y);
    if (value == CLR_INVALID)
    {
        return std::nullopt;
    }
    return Color{.red = static_cast<std::uint8_t>(value & kByte),
                 .green = static_cast<std::uint8_t>((value >> kGreenShift) & kByte),
                 .blue = static_cast<std::uint8_t>((value >> kBlueShift) & kByte),
                 .alpha = UINT8_MAX};
}

// One placeholder panel as a check sees it: its name, where it is, and the color its token gives.
struct Panel
{
    std::string_view name;
    PixelRect area;
    Color color;
};

// Whether the middle of a panel, as the window painted it, has the panel's token color.
void check_panel(HDC surface, const Panel& panel, Json& panels, Report& report)
{
    const PixelRect& area = panel.area;
    Json entry{{"left_px", area.left},
               {"top_px", area.top},
               {"right_px", area.right},
               {"bottom_px", area.bottom},
               {"expected", hex(panel.color)}};
    const auto painted = pixel_at(surface, POINT{.x = (area.left + area.right) / 2, .y = (area.top + area.bottom) / 2});
    entry.emplace("painted", painted ? hex(*painted) : std::string{"nothing"});
    if (area.width() <= 0 || area.height() <= 0 || !painted || hex(*painted) != hex(panel.color))
    {
        report.fail(std::format("the {} panel is painted {} where its token gives {}", panel.name,
                                painted ? hex(*painted) : "nothing", hex(panel.color)));
    }
    panels.emplace(std::string{panel.name}, std::move(entry));
}

// Renders the client area to a memory surface through WM_PRINTCLIENT, the same paint the screen gets, and checks
// both panels.
void check_painting(HostWindow& host, Report& report)
{
    const PixelRect client = host.window().client_rect();
    const HDC screen = GetDC(host.handle());
    const std::unique_ptr<std::remove_pointer_t<HDC>, SurfaceDeleter> surface{CreateCompatibleDC(screen)};
    const std::unique_ptr<std::remove_pointer_t<HBITMAP>, BitmapDeleter> bitmap{
        CreateCompatibleBitmap(screen, client.width(), client.height())};
    ReleaseDC(host.handle(), screen);
    if (!surface || !bitmap)
    {
        report.fail("no memory surface could be made to render the window into");
        return;
    }
    const HGDIOBJ previous = SelectObject(surface.get(), bitmap.get());
    SendMessageW(host.handle(), WM_PRINTCLIENT, std::bit_cast<WPARAM>(surface.get()), PRF_CLIENT);
    Json panels = Json::object();
    check_panel(surface.get(), Panel{.name = "left", .area = host.left_panel(), .color = host.left_color()}, panels,
                report);
    check_panel(surface.get(), Panel{.name = "right", .area = host.right_panel(), .color = host.right_color()}, panels,
                report);
    report.measure("panels", std::move(panels));
    SelectObject(surface.get(), previous);
}

// smoke: the window exists with the right awareness and size, its menus hold their commands and each command
// reaches the log, and both panels paint with their token colors. The window stays hidden.
Report run_smoke(Context& context)
{
    Report report{.scenario = "smoke"};
    HostWindow host{context, false, false};
    measure_window(host, host.window(), report);
    check_menus(host, *context.log, report);
    check_painting(host, report);
    return report;
}

// Pumps messages until done() is true or the patience runs out.
bool pump_until(const std::function<bool()>& done)
{
    const auto deadline = std::chrono::steady_clock::now() + kPatience;
    while (!done())
    {
        if (!Window::pump_pending_messages() || std::chrono::steady_clock::now() >= deadline)
        {
            return done();
        }
        std::this_thread::sleep_for(kPumpPause);
    }
    return true;
}

// lifecycle: the window is shown (quietly: transparent, not activated), paints, is resized and lays out and paints
// again, is closed, and is destroyed with its message loop ended.
Report run_lifecycle(Context& context)
{
    Report report{.scenario = "lifecycle"};
    if (display_session() == DisplaySession::Absent)
    {
        report.result = "no-display";
        report.failures.emplace_back("the process has no visible window station, so a shown window is never painted");
        return report;
    }
    HostWindow host{context, true, true};
    Window& window = host.window();
    window.show();
    if (!pump_until([&host] { return host.paints() > 0; }))
    {
        report.fail("the shown window was not painted");
    }
    const int layouts_before = host.layouts();
    const int paints_before = host.paints();
    const PixelRect before = window.window_rect();
    constexpr std::int32_t kGrow = 120;
    SetWindowPos(host.handle(), nullptr, 0, 0, before.width() + kGrow, before.height() + kGrow,
                 SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE);
    if (!pump_until([&host, paints_before] { return host.paints() > paints_before; }))
    {
        report.fail("the resized window was not painted again");
    }
    if (host.layouts() <= layouts_before || window.window_rect().width() != before.width() + kGrow)
    {
        report.fail("the resize did not lay the panels out again");
    }
    report.measure("paints", host.paints());
    report.measure("layouts", host.layouts());
    report.measure("resized_width_px", window.window_rect().width());
    window.close();
    const int loop_result = Window::run_message_loop();
    report.measure("loop_exit_code", loop_result);
    report.measure("destroyed", !window.alive());
    if (window.alive())
    {
        report.fail("the closed window was not destroyed");
    }
    return report;
}

// The interactive host: the window on screen until the user closes it.
Report run_interactive(Context& context)
{
    Report report{.scenario = "interactive"};
    HostWindow host{context, false, true};
    host.window().show();
    report.measure("loop_exit_code", Window::run_message_loop());
    return report;
}

struct Scenario
{
    std::string_view name;
    Report (*run)(Context&);
};

constexpr std::array<Scenario, 2> kScenarios{
    {{.name = "lifecycle", .run = run_lifecycle}, {.name = "smoke", .run = run_smoke}}};

std::filesystem::path path_of(const std::wstring& text)
{
    return std::filesystem::path{text};
}

int exit_code_of(const Report& report) noexcept
{
    if (report.result == "pass")
    {
        return kExitPass;
    }
    return report.result == "no-display" ? kExitNoDisplay : kExitFail;
}

// Writes the report as one JSON object, atomically. Throws Error when it cannot be written.
void write_report(const std::filesystem::path& file, const Report& report)
{
    Json document = Json::object();
    document.emplace("schema_version", Json(kReportSchema));
    document.emplace("scenario", Json(report.scenario));
    document.emplace("result", Json(report.result));
    document.emplace("failures", Json(report.failures));
    document.emplace("measurements", Json(report.measurements));
    document.emplace("build_id", Json(std::string{isotone::core::build_id()}));
    const std::string text = document.dump(2) + "\n";
    isotone::core::AtomicFile{file}.write(std::as_bytes(std::span{text}));
}

void say(std::string_view sentence) noexcept
{
    std::fputs("foundation-host: ", stderr);
    std::fwrite(sentence.data(), 1, sentence.size(), stderr);
    std::fputc('\n', stderr);
}

// Runs the scenario with the host's log and settings under the data root, and returns its report.
// Opens the host's log and settings under the data root and runs the scenario. Throws when the log or the settings
// cannot be kept there.
Report run_with_data(const Arguments& arguments, const std::string& name, Report (*run)(Context&))
{
    const auto real = isotone::core::AppFolderSources::from_windows();
    const auto folders = isotone::core::resolve_app_folders(
        kAppName, isotone::core::AppFolderSources{.local_app_data = arguments.data_root,
                                                  .executable_folder = real.executable_folder});
    isotone::core::LogConfig log_config;
    log_config.app_name = std::string{kAppName};
    log_config.folder = folders.logs;
    log_config.outputs = {.file = true, .memory = true, .debugger = false};
    Log log{std::move(log_config)};
    isotone::core::Settings settings{folders.settings, log};
    settings.set("host.last-scenario", name);
    Context context{.arguments = arguments, .log = &log};
    try
    {
        return run(context);
    }
    catch (const Error& error)
    {
        // The window could not be made or driven: a skip only without a display, a failure with one.
        Report report{.scenario = name};
        report.result = exit_code_without_window(display_session()) == kExitNoDisplay ? "no-display" : "fail";
        report.failures.emplace_back(error.what());
        return report;
    }
}

// Runs the scenario and returns its report. A failure to start (a data root the log or the settings cannot be kept
// under) is a failing report like any other, so the caller's --report file always says what happened.
Report run_scenario(const Arguments& arguments, Report (*run)(Context&))
{
    const std::string name = arguments.scenario.empty() ? std::string{"interactive"} : arguments.scenario;
    try
    {
        return run_with_data(arguments, name, run);
    }
    catch (const std::exception& error)
    {
        Report report{.scenario = name};
        report.fail(std::format("the host could not keep its log and settings under the data root: {}", error.what()));
        return report;
    }
}

int run_checked(std::span<const std::wstring> arguments)
{
    Arguments parsed;
    if (const auto problem = parse_arguments(arguments, parsed))
    {
        say(*problem);
        return kExitUsage;
    }
    Report (*run)(Context&) = run_interactive;
    if (!parsed.scenario.empty())
    {
        const auto found = std::ranges::find_if(
            kScenarios, [&parsed](const Scenario& scenario) { return scenario.name == parsed.scenario; });
        if (found == kScenarios.end())
        {
            say(std::format("unknown scenario \"{}\"; the scenarios are lifecycle and smoke", parsed.scenario));
            return kExitUsage;
        }
        run = found->run;
    }
    const Report report = run_scenario(parsed, run);
    for (const std::string& failure : report.failures)
    {
        say(failure);
    }
    if (!parsed.report.empty())
    {
        try
        {
            write_report(parsed.report, report);
        }
        catch (const Error& error)
        {
            say(std::format("the report could not be written: {}", error.what()));
            return kExitUsage;
        }
    }
    return exit_code_of(report);
}

} // namespace

DisplaySession display_session() noexcept
{
    const HWINSTA station = GetProcessWindowStation();
    USEROBJECTFLAGS flags{};
    DWORD needed = 0;
    if (station == nullptr || GetUserObjectInformationW(station, UOI_FLAGS, &flags, sizeof(flags), &needed) == FALSE)
    {
        return DisplaySession::Visible;
    }
    return (flags.dwFlags & WSF_VISIBLE) != 0 ? DisplaySession::Visible : DisplaySession::Absent;
}

std::optional<std::string> parse_arguments(std::span<const std::wstring> arguments, Arguments& parsed)
{
    for (auto argument = arguments.begin(); argument != arguments.end(); ++argument)
    {
        const std::wstring& name = *argument;
        if (name == L"--fail-window")
        {
            parsed.fail_window = true;
            continue;
        }
        if (name != L"--scenario" && name != L"--report" && name != L"--data-root")
        {
            return std::format("unknown switch \"{}\"; the switches are --scenario <name>, --report <path>, "
                               "--data-root <folder>, and --fail-window",
                               utf8(name));
        }
        if (std::next(argument) == arguments.end())
        {
            return std::format("the switch {} needs a value", utf8(name));
        }
        const std::wstring& value = *++argument;
        if (name == L"--scenario")
        {
            parsed.scenario = utf8(value);
        }
        else if (name == L"--report")
        {
            parsed.report = path_of(value);
        }
        else
        {
            parsed.data_root = path_of(value);
        }
    }
    if (parsed.data_root.empty())
    {
        return std::string{"--data-root <folder> is required: the host keeps its log and settings there and never "
                           "in the user's own app-data folder"};
    }
    return std::nullopt;
}

void Report::measure(const std::string& key, nlohmann::ordered_json value)
{
    measurements.emplace(key, std::move(value));
}

void Report::fail(std::string sentence)
{
    result = "fail";
    failures.push_back(std::move(sentence));
}

std::vector<std::string_view> scenario_names()
{
    std::vector<std::string_view> names;
    names.reserve(kScenarios.size());
    for (const Scenario& scenario : kScenarios)
    {
        names.push_back(scenario.name);
    }
    return names;
}

int run_host(std::span<const std::wstring> arguments) noexcept
{
    try
    {
        return run_checked(arguments);
    }
    catch (const std::exception& error)
    {
        say(error.what());
    }
    catch (...)
    {
        say("an unknown failure ended the run");
    }
    return kExitFail;
}

} // namespace isotone::foundation_host
