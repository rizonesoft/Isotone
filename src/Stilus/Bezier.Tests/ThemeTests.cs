namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Services;

public class ThemeTests
{
    [Fact]
    public void Theme_DefaultProperties()
    {
        var theme = new Theme();

        Assert.Equal("Default", theme.Name);
        Assert.True(theme.IsDark);
        Assert.False(theme.UseCustomAccent);
    }

    [Fact]
    public void Theme_EffectiveAccent_ReturnsThemeAccent_WhenNoCustom()
    {
        var theme = CatppuccinThemes.Mocha;

        Assert.Equal(theme.Colors.Accent, theme.EffectiveAccent);
    }

    [Fact]
    public void Theme_EffectiveAccent_ReturnsCustomAccent_WhenSet()
    {
        var theme = CatppuccinThemes.Mocha;
        theme.CustomAccent = 0xFFFF0000;
        theme.UseCustomAccent = true;

        Assert.Equal(0xFFFF0000u, theme.EffectiveAccent);
    }

    [Fact]
    public void Theme_AccentText_ReturnsBlack_ForLightAccent()
    {
        var theme = new Theme();
        theme.CustomAccent = 0xFFFFFFFF; // White
        theme.UseCustomAccent = true;

        Assert.Equal(0xFF000000u, theme.AccentText);
    }

    [Fact]
    public void Theme_AccentText_ReturnsWhite_ForDarkAccent()
    {
        var theme = new Theme();
        theme.CustomAccent = 0xFF000000; // Black
        theme.UseCustomAccent = true;

        Assert.Equal(0xFFFFFFFFu, theme.AccentText);
    }
}

public class CatppuccinThemesTests
{
    [Fact]
    public void Mocha_IsDarkTheme()
    {
        var theme = CatppuccinThemes.Mocha;

        Assert.True(theme.IsDark);
        Assert.Equal("catppuccin-mocha", theme.Id);
    }

    [Fact]
    public void Mocha_HasCorrectColors()
    {
        var theme = CatppuccinThemes.Mocha;

        Assert.Equal(0xFF1E1E2Eu, theme.Colors.Background);
        Assert.Equal(0xFF313244u, theme.Colors.Surface);
        Assert.Equal(0xFFCDD6F4u, theme.Colors.Text);
        Assert.Equal(0xFF89B4FAu, theme.Colors.Accent);
    }

    [Fact]
    public void Latte_IsLightTheme()
    {
        var theme = CatppuccinThemes.Latte;

        Assert.False(theme.IsDark);
        Assert.Equal("catppuccin-latte", theme.Id);
    }

    [Fact]
    public void Latte_HasCorrectColors()
    {
        var theme = CatppuccinThemes.Latte;

        Assert.Equal(0xFFEFF1F5u, theme.Colors.Background);
        Assert.Equal(0xFF4C4F69u, theme.Colors.Text);
        Assert.Equal(0xFF1E66F5u, theme.Colors.Accent);
    }

    [Fact]
    public void Macchiato_IsDarkTheme()
    {
        var theme = CatppuccinThemes.Macchiato;

        Assert.True(theme.IsDark);
        Assert.Equal("catppuccin-macchiato", theme.Id);
    }

    [Fact]
    public void Frappe_IsDarkTheme()
    {
        var theme = CatppuccinThemes.Frappe;

        Assert.True(theme.IsDark);
        Assert.Equal("catppuccin-frappe", theme.Id);
    }

    [Fact]
    public void All_ContainsFourThemes()
    {
        var themes = CatppuccinThemes.All;

        Assert.Equal(4, themes.Length);
    }

    [Fact]
    public void All_ContainsOneLightTheme()
    {
        var lightThemes = CatppuccinThemes.All.Where(t => !t.IsDark).ToList();

        Assert.Single(lightThemes);
        Assert.Equal("catppuccin-latte", lightThemes[0].Id);
    }

    [Fact]
    public void AllThemes_HaveSemanticColors()
    {
        foreach (var theme in CatppuccinThemes.All)
        {
            Assert.NotEqual(0u, theme.Colors.Success);
            Assert.NotEqual(0u, theme.Colors.Warning);
            Assert.NotEqual(0u, theme.Colors.Error);
            Assert.NotEqual(0u, theme.Colors.Info);
        }
    }

