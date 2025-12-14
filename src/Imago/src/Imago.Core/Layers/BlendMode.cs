namespace Imago.Core.Layers;

/// <summary>
/// Defines the blend modes available for layer compositing.
/// </summary>
public enum BlendMode
{
    // Normal modes
    Normal,
    Dissolve,

    // Darken modes
    Darken,
    Multiply,
    ColorBurn,
    LinearBurn,
    DarkerColor,

    // Lighten modes
    Lighten,
    Screen,
    ColorDodge,
    LinearDodge,
    LighterColor,

    // Contrast modes
    Overlay,
    SoftLight,
    HardLight,
    VividLight,
    LinearLight,
    PinLight,
    HardMix,

    // Inversion modes
    Difference,
    Exclusion,
    Subtract,
    Divide,

    // Component modes
    Hue,
    Saturation,
    Color,
    Luminosity
}
