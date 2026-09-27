namespace Pinxit.Core.Colors;

using System.Runtime.CompilerServices;

/// <summary>
/// HSV (Hue, Saturation, Value) color model.
/// </summary>
public readonly record struct HsvColor(float H, float S, float V)
{
    /// <summary>
    /// Hue in degrees (0-360).
    /// </summary>
    public float H { get; init; } = H;

    /// <summary>
    /// Saturation (0-1).
    /// </summary>
    public float S { get; init; } = S;

    /// <summary>
    /// Value/Brightness (0-1).
    /// </summary>
    public float V { get; init; } = V;

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static HsvColor FromRgb(float r, float g, float b)
    {
        var (h, s, v) = ColorConverter.RgbToHsv(r, g, b);
        return new HsvColor(h, s, v);
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public readonly (float R, float G, float B) ToRgb()
    {
        return ColorConverter.HsvToRgb(H, S, V);
    }

    public readonly Rgba32 ToRgba32(byte alpha = 255)
    {
        var (r, g, b) = ToRgb();
        return Rgba32.FromNormalized(r, g, b, alpha / 255f);
    }

    public override string ToString() => $"HSV({H:F0}°, {S:P0}, {V:P0})";
}

/// <summary>
/// HSL (Hue, Saturation, Lightness) color model.
/// </summary>
public readonly record struct HslColor(float H, float S, float L)
{
    /// <summary>
    /// Hue in degrees (0-360).
    /// </summary>
    public float H { get; init; } = H;

    /// <summary>
    /// Saturation (0-1).
    /// </summary>
    public float S { get; init; } = S;

    /// <summary>
    /// Lightness (0-1).
    /// </summary>
    public float L { get; init; } = L;

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static HslColor FromRgb(float r, float g, float b)
    {
        var (h, s, l) = ColorConverter.RgbToHsl(r, g, b);
        return new HslColor(h, s, l);
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public readonly (float R, float G, float B) ToRgb()
    {
        return ColorConverter.HslToRgb(H, S, L);
    }

    public readonly Rgba32 ToRgba32(byte alpha = 255)
    {
        var (r, g, b) = ToRgb();
        return Rgba32.FromNormalized(r, g, b, alpha / 255f);
    }

    public override string ToString() => $"HSL({H:F0}°, {S:P0}, {L:P0})";
}

/// <summary>
/// CIE L*a*b* color model.
/// </summary>
public readonly record struct LabColor(float L, float A, float B)
{
    /// <summary>
    /// Lightness (0-100).
    /// </summary>
    public float L { get; init; } = L;

    /// <summary>
    /// Green-Red axis (-128 to 127).
    /// </summary>
    public float A { get; init; } = A;

    /// <summary>
    /// Blue-Yellow axis (-128 to 127).
    /// </summary>
    public float B { get; init; } = B;

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static LabColor FromSrgb(float r, float g, float b)
    {
        var (l, a, lab_b) = ColorConverter.SrgbToLab(r, g, b);
        return new LabColor(l, a, lab_b);
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public readonly (float R, float G, float B) ToSrgb()
    {
        return ColorConverter.LabToSrgb(L, A, B);
    }

    public readonly Rgba32 ToRgba32(byte alpha = 255)
    {
        var (r, g, b) = ToSrgb();
        return Rgba32.FromNormalized(r, g, b, alpha / 255f);
    }

    /// <summary>
    /// Calculates the Delta E (CIE76) color difference.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public readonly float DeltaE(LabColor other)
    {
        float dL = L - other.L;
        float dA = A - other.A;
        float dB = B - other.B;
        return MathF.Sqrt(dL * dL + dA * dA + dB * dB);
    }

    public override string ToString() => $"LAB({L:F1}, {A:F1}, {B:F1})";
}

/// <summary>
/// CMYK color model.
/// </summary>
public readonly record struct CmykColor(float C, float M, float Y, float K)
{
    /// <summary>
    /// Cyan (0-1).
    /// </summary>
    public float C { get; init; } = C;

    /// <summary>
    /// Magenta (0-1).
    /// </summary>
    public float M { get; init; } = M;

    /// <summary>
    /// Yellow (0-1).
    /// </summary>
    public float Y { get; init; } = Y;

    /// <summary>
    /// Key/Black (0-1).
    /// </summary>
    public float K { get; init; } = K;

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static CmykColor FromRgb(float r, float g, float b)
    {
        var (c, m, y, k) = ColorConverter.RgbToCmyk(r, g, b);
        return new CmykColor(c, m, y, k);
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public readonly (float R, float G, float B) ToRgb()
    {
        return ColorConverter.CmykToRgb(C, M, Y, K);
    }

    public readonly Rgba32 ToRgba32()
    {
        var (r, g, b) = ToRgb();
        return Rgba32.FromNormalized(r, g, b);
    }

    public override string ToString() => $"CMYK({C:P0}, {M:P0}, {Y:P0}, {K:P0})";
}