    [Fact]
    public void AllThemes_HaveCatppuccinPalette()
    {
        foreach (var theme in CatppuccinThemes.All)
        {
            Assert.NotEqual(0u, theme.Colors.Rosewater);
            Assert.NotEqual(0u, theme.Colors.Flamingo);
            Assert.NotEqual(0u, theme.Colors.Pink);
            Assert.NotEqual(0u, theme.Colors.Mauve);
            Assert.NotEqual(0u, theme.Colors.Blue);
            Assert.NotEqual(0u, theme.Colors.Lavender);
        }
    }
}

public class ThemeManagerTests
{
    private readonly ThemeManager _manager;

    public ThemeManagerTests()
    {
        _manager = new ThemeManager();
    }

    [Fact]
    public void Constructor_SetsDefaultTheme()
    {
        Assert.NotNull(_manager.CurrentTheme);
        Assert.Equal("catppuccin-mocha", _manager.CurrentTheme.Id);
    }

    [Fact]
    public void Constructor_RegistersBuiltInThemes()
    {
        var themes = _manager.Themes.ToList();

        Assert.Equal(4, themes.Count);
    }

    [Fact]
    public void Colors_ReturnsCurrentThemeColors()
    {
        Assert.Same(_manager.CurrentTheme.Colors, _manager.Colors);
    }

    [Fact]
    public void IsDarkTheme_ReflectsCurrentTheme()
    {
        Assert.True(_manager.IsDarkTheme);

        _manager.SetTheme("catppuccin-latte");

        Assert.False(_manager.IsDarkTheme);
    }

    [Fact]
    public void SetTheme_ByIdChangesTheme()
    {
        var result = _manager.SetTheme("catppuccin-latte");

        Assert.True(result);
        Assert.Equal("catppuccin-latte", _manager.CurrentTheme.Id);
    }

    [Fact]
    public void SetTheme_ReturnsFalse_ForUnknownId()
    {
        var result = _manager.SetTheme("unknown-theme");

        Assert.False(result);
        Assert.Equal("catppuccin-mocha", _manager.CurrentTheme.Id);
    }

    [Fact]
    public void SetTheme_ByObject_RegistersAndSets()
    {
        var customTheme = new Theme { Id = "custom", Name = "Custom" };

        _manager.SetTheme(customTheme);

        Assert.Same(customTheme, _manager.CurrentTheme);
        Assert.NotNull(_manager.GetTheme("custom"));
    }

    [Fact]
    public void RegisterTheme_AddsToCollection()
    {
        var customTheme = new Theme { Id = "custom", Name = "Custom" };

        _manager.RegisterTheme(customTheme);

        Assert.Contains(_manager.Themes, t => t.Id == "custom");
    }

    [Fact]
    public void UnregisterTheme_RemovesFromCollection()
    {
        var customTheme = new Theme { Id = "custom", Name = "Custom" };
        _manager.RegisterTheme(customTheme);

        var result = _manager.UnregisterTheme("custom");

        Assert.True(result);
        Assert.DoesNotContain(_manager.Themes, t => t.Id == "custom");
    }

    [Fact]
    public void UnregisterTheme_ReturnsFalse_ForCurrentTheme()
    {
        var result = _manager.UnregisterTheme("catppuccin-mocha");

        Assert.False(result);
    }

    [Fact]
    public void GetTheme_ReturnsTheme()
    {
        var theme = _manager.GetTheme("catppuccin-latte");

        Assert.NotNull(theme);
        Assert.Equal("Catppuccin Latte", theme.Name);
    }

    [Fact]
    public void GetTheme_ReturnsNull_ForUnknown()
    {
        var theme = _manager.GetTheme("unknown");

        Assert.Null(theme);
    }

    [Fact]
    public void ToggleDarkMode_SwitchesToLight()
    {
        _manager.SetTheme("catppuccin-mocha");

        _manager.ToggleDarkMode();

        Assert.False(_manager.IsDarkTheme);
    }

