// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// isotone::ui::Window on hidden windows: nothing here shows a window or needs a second monitor.

#include "isotone/ui/window.h"

#include <bit>
#include <cstdint>
#include <gtest/gtest.h>
#include <optional>
#include <stdexcept>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>

namespace
{

using isotone::ui::Dip;
using isotone::ui::DipSize;
using isotone::ui::Message;
using isotone::ui::PixelRect;
using isotone::ui::Window;

// Two application messages a test handler answers or fails on.
constexpr std::uint32_t kAnswered = WM_APP + 1;
constexpr std::uint32_t kThrowing = WM_APP + 2;
constexpr std::intptr_t kAnswer = 4242;

Window::Options hidden_options()
{
    constexpr DipSize kSize{.width = 400.0F, .height = 300.0F};
    return Window::Options{.title = L"isotone window test", .client_size = kSize};
}

HWND handle_of(const Window& window)
{
    return static_cast<HWND>(window.native_handle());
}

// The client area is the size asked for in DIPs, converted at the window's DPI by the one rounding rule.
TEST(Window, ClientAreaIsTheSizeAskedFor)
{
    const Window window{hidden_options()};
    ASSERT_TRUE(window.alive());
    const PixelRect client = window.client_rect();
    EXPECT_EQ(client.width(), isotone::ui::to_pixels(Dip{hidden_options().client_size.width}, window.dpi()));
    EXPECT_EQ(client.height(), isotone::ui::to_pixels(Dip{hidden_options().client_size.height}, window.dpi()));
    EXPECT_GE(window.dpi(), isotone::ui::kBaseDpi);
    EXPECT_FALSE(IsWindowVisible(handle_of(window)) != FALSE);
}

// A window whose handler asks for the DPI while the window is still being created, as a surface that lays itself
// out on WM_CREATE or answers WM_NCCALCSIZE does.
struct LayoutProbe
{
    std::uint32_t dpi_at_create = 0;
    // Last: its messages reach the member above from the moment it is created.
    Window window{hidden_options(), [this](const Message& message) -> std::optional<std::intptr_t> {
                      if (message.id == WM_CREATE)
                      {
                          dpi_at_create = window.dpi();
                      }
                      return std::nullopt;
                  }};
};

// The DPI is the monitor's from the first message on, not the 96 a window starts from before it asks.
TEST(Window, DpiIsKnownWhileTheWindowIsBeingCreated)
{
    const LayoutProbe probe;
    EXPECT_EQ(probe.dpi_at_create, GetDpiForWindow(handle_of(probe.window)));
    EXPECT_EQ(probe.window.dpi(), GetDpiForWindow(handle_of(probe.window)));
    // The test executable embeds native/ui/app.manifest, so this is the monitor's DPI and not a virtualized 96.
    EXPECT_EQ(probe.window.awareness(), isotone::ui::DpiAwareness::PerMonitorV2);
}

// A resize of the client area keeps what surrounds it: a menu bar added after creation does not eat into the size.
TEST(Window, ResizeClientGivesTheSizeAskedForUnderAMenu)
{
    Window window{hidden_options()};
    const HMENU bar = CreateMenu();
    AppendMenuW(bar, MF_STRING, 1, L"Menu");
    ASSERT_NE(SetMenu(handle_of(window), bar), FALSE);
    EXPECT_LT(window.client_rect().height(),
              isotone::ui::to_pixels(Dip{hidden_options().client_size.height}, window.dpi()));

    constexpr DipSize kSize{.width = 512.0F, .height = 384.0F};
    window.resize_client(kSize);
    EXPECT_EQ(window.client_rect().width(), isotone::ui::to_pixels(Dip{kSize.width}, window.dpi()));
    EXPECT_EQ(window.client_rect().height(), isotone::ui::to_pixels(Dip{kSize.height}, window.dpi()));
}

// Windows tells a window its new DPI and the rectangle that keeps its size in DIPs there; the window takes both.
TEST(Window, DpiChangeTakesTheSuggestedRectangle)
{
    Window window{hidden_options()};
    constexpr std::uint32_t kNewDpi = 144;
    constexpr std::uint32_t kWordBits = 16;
    RECT suggested{.left = 37, .top = 53, .right = 37 + 911, .bottom = 53 + 677};
    const WPARAM both_words = (static_cast<WPARAM>(kNewDpi) << kWordBits) | kNewDpi;
    SendMessageW(handle_of(window), WM_DPICHANGED, both_words, std::bit_cast<LPARAM>(&suggested));

    EXPECT_EQ(window.dpi(), kNewDpi);
    const PixelRect now = window.window_rect();
    EXPECT_EQ(now.left, suggested.left);
    EXPECT_EQ(now.top, suggested.top);
    EXPECT_EQ(now.width(), suggested.right - suggested.left);
    EXPECT_EQ(now.height(), suggested.bottom - suggested.top);
}

// The handler sees a message first, its answer is the message's result, and an exception it throws never crosses
// the window procedure.
TEST(Window, HandlerAnswersAndItsExceptionsStayInside)
{
    Window window{hidden_options(), [](const Message& message) -> std::optional<std::intptr_t> {
                      if (message.id == kAnswered)
                      {
                          return kAnswer;
                      }
                      if (message.id == kThrowing)
                      {
                          throw std::runtime_error{"a handler that fails"};
                      }
                      return std::nullopt;
                  }};
    EXPECT_EQ(SendMessageW(handle_of(window), kAnswered, 0, 0), kAnswer);
    EXPECT_EQ(window.handler_failures(), 0U);
    EXPECT_EQ(SendMessageW(handle_of(window), kThrowing, 0, 0), 0);
    EXPECT_EQ(window.handler_failures(), 1U);
    EXPECT_TRUE(window.alive());
}

// Closing is asked through the message queue, the window is destroyed, and the loop ends.
TEST(Window, CloseDestroysTheWindowAndEndsTheLoop)
{
    Window::Options options = hidden_options();
    options.quit_on_destroy = true;
    Window window{options};
    const HWND handle = handle_of(window);
    window.close();
    EXPECT_TRUE(window.alive());
    EXPECT_EQ(Window::run_message_loop(), 0);
    EXPECT_FALSE(window.alive());
    EXPECT_EQ(window.native_handle(), nullptr);
    EXPECT_EQ(IsWindow(handle), FALSE);
}

// A handler that answers the window's last messages itself cannot keep the window alive or its loop running: the
// window's own bookkeeping does not depend on the handler letting those messages through.
TEST(Window, AHandlerThatAnswersTheLastMessagesCannotKeepTheWindowAlive)
{
    Window::Options options = hidden_options();
    options.quit_on_destroy = true;
    Window window{options, [](const Message& message) -> std::optional<std::intptr_t> {
                      if (message.id == WM_DESTROY || message.id == WM_NCDESTROY)
                      {
                          return 0;
                      }
                      return std::nullopt;
                  }};
    // Destroyed directly, so a broken window fails the assertions below instead of waiting in a message loop.
    ASSERT_NE(DestroyWindow(handle_of(window)), FALSE);
    EXPECT_FALSE(window.alive());
    EXPECT_EQ(window.native_handle(), nullptr);
    MSG quit{};
    EXPECT_NE(PeekMessageW(&quit, nullptr, WM_QUIT, WM_QUIT, PM_REMOVE), FALSE);
}

// A handler that answers WM_DPICHANGED places the window itself, and the window still learns its new DPI.
TEST(Window, AHandlerThatAnswersTheDpiChangeStillLeavesTheNewDpi)
{
    Window window{hidden_options(), [](const Message& message) -> std::optional<std::intptr_t> {
                      return message.id == WM_DPICHANGED ? std::optional<std::intptr_t>{0} : std::nullopt;
                  }};
    constexpr std::uint32_t kNewDpi = 192;
    constexpr std::uint32_t kWordBits = 16;
    const PixelRect before = window.window_rect();
    RECT suggested{.left = 11, .top = 13, .right = 511, .bottom = 413};
    const WPARAM both_words = (static_cast<WPARAM>(kNewDpi) << kWordBits) | kNewDpi;
    SendMessageW(handle_of(window), WM_DPICHANGED, both_words, std::bit_cast<LPARAM>(&suggested));
    EXPECT_EQ(window.dpi(), kNewDpi);
    EXPECT_EQ(window.window_rect(), before);
}

// A window that goes out of scope takes its handle with it.
TEST(Window, DestructionDestroysTheHandle)
{
    HWND handle = nullptr;
    {
        const Window window{hidden_options()};
        handle = handle_of(window);
        EXPECT_NE(IsWindow(handle), FALSE);
    }
    EXPECT_EQ(IsWindow(handle), FALSE);
}

} // namespace
