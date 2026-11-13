// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include "isotone/ui/dpi.h"

#include <cstdint>
#include <functional>
#include <optional>
#include <string>

namespace isotone::ui
{

// How Windows scales a window's coordinates. An Isotone process is PerMonitorV2 through its manifest
// (native/ui/app.manifest); anything else means the executable was built without it.
enum class DpiAwareness : std::uint8_t
{
    Unaware,
    System,
    PerMonitor,
    PerMonitorV2,
    Unknown,
};

// One window message: its number and its two parameters, as the window procedure receives them.
struct Message
{
    std::uint32_t id = 0;
    std::uintptr_t wparam = 0;
    std::intptr_t lparam = 0;
};

// A top-level Win32 window of the suite: per-monitor DPI aware, taking the rectangle Windows suggests when its DPI
// changes. It owns the window handle from construction to destruction. Every member is used on the thread that
// created it (the UI thread: standards/cpp.md, Threading).
class Window
{
  public:
    struct Options
    {
        std::wstring title;
        // The client area in DIPs, converted at the DPI of the monitor the window opens on.
        DipSize client_size{};
        // Shown without activation and fully transparent, with no taskbar button: the window lives, lays out,
        // and paints like any other, and nothing appears on the desktop. For tests.
        bool quiet = false;
        // Ends the thread's message loop (PostQuitMessage) when this window is destroyed.
        bool quit_on_destroy = false;
    };

    // Sees every message first. A returned value is the message's result and stops the default handling; nothing
    // lets the window handle it. Whatever it answers, the window still takes what it must know from the message:
    // its new DPI (WM_DPICHANGED, where an answer means the handler placed the window itself), the end of its
    // message loop (WM_DESTROY), and the loss of its handle (WM_NCDESTROY). An exception it throws is caught at the
    // window procedure, counted in handler_failures(), and the message then takes the default path.
    using Handler = std::function<std::optional<std::intptr_t>(const Message& message)>;

    // Registers the window class on first use and creates the window, hidden. Throws isotone::core::Error naming
    // the failing call (RegisterClassExW, CreateWindowExW, SetWindowPos).
    explicit Window(const Options& options, Handler handler = {});
    ~Window();
    Window(const Window&) = delete;
    Window& operator=(const Window&) = delete;
    Window(Window&&) = delete;
    Window& operator=(Window&&) = delete;

    // The HWND, or null once the window is destroyed.
    [[nodiscard]] void* native_handle() const noexcept;
    [[nodiscard]] bool alive() const noexcept;

    // The window's DPI: the monitor's when it was created, then whatever WM_DPICHANGED last said.
    [[nodiscard]] std::uint32_t dpi() const noexcept;
    [[nodiscard]] DpiAwareness awareness() const noexcept;

    // The client area in pixels (left and top are 0) and the whole window in screen pixels.
    [[nodiscard]] PixelRect client_rect() const;
    [[nodiscard]] PixelRect window_rect() const;

    // Makes the client area this size in DIPs at the window's DPI, keeping whatever surrounds it (the frame, a
    // menu bar attached since the window was created). Throws isotone::core::Error.
    void resize_client(DipSize size);

    // Shows the window: activated, or as Options::quiet says.
    void show();
    // Asks the window to close, as its close button does (WM_CLOSE).
    void close();

    // How many times the handler threw.
    [[nodiscard]] std::uint32_t handler_failures() const noexcept;

    // Runs the thread's message loop until WM_QUIT and returns its exit code.
    static int run_message_loop();
    // Dispatches every message already queued and returns; false once WM_QUIT was seen.
    static bool pump_pending_messages();

    // Called by the window procedure. Not for other callers.
    std::intptr_t dispatch(void* window, const Message& message) noexcept;

  private:
    void* window_ = nullptr;
    Handler handler_;
    std::uint32_t dpi_ = kBaseDpi;
    std::uint32_t handler_failures_ = 0;
    bool quiet_ = false;
    bool quit_on_destroy_ = false;
};

} // namespace isotone::ui
