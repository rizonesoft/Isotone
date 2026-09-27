using System.ComponentModel;

namespace Bezier.Core.Models;

/// <summary>
/// Represents a color palette for theming.
/// </summary>
public class ThemeColors
{
    // Base colors
    public uint Background { get; init; }
    public uint Surface { get; init; }
    public uint SurfaceVariant { get; init; }
    public uint Overlay { get; init; }

    // Text colors
    public uint Text { get; init; }
    public uint TextSubtle { get; init; }
    public uint TextMuted { get; init; }

    // Accent colors
    public uint Accent { get; init; }
    public uint AccentHover { get; init; }
    public uint AccentPressed { get; init; }

    // Semantic colors
    public uint Success { get; init; }
    public uint Warning { get; init; }
    public uint Error { get; init; }
    public uint Info { get; init; }

    // UI element colors
    public uint Border { get; init; }
    public uint BorderSubtle { get; init; }
    public uint Selection { get; init; }
    public uint SelectionInactive { get; init; }
    public uint Hover { get; init; }

    // Canvas colors
    public uint CanvasBackground { get; init; }
    public uint CanvasGrid { get; init; }
    public uint CanvasGuide { get; init; }

    // Catppuccin palette colors (for variety)
    public uint Rosewater { get; init; }
    public uint Flamingo { get; init; }
    public uint Pink { get; init; }
    public uint Mauve { get; init; }
    public uint Red { get; init; }
    public uint Maroon { get; init; }
    public uint Peach { get; init; }
    public uint Yellow { get; init; }
    public uint Green { get; init; }
    public uint Teal { get; init; }
    public uint Sky { get; init; }
    public uint Sapphire { get; init; }
    public uint Blue { get; init; }
    public uint Lavender { get; init; }
}

/// <summary>
/// Represents a complete application theme.
/// </summary>
public class Theme : INotifyPropertyChanged
{
    private string _name = "Default";
    private bool _isDark = true;
    private uint _customAccent;
    private bool _useCustomAccent;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets the theme identifier.
    /// </summary>
    public string Id { get; init; } = "default";

    /// <summary>
    /// Gets or sets the theme display name.
    /// </summary>
    public string Name
    {
        get => _name;
        set { _name = value; OnPropertyChanged(nameof(Name)); }
    }

    /// <summary>
    /// Gets or sets whether this is a dark theme.
    /// </summary>
    public bool IsDark
    {
        get => _isDark;
        set { _isDark = value; OnPropertyChanged(nameof(IsDark)); }
    }

    /// <summary>
    /// Gets the color palette.
    /// </summary>
    public ThemeColors Colors { get; init; } = new();

    /// <summary>
    /// Gets or sets the custom accent color.
    /// </summary>
    public uint CustomAccent
    {
        get => _customAccent;
        set { _customAccent = value; OnPropertyChanged(nameof(CustomAccent)); OnPropertyChanged(nameof(EffectiveAccent)); }
    }

    /// <summary>
    /// Gets or sets whether to use custom accent color.
    /// </summary>
    public bool UseCustomAccent
    {
        get => _useCustomAccent;
        set { _useCustomAccent = value; OnPropertyChanged(nameof(UseCustomAccent)); OnPropertyChanged(nameof(EffectiveAccent)); }
    }

    /// <summary>
    /// Gets the effective accent color (custom or theme default).
    /// </summary>
    public uint EffectiveAccent => UseCustomAccent ? CustomAccent : Colors.Accent;

    /// <summary>
    /// Gets a contrasting text color for the accent.
    /// </summary>
    public uint AccentText
    {
        get
        {
            var accent = EffectiveAccent;
            var r = (accent >> 16) & 0xFF;
            var g = (accent >> 8) & 0xFF;
            var b = accent & 0xFF;
            var luminance = 0.299 * r / 255 + 0.587 * g / 255 + 0.114 * b / 255;
            return luminance > 0.5 ? 0xFF000000 : 0xFFFFFFFF;
        }
    }
}

