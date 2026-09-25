using System.ComponentModel;
using Bezier.Core.Models;

namespace Bezier.Core.Services;

/// <summary>
/// Event args for theme changes.
/// </summary>
public class ThemeChangedEventArgs : EventArgs
{
    public Theme OldTheme { get; }
    public Theme NewTheme { get; }

    public ThemeChangedEventArgs(Theme oldTheme, Theme newTheme)
    {
        OldTheme = oldTheme;
        NewTheme = newTheme;
    }
}

/// <summary>
/// Manages application theming.
/// </summary>
public class ThemeManager : INotifyPropertyChanged
{
    private Theme _currentTheme;
    private readonly Dictionary<string, Theme> _themes = [];

    public event PropertyChangedEventHandler? PropertyChanged;
    public event EventHandler<ThemeChangedEventArgs>? ThemeChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    public ThemeManager()
    {
        // Register built-in themes
        foreach (var theme in CatppuccinThemes.All)
        {
            RegisterTheme(theme);
        }

        // Set default theme
        _currentTheme = CatppuccinThemes.Mocha;
    }

    /// <summary>
    /// Gets the current theme.
    /// </summary>
    public Theme CurrentTheme
    {
        get => _currentTheme;
        private set
        {
            if (_currentTheme != value)
            {
                var oldTheme = _currentTheme;
                _currentTheme = value;
                OnPropertyChanged(nameof(CurrentTheme));
                OnPropertyChanged(nameof(Colors));
                OnPropertyChanged(nameof(IsDarkTheme));
                ThemeChanged?.Invoke(this, new ThemeChangedEventArgs(oldTheme, value));
            }
        }
    }

    /// <summary>
    /// Gets the current theme colors (shortcut).
    /// </summary>
    public ThemeColors Colors => CurrentTheme.Colors;

    /// <summary>
    /// Gets whether the current theme is dark.
    /// </summary>
    public bool IsDarkTheme => CurrentTheme.IsDark;

    /// <summary>
    /// Gets all registered themes.
    /// </summary>
    public IEnumerable<Theme> Themes => _themes.Values;

    /// <summary>
    /// Gets all dark themes.
    /// </summary>
    public IEnumerable<Theme> DarkThemes => _themes.Values.Where(t => t.IsDark);

    /// <summary>
    /// Gets all light themes.
    /// </summary>
    public IEnumerable<Theme> LightThemes => _themes.Values.Where(t => !t.IsDark);

    /// <summary>
    /// Registers a theme.
    /// </summary>
    public void RegisterTheme(Theme theme)
    {
        _themes[theme.Id] = theme;
    }

    /// <summary>
    /// Unregisters a theme.
    /// </summary>
    public bool UnregisterTheme(string themeId)
    {
        if (CurrentTheme.Id == themeId)
            return false; // Can't remove current theme

        return _themes.Remove(themeId);
    }

    /// <summary>
    /// Gets a theme by ID.
    /// </summary>
    public Theme? GetTheme(string themeId)
    {
        return _themes.GetValueOrDefault(themeId);
    }

    /// <summary>
    /// Sets the current theme by ID.
    /// </summary>
    public bool SetTheme(string themeId)
    {
        if (_themes.TryGetValue(themeId, out var theme))
        {
            CurrentTheme = theme;
            return true;
        }
        return false;
    }

    /// <summary>
    /// Sets the current theme.
    /// </summary>
    public void SetTheme(Theme theme)
    {
        if (!_themes.ContainsKey(theme.Id))
        {
            RegisterTheme(theme);
        }
        CurrentTheme = theme;
    }

    /// <summary>
    /// Toggles between dark and light themes.
    /// </summary>
    public void ToggleDarkMode()
    {
        if (IsDarkTheme)
        {
            // Switch to first light theme
            var lightTheme = LightThemes.FirstOrDefault();
            if (lightTheme != null)
                CurrentTheme = lightTheme;
        }
        else
        {
            // Switch to first dark theme
            var darkTheme = DarkThemes.FirstOrDefault();
            if (darkTheme != null)
                CurrentTheme = darkTheme;
        }
    }

    /// <summary>
    /// Sets a custom accent color for the current theme.
    /// </summary>
    public void SetAccentColor(uint color)
    {
        CurrentTheme.CustomAccent = color;
        CurrentTheme.UseCustomAccent = true;
        OnPropertyChanged(nameof(CurrentTheme));
    }

    /// <summary>
    /// Resets to the theme's default accent color.
    /// </summary>
    public void ResetAccentColor()
    {
        CurrentTheme.UseCustomAccent = false;
        OnPropertyChanged(nameof(CurrentTheme));
    }

    /// <summary>
    /// Gets a color with modified alpha.
    /// </summary>
    public static uint WithAlpha(uint color, byte alpha)
    {
        return (uint)((alpha << 24) | (color & 0x00FFFFFF));
    }

    /// <summary>
    /// Blends two colors.
    /// </summary>
    public static uint BlendColors(uint color1, uint color2, double amount)
    {
        var a1 = (byte)((color1 >> 24) & 0xFF);
        var r1 = (byte)((color1 >> 16) & 0xFF);
        var g1 = (byte)((color1 >> 8) & 0xFF);
        var b1 = (byte)(color1 & 0xFF);

        var a2 = (byte)((color2 >> 24) & 0xFF);
        var r2 = (byte)((color2 >> 16) & 0xFF);
        var g2 = (byte)((color2 >> 8) & 0xFF);
        var b2 = (byte)(color2 & 0xFF);

        var a = (byte)(a1 + (a2 - a1) * amount);
        var r = (byte)(r1 + (r2 - r1) * amount);
        var g = (byte)(g1 + (g2 - g1) * amount);
        var b = (byte)(b1 + (b2 - b1) * amount);

        return (uint)((a << 24) | (r << 16) | (g << 8) | b);
    }

    /// <summary>
    /// Lightens a color.
    /// </summary>
    public static uint Lighten(uint color, double amount)
    {
        return BlendColors(color, 0xFFFFFFFF, amount);
    }

    /// <summary>
    /// Darkens a color.
    /// </summary>
    public static uint Darken(uint color, double amount)
    {
        return BlendColors(color, 0xFF000000, amount);
    }

    /// <summary>
    /// Converts a hex string to ARGB color.
    /// </summary>
    public static uint ParseHex(string hex)
    {
        hex = hex.TrimStart('#');
        return hex.Length switch
        {
            6 => 0xFF000000 | Convert.ToUInt32(hex, 16),
            8 => Convert.ToUInt32(hex, 16),
            _ => 0xFF000000
        };
    }

    /// <summary>
    /// Converts an ARGB color to hex string.
    /// </summary>
    public static string ToHex(uint color, bool includeAlpha = false)
    {
        if (includeAlpha)
            return $"#{color:X8}";
        return $"#{color & 0x00FFFFFF:X6}";
    }
}
