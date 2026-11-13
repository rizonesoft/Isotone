// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/ui/window.h"

#include "isotone/core/error.h"

#include <bit>
#include <cstdint>
#include <mutex>
#include <optional>
#include <utility>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>

namespace isotone::ui
{
namespace
{

using isotone::core::Error;

constexpr const wchar_t* kClassName = L"IsotoneWindow";
// WM_DPICHANGED carries the new DPI in both words of wParam; the high word is the vertical one.
constexpr std::uintptr_t kWordBits = 16;
constexpr std::uintptr_t kWordMask = 0xFFFF;
// The system's arrow cursor (IDC_ARROW).
constexpr std::uintptr_t kArrowCursor = 32512;

HWND handle_of(void* window) noexcept
{
    return static_cast<HWND>(window);
}

// The window procedure of every Isotone window: it finds the Window object and hands the message over. Nothing is
// thrown across it (standards/cpp.md, Errors): Window::dispatch is noexcept.
LRESULT CALLBACK window_procedure(HWND window, UINT message, WPARAM wparam, LPARAM lparam) noexcept
{
    if (message == WM_NCCREATE)
    {
        // The first message a window gets that carries the creation parameter: the Window that is creating it.
        const auto* create = std::bit_cast<const CREATESTRUCTW*>(lparam);
        SetWindowLongPtrW(window, GWLP_USERDATA, std::bit_cast<LONG_PTR>(create->lpCreateParams));
    }
    auto* self = std::bit_cast<Window*>(GetWindowLongPtrW(window, GWLP_USERDATA));
    if (self == nullptr)
    {
        return DefWindowProcW(window, message, wparam, lparam);
    }
    return self->dispatch(window, Message{.id = message, .wparam = wparam, .lparam = lparam});
}

// Registers the window class once for the process. Throws Error when Windows refuses.
void register_window_class()
{
    static std::once_flag once;
    static DWORD failure = ERROR_SUCCESS;
    std::call_once(once, [] {
        WNDCLASSEXW window_class{};
        window_class.cbSize = sizeof(window_class);
        window_class.style = CS_HREDRAW | CS_VREDRAW;
        window_class.lpfnWndProc = window_procedure;
        window_class.hInstance = GetModuleHandleW(nullptr);
        // The standard arrow, named by its resource number: IDC_ARROW is a macro that spells it for one character
        // set, and this code calls the wide functions by name.
        window_class.hCursor = LoadCursorW(nullptr, std::bit_cast<LPCWSTR>(kArrowCursor));
        window_class.lpszClassName = kClassName;
        if (RegisterClassExW(&window_class) == 0)
        {
            failure = GetLastError();
        }
    });
    if (failure != ERROR_SUCCESS)
    {
        throw Error{"RegisterClassExW", failure, "registering the Isotone window class"};
    }
}

PixelRect to_pixel_rect(const RECT& rect) noexcept
{
    return PixelRect{.left = rect.left, .top = rect.top, .right = rect.right, .bottom = rect.bottom};
}

} // namespace

Window::Window(const Options& options, Handler handler)
    : handler_{std::move(handler)}, quiet_{options.quiet}, quit_on_destroy_{options.quit_on_destroy}
{
    register_window_class();
    const DWORD extended_style = quiet_ ? WS_EX_LAYERED | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW : 0;
    const HWND window =
        CreateWindowExW(extended_style, kClassName, options.title.c_str(), WS_OVERLAPPEDWINDOW, CW_USEDEFAULT,
                        CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, nullptr, nullptr, GetModuleHandleW(nullptr), this);
    if (window == nullptr)
    {
        throw Error{"CreateWindowExW", GetLastError(), "creating a window"};
    }
    window_ = window;
    try
    {
        if (quiet_ && SetLayeredWindowAttributes(window, 0, 0, LWA_ALPHA) == FALSE)
        {
            throw Error{"SetLayeredWindowAttributes", GetLastError(), "making a quiet window transparent"};
        }
        resize_client(options.client_size);
    }
    catch (...)
    {
        DestroyWindow(window);
        throw;
    }
}

Window::~Window()
{
    if (window_ != nullptr)
    {
        DestroyWindow(handle_of(window_));
    }
}

void* Window::native_handle() const noexcept
{
    return window_;
}

bool Window::alive() const noexcept
{
    return window_ != nullptr;
}

std::uint32_t Window::dpi() const noexcept
{
    return dpi_;
}

DpiAwareness Window::awareness() const noexcept
{
    if (window_ == nullptr)
    {
        return DpiAwareness::Unknown;
    }
    const DPI_AWARENESS_CONTEXT context = GetWindowDpiAwarenessContext(handle_of(window_));
    if (AreDpiAwarenessContextsEqual(context, DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2) != FALSE)
    {
        return DpiAwareness::PerMonitorV2;
    }
    if (AreDpiAwarenessContextsEqual(context, DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE) != FALSE)
    {
        return DpiAwareness::PerMonitor;
    }
    if (AreDpiAwarenessContextsEqual(context, DPI_AWARENESS_CONTEXT_SYSTEM_AWARE) != FALSE)
    {
        return DpiAwareness::System;
    }
    if (AreDpiAwarenessContextsEqual(context, DPI_AWARENESS_CONTEXT_UNAWARE) != FALSE ||
        AreDpiAwarenessContextsEqual(context, DPI_AWARENESS_CONTEXT_UNAWARE_GDISCALED) != FALSE)
    {
        return DpiAwareness::Unaware;
    }
    return DpiAwareness::Unknown;
}

PixelRect Window::client_rect() const
{
    RECT rect{};
    if (GetClientRect(handle_of(window_), &rect) == FALSE)
    {
        throw Error{"GetClientRect", GetLastError(), "reading the window's client area"};
    }
    return to_pixel_rect(rect);
}

PixelRect Window::window_rect() const
{
    RECT rect{};
    if (GetWindowRect(handle_of(window_), &rect) == FALSE)
    {
        throw Error{"GetWindowRect", GetLastError(), "reading the window's rectangle"};
    }
    return to_pixel_rect(rect);
}

void Window::resize_client(DipSize size)
{
    const std::int32_t wanted_width = to_pixels(Dip{size.width}, dpi_);
    const std::int32_t wanted_height = to_pixels(Dip{size.height}, dpi_);
    if (wanted_width <= 0 || wanted_height <= 0)
    {
        return;
    }
    // Whatever surrounds the client area now (the frame, the caption, a menu bar) stays as it is: the window grows
    // or shrinks by the difference between the client area it has and the one that is wanted.
    const PixelRect outer = window_rect();
    const PixelRect client = client_rect();
    if (SetWindowPos(handle_of(window_), nullptr, 0, 0, outer.width() - client.width() + wanted_width,
                     outer.height() - client.height() + wanted_height,
                     SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE) == FALSE)
    {
        throw Error{"SetWindowPos", GetLastError(), "sizing the window's client area"};
    }
}

void Window::show()
{
    ShowWindow(handle_of(window_), quiet_ ? SW_SHOWNOACTIVATE : SW_SHOW);
}

void Window::close()
{
    if (window_ != nullptr && PostMessageW(handle_of(window_), WM_CLOSE, 0, 0) == FALSE)
    {
        throw Error{"PostMessageW", GetLastError(), "asking the window to close"};
    }
}

std::uint32_t Window::handler_failures() const noexcept
{
    return handler_failures_;
}

int Window::run_message_loop()
{
    MSG message{};
    for (;;)
    {
        const BOOL result = GetMessageW(&message, nullptr, 0, 0);
        if (result == 0)
        {
            return static_cast<int>(message.wParam);
        }
        if (result < 0)
        {
            throw Error{"GetMessageW", GetLastError(), "running the message loop"};
        }
        TranslateMessage(&message);
        DispatchMessageW(&message);
    }
}

bool Window::pump_pending_messages()
{
    MSG message{};
    while (PeekMessageW(&message, nullptr, 0, 0, PM_REMOVE) != FALSE)
    {
        if (message.message == WM_QUIT)
        {
            return false;
        }
        TranslateMessage(&message);
        DispatchMessageW(&message);
    }
    return true;
}

std::intptr_t Window::dispatch(void* window, const Message& message) noexcept
{
    const HWND handle = handle_of(window);
    if (message.id == WM_NCCREATE)
    {
        // Messages arrive while CreateWindowExW is still running, before the constructor has the handle: the handle
        // and the DPI are known from this first message on, so a handler that lays out on WM_CREATE has both.
        window_ = window;
        dpi_ = GetDpiForWindow(handle);
    }
    if (handler_)
    {
        try
        {
            if (const std::optional<std::intptr_t> result = handler_(message))
            {
                return *result;
            }
        }
        catch (...)
        {
            // Nothing crosses the window procedure: the failure is counted and the message takes the default path.
            ++handler_failures_;
        }
    }
    if (message.id == WM_DPICHANGED)
    {
        // Windows suggests the rectangle that keeps the window's size in DIPs at the new DPI: take it as given.
        dpi_ = static_cast<std::uint32_t>((message.wparam >> kWordBits) & kWordMask);
        const auto* suggested = std::bit_cast<const RECT*>(message.lparam);
        SetWindowPos(handle, nullptr, suggested->left, suggested->top, suggested->right - suggested->left,
                     suggested->bottom - suggested->top, SWP_NOZORDER | SWP_NOACTIVATE);
        return 0;
    }
    if (message.id == WM_DESTROY && quit_on_destroy_)
    {
        PostQuitMessage(0);
    }
    if (message.id == WM_NCDESTROY)
    {
        // The last message: the handle is gone after it.
        window_ = nullptr;
        SetWindowLongPtrW(handle, GWLP_USERDATA, 0);
    }
    return DefWindowProcW(handle, message.id, message.wparam, message.lparam);
}

} // namespace isotone::ui