/// <summary>
/// Predefined Catppuccin themes.
/// </summary>
public static class CatppuccinThemes
{
    /// <summary>
    /// Catppuccin Mocha (dark theme).
    /// </summary>
    public static Theme Mocha => new()
    {
        Id = "catppuccin-mocha",
        Name = "Catppuccin Mocha",
        IsDark = true,
        Colors = new ThemeColors
        {
            // Base
            Background = 0xFF1E1E2E,  // Base
            Surface = 0xFF313244,      // Surface0
            SurfaceVariant = 0xFF45475A, // Surface1
            Overlay = 0xFF585B70,      // Surface2

            // Text
            Text = 0xFFCDD6F4,         // Text
            TextSubtle = 0xFFBAC2DE,   // Subtext1
            TextMuted = 0xFFA6ADC8,    // Subtext0

            // Accent
            Accent = 0xFF89B4FA,       // Blue
            AccentHover = 0xFF74C7EC,  // Sapphire
            AccentPressed = 0xFF89DCEB, // Sky

            // Semantic
            Success = 0xFFA6E3A1,      // Green
            Warning = 0xFFF9E2AF,      // Yellow
            Error = 0xFFF38BA8,        // Red
            Info = 0xFF89B4FA,         // Blue

            // UI
            Border = 0xFF585B70,       // Surface2
            BorderSubtle = 0xFF45475A, // Surface1
            Selection = 0x4089B4FA,    // Blue with alpha
            SelectionInactive = 0x20CDD6F4,
            Hover = 0x20CDD6F4,

            // Canvas
            CanvasBackground = 0xFF11111B, // Crust
            CanvasGrid = 0xFF313244,
            CanvasGuide = 0xFF89B4FA,

            // Catppuccin palette
            Rosewater = 0xFFF5E0DC,
            Flamingo = 0xFFF2CDCD,
            Pink = 0xFFF5C2E7,
            Mauve = 0xFFCBA6F7,
            Red = 0xFFF38BA8,
            Maroon = 0xFFEBA0AC,
            Peach = 0xFFFAB387,
            Yellow = 0xFFF9E2AF,
            Green = 0xFFA6E3A1,
            Teal = 0xFF94E2D5,
            Sky = 0xFF89DCEB,
            Sapphire = 0xFF74C7EC,
            Blue = 0xFF89B4FA,
            Lavender = 0xFFB4BEFE,
        }
    };

    /// <summary>
    /// Catppuccin Latte (light theme).
    /// </summary>
    public static Theme Latte => new()
    {
        Id = "catppuccin-latte",
        Name = "Catppuccin Latte",
        IsDark = false,
        Colors = new ThemeColors
        {
            // Base
            Background = 0xFFEFF1F5,   // Base
            Surface = 0xFFE6E9EF,      // Surface0
            SurfaceVariant = 0xFFDCE0E8, // Surface1
            Overlay = 0xFFCCD0DA,      // Surface2

            // Text
            Text = 0xFF4C4F69,         // Text
            TextSubtle = 0xFF5C5F77,   // Subtext1
            TextMuted = 0xFF6C6F85,    // Subtext0

            // Accent
            Accent = 0xFF1E66F5,       // Blue
            AccentHover = 0xFF209FB5,  // Sapphire
            AccentPressed = 0xFF04A5E5, // Sky

            // Semantic
            Success = 0xFF40A02B,      // Green
            Warning = 0xFFDF8E1D,      // Yellow
            Error = 0xFFD20F39,        // Red
            Info = 0xFF1E66F5,         // Blue

            // UI
            Border = 0xFFCCD0DA,       // Surface2
            BorderSubtle = 0xFFDCE0E8, // Surface1
            Selection = 0x401E66F5,    // Blue with alpha
            SelectionInactive = 0x204C4F69,
            Hover = 0x204C4F69,

            // Canvas
            CanvasBackground = 0xFFFFFFFF,
            CanvasGrid = 0xFFDCE0E8,
            CanvasGuide = 0xFF1E66F5,

            // Catppuccin palette
            Rosewater = 0xFFDC8A78,
            Flamingo = 0xFFDD7878,
            Pink = 0xFFEA76CB,
            Mauve = 0xFF8839EF,
            Red = 0xFFD20F39,
            Maroon = 0xFFE64553,
            Peach = 0xFFFE640B,
            Yellow = 0xFFDF8E1D,
            Green = 0xFF40A02B,
            Teal = 0xFF179299,
            Sky = 0xFF04A5E5,
            Sapphire = 0xFF209FB5,
            Blue = 0xFF1E66F5,
            Lavender = 0xFF7287FD,
        }
    };

