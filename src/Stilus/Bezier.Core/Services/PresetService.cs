namespace Bezier.Core.Services;

/// <summary>
/// Represents a preset value with name and value.
/// </summary>
public record Preset<T>(string Name, T Value, string? Category = null);

/// <summary>
/// Service for managing common presets for UI controls.
/// </summary>
public static class PresetService
{
    /// <summary>
    /// Common stroke width presets.
    /// </summary>
    public static readonly Preset<double>[] StrokeWidths =
    [
        new("Hairline", 0.5),
        new("Thin", 1),
        new("Light", 1.5),
        new("Normal", 2),
        new("Medium", 3),
        new("Thick", 4),
        new("Heavy", 6),
        new("Extra Heavy", 8),
        new("Ultra", 12),
    ];

    /// <summary>
    /// Common opacity presets.
    /// </summary>
    public static readonly Preset<double>[] Opacities =
    [
        new("0%", 0),
        new("10%", 0.1),
        new("25%", 0.25),
        new("50%", 0.5),
        new("75%", 0.75),
        new("90%", 0.9),
        new("100%", 1),
    ];

    /// <summary>
    /// Common corner radius presets.
    /// </summary>
    public static readonly Preset<double>[] CornerRadii =
    [
        new("None", 0),
        new("Small", 4),
        new("Medium", 8),
        new("Large", 12),
        new("Extra Large", 16),
        new("Rounded", 24),
        new("Pill", 9999),
    ];

    /// <summary>
    /// Common dash pattern presets.
    /// </summary>
    public static readonly Preset<double[]>[] DashPatterns =
    [
        new("Solid", []),
        new("Dotted", [1, 2]),
        new("Dashed", [4, 4]),
        new("Long Dash", [8, 4]),
        new("Dash Dot", [8, 4, 2, 4]),
        new("Dash Dot Dot", [8, 4, 2, 4, 2, 4]),
    ];

    /// <summary>
    /// Common color presets (ARGB).
    /// </summary>
    public static readonly Preset<uint>[] Colors =
    [
        // Grayscale
        new("Black", 0xFF000000, "Grayscale"),
        new("Dark Gray", 0xFF333333, "Grayscale"),
        new("Gray", 0xFF666666, "Grayscale"),
        new("Light Gray", 0xFF999999, "Grayscale"),
        new("Silver", 0xFFCCCCCC, "Grayscale"),
        new("White", 0xFFFFFFFF, "Grayscale"),
        
        // Primary
        new("Red", 0xFFFF0000, "Primary"),
        new("Green", 0xFF00FF00, "Primary"),
        new("Blue", 0xFF0000FF, "Primary"),
        
        // Secondary
        new("Cyan", 0xFF00FFFF, "Secondary"),
        new("Magenta", 0xFFFF00FF, "Secondary"),
        new("Yellow", 0xFFFFFF00, "Secondary"),
        
        // Web Colors
        new("Coral", 0xFFFF7F50, "Web"),
        new("Tomato", 0xFFFF6347, "Web"),
        new("Orange", 0xFFFFA500, "Web"),
        new("Gold", 0xFFFFD700, "Web"),
        new("Lime", 0xFF32CD32, "Web"),
        new("Teal", 0xFF008080, "Web"),
        new("Navy", 0xFF000080, "Web"),
        new("Purple", 0xFF800080, "Web"),
        new("Indigo", 0xFF4B0082, "Web"),
        new("Pink", 0xFFFFC0CB, "Web"),
        
        // Catppuccin Mocha
        new("Rosewater", 0xFFF5E0DC, "Catppuccin"),
        new("Flamingo", 0xFFF2CDCD, "Catppuccin"),
        new("Pink", 0xFFF5C2E7, "Catppuccin"),
        new("Mauve", 0xFFCBA6F7, "Catppuccin"),
        new("Red", 0xFFF38BA8, "Catppuccin"),
        new("Maroon", 0xFFEBA0AC, "Catppuccin"),
        new("Peach", 0xFFFAB387, "Catppuccin"),
        new("Yellow", 0xFFF9E2AF, "Catppuccin"),
        new("Green", 0xFFA6E3A1, "Catppuccin"),
        new("Teal", 0xFF94E2D5, "Catppuccin"),
        new("Sky", 0xFF89DCEB, "Catppuccin"),
        new("Sapphire", 0xFF74C7EC, "Catppuccin"),
        new("Blue", 0xFF89B4FA, "Catppuccin"),
        new("Lavender", 0xFFB4BEFE, "Catppuccin"),
    ];

    /// <summary>
    /// Common font size presets.
    /// </summary>
    public static readonly Preset<double>[] FontSizes =
    [
        new("Tiny", 8),
        new("Small", 10),
        new("Normal", 12),
        new("Medium", 14),
        new("Large", 18),
        new("Extra Large", 24),
        new("Huge", 32),
        new("Giant", 48),
        new("Massive", 72),
    ];

    /// <summary>
    /// Common rotation angle presets.
    /// </summary>
    public static readonly Preset<double>[] RotationAngles =
    [
        new("0°", 0),
        new("45°", 45),
        new("90°", 90),
        new("135°", 135),
        new("180°", 180),
        new("225°", 225),
        new("270°", 270),
        new("315°", 315),
    ];

    /// <summary>
    /// Gets presets filtered by category.
    /// </summary>
    public static IEnumerable<Preset<T>> GetByCategory<T>(Preset<T>[] presets, string category)
    {
        return presets.Where(p => p.Category == category);
    }

    /// <summary>
    /// Gets all unique categories from presets.
    /// </summary>
    public static IEnumerable<string> GetCategories<T>(Preset<T>[] presets)
    {
        return presets
            .Where(p => p.Category != null)
            .Select(p => p.Category!)
            .Distinct();
    }

    /// <summary>
    /// Finds a preset by name.
    /// </summary>
    public static Preset<T>? FindByName<T>(Preset<T>[] presets, string name)
    {
        return presets.FirstOrDefault(p =>
            p.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Finds the closest preset to a value.
    /// </summary>
    public static Preset<double>? FindClosest(Preset<double>[] presets, double value, double tolerance = 0.1)
    {
        return presets
            .OrderBy(p => Math.Abs(p.Value - value))
            .FirstOrDefault(p => Math.Abs(p.Value - value) <= tolerance);
    }
}