    [Fact]
    public void ToggleDarkMode_SwitchesToDark()
    {
        _manager.SetTheme("catppuccin-latte");

        _manager.ToggleDarkMode();

        Assert.True(_manager.IsDarkTheme);
    }

    [Fact]
    public void SetAccentColor_SetsCustomAccent()
    {
        _manager.SetAccentColor(0xFFFF0000);

        Assert.True(_manager.CurrentTheme.UseCustomAccent);
        Assert.Equal(0xFFFF0000u, _manager.CurrentTheme.CustomAccent);
    }

    [Fact]
    public void ResetAccentColor_DisablesCustomAccent()
    {
        _manager.SetAccentColor(0xFFFF0000);
        _manager.ResetAccentColor();

        Assert.False(_manager.CurrentTheme.UseCustomAccent);
    }

    [Fact]
    public void ThemeChanged_EventRaised()
    {
        Theme? oldTheme = null;
        Theme? newTheme = null;
        _manager.ThemeChanged += (_, e) =>
        {
            oldTheme = e.OldTheme;
            newTheme = e.NewTheme;
        };

        _manager.SetTheme("catppuccin-latte");

        Assert.NotNull(oldTheme);
        Assert.NotNull(newTheme);
        Assert.Equal("catppuccin-mocha", oldTheme.Id);
        Assert.Equal("catppuccin-latte", newTheme.Id);
    }

    [Fact]
    public void DarkThemes_ReturnsOnlyDark()
    {
        var darkThemes = _manager.DarkThemes.ToList();

        Assert.All(darkThemes, t => Assert.True(t.IsDark));
        Assert.Equal(3, darkThemes.Count);
    }

    [Fact]
    public void LightThemes_ReturnsOnlyLight()
    {
        var lightThemes = _manager.LightThemes.ToList();

        Assert.All(lightThemes, t => Assert.False(t.IsDark));
        Assert.Single(lightThemes);
    }

    [Fact]
    public void WithAlpha_SetsAlphaChannel()
    {
        var color = 0xFFFF0000u;

        var result = ThemeManager.WithAlpha(color, 0x80);

        Assert.Equal(0x80FF0000u, result);
    }

    [Fact]
    public void BlendColors_InterpolatesCorrectly()
    {
        var black = 0xFF000000u;
        var white = 0xFFFFFFFFu;

        var mid = ThemeManager.BlendColors(black, white, 0.5);

        var r = (byte)((mid >> 16) & 0xFF);
        var g = (byte)((mid >> 8) & 0xFF);
        var b = (byte)(mid & 0xFF);

        Assert.InRange(r, 125, 130);
        Assert.InRange(g, 125, 130);
        Assert.InRange(b, 125, 130);
    }

    [Fact]
    public void Lighten_MakesColorLighter()
    {
        var color = 0xFF000000u;

        var result = ThemeManager.Lighten(color, 0.5);

        Assert.NotEqual(color, result);
        var r = (byte)((result >> 16) & 0xFF);
        Assert.True(r > 0);
    }

    [Fact]
    public void Darken_MakesColorDarker()
    {
        var color = 0xFFFFFFFFu;

        var result = ThemeManager.Darken(color, 0.5);

        Assert.NotEqual(color, result);
        var r = (byte)((result >> 16) & 0xFF);
        Assert.True(r < 255);
    }

    [Fact]
    public void ParseHex_Parses6DigitHex()
    {
        var result = ThemeManager.ParseHex("#FF0000");

        Assert.Equal(0xFFFF0000u, result);
    }

    [Fact]
    public void ParseHex_Parses8DigitHex()
    {
        var result = ThemeManager.ParseHex("#80FF0000");

        Assert.Equal(0x80FF0000u, result);
    }

    [Fact]
    public void ToHex_Converts6Digit()
    {
        var result = ThemeManager.ToHex(0xFFFF0000);

        Assert.Equal("#FF0000", result);
    }

    [Fact]
    public void ToHex_Converts8Digit_WithAlpha()
    {
        var result = ThemeManager.ToHex(0x80FF0000, includeAlpha: true);

        Assert.Equal("#80FF0000", result);
    }
}