    /// <summary>
    /// Catppuccin Macchiato (medium dark theme).
    /// </summary>
    public static Theme Macchiato => new()
    {
        Id = "catppuccin-macchiato",
        Name = "Catppuccin Macchiato",
        IsDark = true,
        Colors = new ThemeColors
        {
            // Base
            Background = 0xFF24273A,
            Surface = 0xFF363A4F,
            SurfaceVariant = 0xFF494D64,
            Overlay = 0xFF5B6078,

            // Text
            Text = 0xFFCAD3F5,
            TextSubtle = 0xFFB8C0E0,
            TextMuted = 0xFFA5ADCB,

            // Accent
            Accent = 0xFF8AADF4,
            AccentHover = 0xFF7DC4E4,
            AccentPressed = 0xFF91D7E3,

            // Semantic
            Success = 0xFFA6DA95,
            Warning = 0xFFEED49F,
            Error = 0xFFED8796,
            Info = 0xFF8AADF4,

            // UI
            Border = 0xFF5B6078,
            BorderSubtle = 0xFF494D64,
            Selection = 0x408AADF4,
            SelectionInactive = 0x20CAD3F5,
            Hover = 0x20CAD3F5,

            // Canvas
            CanvasBackground = 0xFF181926,
            CanvasGrid = 0xFF363A4F,
            CanvasGuide = 0xFF8AADF4,

            // Catppuccin palette
            Rosewater = 0xFFF4DBD6,
            Flamingo = 0xFFF0C6C6,
            Pink = 0xFFF5BDE6,
            Mauve = 0xFFC6A0F6,
            Red = 0xFFED8796,
            Maroon = 0xFFEE99A0,
            Peach = 0xFFF5A97F,
            Yellow = 0xFFEED49F,
            Green = 0xFFA6DA95,
            Teal = 0xFF8BD5CA,
            Sky = 0xFF91D7E3,
            Sapphire = 0xFF7DC4E4,
            Blue = 0xFF8AADF4,
            Lavender = 0xFFB7BDF8,
        }
    };

    /// <summary>
    /// Catppuccin Frappé (medium theme).
    /// </summary>
    public static Theme Frappe => new()
    {
        Id = "catppuccin-frappe",
        Name = "Catppuccin Frappé",
        IsDark = true,
        Colors = new ThemeColors
        {
            // Base
            Background = 0xFF303446,
            Surface = 0xFF414559,
            SurfaceVariant = 0xFF51576D,
            Overlay = 0xFF626880,

            // Text
            Text = 0xFFC6D0F5,
            TextSubtle = 0xFFB5BFE2,
            TextMuted = 0xFFA5ADCE,

            // Accent
            Accent = 0xFF8CAAEE,
            AccentHover = 0xFF85C1DC,
            AccentPressed = 0xFF99D1DB,

            // Semantic
            Success = 0xFFA6D189,
            Warning = 0xFFE5C890,
            Error = 0xFFE78284,
            Info = 0xFF8CAAEE,

            // UI
            Border = 0xFF626880,
            BorderSubtle = 0xFF51576D,
            Selection = 0x408CAAEE,
            SelectionInactive = 0x20C6D0F5,
            Hover = 0x20C6D0F5,

            // Canvas
            CanvasBackground = 0xFF232634,
            CanvasGrid = 0xFF414559,
            CanvasGuide = 0xFF8CAAEE,

            // Catppuccin palette
            Rosewater = 0xFFF2D5CF,
            Flamingo = 0xFFEEBEBE,
            Pink = 0xFFF4B8E4,
            Mauve = 0xFFCA9EE6,
            Red = 0xFFE78284,
            Maroon = 0xFFEA999C,
            Peach = 0xFFEF9F76,
            Yellow = 0xFFE5C890,
            Green = 0xFFA6D189,
            Teal = 0xFF81C8BE,
            Sky = 0xFF99D1DB,
            Sapphire = 0xFF85C1DC,
            Blue = 0xFF8CAAEE,
            Lavender = 0xFFBABBF1,
        }
    };

    /// <summary>
    /// Gets all available Catppuccin themes.
    /// </summary>
    public static Theme[] All => [Mocha, Latte, Macchiato, Frappe];
}
