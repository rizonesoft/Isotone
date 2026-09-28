namespace Gesso.Core.Layers;

/// <summary>
/// Defines the blend modes available for layer compositing.
/// Photoshop-compatible with extended modes.
/// </summary>
public enum BlendMode
{
    // Normal modes (0-9)
    Normal = 0,
    Dissolve = 1,
    Behind = 2,
    Clear = 3,

    // Darken modes (10-19)
    Darken = 10,
    Multiply = 11,
    ColorBurn = 12,
    LinearBurn = 13,
    DarkerColor = 14,

    // Lighten modes (20-29)
    Lighten = 20,
    Screen = 21,
    ColorDodge = 22,
    LinearDodge = 23,
    LighterColor = 24,

    // Contrast modes (30-49)
    Overlay = 30,
    SoftLight = 31,
    HardLight = 32,
    VividLight = 33,
    LinearLight = 34,
    PinLight = 35,
    HardMix = 36,

    // Inversion modes (50-59)
    Difference = 50,
    Exclusion = 51,
    Subtract = 52,
    Divide = 53,
    NegativeMultiply = 54,

    // Component modes (60-69)
    Hue = 60,
    Saturation = 61,
    Color = 62,
    Luminosity = 63,

    // Special modes (70-89)
    PassThrough = 70,
    DarkenOnly = 71,
    LightenOnly = 72,
    Average = 73,
    Reflect = 74,
    Glow = 75,
    Phoenix = 76,
    Negation = 77,

    // Photographic modes (90-99)
    Grain = 90,
    GrainMerge = 91,
    GrainExtract = 92,

    // Additional contrast modes (100-109)
    SoftDodge = 100,
    SoftBurn = 101,
    FlatLight = 102,
    StampLight = 103,
    Freeze = 104,
    Heat = 105,

    // Geometric modes (110-119)
    GeometricMean = 110,
    HarmonicMean = 111,
    Interpolation = 112,

    // Legacy/compatibility modes (120+)
    Atop = 120,
    Xor = 121,
    Plus = 122,
    Minus = 123
}

/// <summary>
/// Extension methods for BlendMode.
/// </summary>
public static class BlendModeExtensions
{
    /// <summary>
    /// Gets the display name for a blend mode.
    /// </summary>
    public static string GetDisplayName(this BlendMode mode) => mode switch
    {
        BlendMode.LinearDodge => "Linear Dodge (Add)",
        BlendMode.LinearBurn => "Linear Burn",
        BlendMode.PassThrough => "Pass Through",
        BlendMode.NegativeMultiply => "Negative Multiply",
        BlendMode.GrainMerge => "Grain Merge",
        BlendMode.GrainExtract => "Grain Extract",
        _ => SplitCamelCase(mode.ToString())
    };

    /// <summary>
    /// Gets the category for a blend mode.
    /// </summary>
    public static BlendModeCategory GetCategory(this BlendMode mode) => (int)mode switch
    {
        < 10 => BlendModeCategory.Normal,
        < 20 => BlendModeCategory.Darken,
        < 30 => BlendModeCategory.Lighten,
        < 50 => BlendModeCategory.Contrast,
        < 60 => BlendModeCategory.Inversion,
        < 70 => BlendModeCategory.Component,
        _ => BlendModeCategory.Special
    };

    private static string SplitCamelCase(string input)
    {
        if (string.IsNullOrEmpty(input)) return input;

        Span<char> result = stackalloc char[input.Length * 2];
        int resultIndex = 0;

        for (int i = 0; i < input.Length; i++)
        {
            if (i > 0 && char.IsUpper(input[i]))
            {
                result[resultIndex++] = ' ';
            }
            result[resultIndex++] = input[i];
        }

        return new string(result[..resultIndex]);
    }
}

/// <summary>
/// Categories of blend modes for UI grouping.
/// </summary>
public enum BlendModeCategory
{
    Normal,
    Darken,
    Lighten,
    Contrast,
    Inversion,
    Component,
    Special
}
