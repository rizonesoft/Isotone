namespace Imago.Core.Colors;

using System.Runtime.CompilerServices;

/// <summary>
/// High-performance color space conversion service.
/// All hot-path methods are zero-allocation.
/// </summary>
public static class ColorConverter
{
    // sRGB linearization constants
    private const float SrgbThreshold = 0.04045f;
    private const float SrgbLinearScale = 1f / 12.92f;
    private const float SrgbGammaScale = 1f / 1.055f;
    private const float SrgbGammaOffset = 0.055f;
    private const float SrgbGamma = 2.4f;

    #region RGB ↔ Linear RGB (sRGB gamma)

    /// <summary>
    /// Converts sRGB to linear RGB (removes gamma).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static float SrgbToLinear(float srgb)
    {
        return srgb <= SrgbThreshold
            ? srgb * SrgbLinearScale
            : MathF.Pow((srgb + SrgbGammaOffset) * SrgbGammaScale, SrgbGamma);
    }

    /// <summary>
    /// Converts linear RGB to sRGB (applies gamma).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static float LinearToSrgb(float linear)
    {
        return linear <= 0.0031308f
            ? linear * 12.92f
            : 1.055f * MathF.Pow(linear, 1f / 2.4f) - 0.055f;
    }

    /// <summary>
    /// Converts sRGB color to linear RGB.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float R, float G, float B) SrgbToLinear(float r, float g, float b)
    {
        return (SrgbToLinear(r), SrgbToLinear(g), SrgbToLinear(b));
    }

    /// <summary>
    /// Converts linear RGB to sRGB.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float R, float G, float B) LinearToSrgb(float r, float g, float b)
    {
        return (LinearToSrgb(r), LinearToSrgb(g), LinearToSrgb(b));
    }

    #endregion

    #region RGB ↔ HSV

    /// <summary>
    /// Converts RGB to HSV. H is in degrees (0-360), S and V are 0-1.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float H, float S, float V) RgbToHsv(float r, float g, float b)
    {
        float max = MathF.Max(r, MathF.Max(g, b));
        float min = MathF.Min(r, MathF.Min(g, b));
        float delta = max - min;

        float h = 0f;
        if (delta > 0.00001f)
        {
            if (max == r)
                h = 60f * (((g - b) / delta) % 6f);
            else if (max == g)
                h = 60f * (((b - r) / delta) + 2f);
            else
                h = 60f * (((r - g) / delta) + 4f);
        }

        if (h < 0) h += 360f;

        float s = max > 0.00001f ? delta / max : 0f;
        float v = max;

        return (h, s, v);
    }

    /// <summary>
    /// Converts HSV to RGB. H is in degrees (0-360), S and V are 0-1.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float R, float G, float B) HsvToRgb(float h, float s, float v)
    {
        if (s < 0.00001f)
            return (v, v, v);

        h %= 360f;
        if (h < 0) h += 360f;

        float c = v * s;
        float x = c * (1f - MathF.Abs((h / 60f) % 2f - 1f));
        float m = v - c;

        float r, g, b;
        if (h < 60f) { r = c; g = x; b = 0; }
        else if (h < 120f) { r = x; g = c; b = 0; }
        else if (h < 180f) { r = 0; g = c; b = x; }
        else if (h < 240f) { r = 0; g = x; b = c; }
        else if (h < 300f) { r = x; g = 0; b = c; }
        else { r = c; g = 0; b = x; }

        return (r + m, g + m, b + m);
    }

    #endregion

    #region RGB ↔ HSL

    /// <summary>
    /// Converts RGB to HSL. H is in degrees (0-360), S and L are 0-1.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float H, float S, float L) RgbToHsl(float r, float g, float b)
    {
        float max = MathF.Max(r, MathF.Max(g, b));
        float min = MathF.Min(r, MathF.Min(g, b));
        float delta = max - min;
        float l = (max + min) * 0.5f;

        float h = 0f, s = 0f;

        if (delta > 0.00001f)
        {
            s = l > 0.5f ? delta / (2f - max - min) : delta / (max + min);

            if (max == r)
                h = 60f * (((g - b) / delta) % 6f);
            else if (max == g)
                h = 60f * (((b - r) / delta) + 2f);
            else
                h = 60f * (((r - g) / delta) + 4f);
        }

        if (h < 0) h += 360f;

        return (h, s, l);
    }

    /// <summary>
    /// Converts HSL to RGB. H is in degrees (0-360), S and L are 0-1.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float R, float G, float B) HslToRgb(float h, float s, float l)
    {
        if (s < 0.00001f)
            return (l, l, l);

        float c = (1f - MathF.Abs(2f * l - 1f)) * s;
        float x = c * (1f - MathF.Abs((h / 60f) % 2f - 1f));
        float m = l - c * 0.5f;

        h %= 360f;
        if (h < 0) h += 360f;

        float r, g, b;
        if (h < 60f) { r = c; g = x; b = 0; }
        else if (h < 120f) { r = x; g = c; b = 0; }
        else if (h < 180f) { r = 0; g = c; b = x; }
        else if (h < 240f) { r = 0; g = x; b = c; }
        else if (h < 300f) { r = x; g = 0; b = c; }
        else { r = c; g = 0; b = x; }

        return (r + m, g + m, b + m);
    }

    #endregion

    #region RGB ↔ LAB (CIE L*a*b*)

    /// <summary>
    /// Converts linear RGB to XYZ (D65 illuminant).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float X, float Y, float Z) LinearRgbToXyz(float r, float g, float b)
    {
        // sRGB to XYZ matrix (D65)
        float x = r * 0.4124564f + g * 0.3575761f + b * 0.1804375f;
        float y = r * 0.2126729f + g * 0.7151522f + b * 0.0721750f;
        float z = r * 0.0193339f + g * 0.1191920f + b * 0.9503041f;
        return (x, y, z);
    }

    /// <summary>
    /// Converts XYZ to linear RGB (D65 illuminant).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float R, float G, float B) XyzToLinearRgb(float x, float y, float z)
    {
        // XYZ to sRGB matrix (D65)
        float r = x * 3.2404542f + y * -1.5371385f + z * -0.4985314f;
        float g = x * -0.9692660f + y * 1.8760108f + z * 0.0415560f;
        float b = x * 0.0556434f + y * -0.2040259f + z * 1.0572252f;
        return (r, g, b);
    }

    // D65 reference white
    private const float RefX = 0.95047f;
    private const float RefY = 1.00000f;
    private const float RefZ = 1.08883f;
    private const float LabEpsilon = 0.008856f;
    private const float LabKappa = 903.3f;

    /// <summary>
    /// Converts XYZ to LAB.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float L, float A, float B) XyzToLab(float x, float y, float z)
    {
        x /= RefX;
        y /= RefY;
        z /= RefZ;

        x = x > LabEpsilon ? MathF.Cbrt(x) : (LabKappa * x + 16f) / 116f;
        y = y > LabEpsilon ? MathF.Cbrt(y) : (LabKappa * y + 16f) / 116f;
        z = z > LabEpsilon ? MathF.Cbrt(z) : (LabKappa * z + 16f) / 116f;

        float l = 116f * y - 16f;
        float a = 500f * (x - y);
        float b = 200f * (y - z);

        return (l, a, b);
    }

    /// <summary>
    /// Converts LAB to XYZ.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float X, float Y, float Z) LabToXyz(float l, float a, float b)
    {
        float y = (l + 16f) / 116f;
        float x = a / 500f + y;
        float z = y - b / 200f;

        float x3 = x * x * x;
        float y3 = y * y * y;
        float z3 = z * z * z;

        x = x3 > LabEpsilon ? x3 : (116f * x - 16f) / LabKappa;
        y = l > LabKappa * LabEpsilon ? y3 : l / LabKappa;
        z = z3 > LabEpsilon ? z3 : (116f * z - 16f) / LabKappa;

        return (x * RefX, y * RefY, z * RefZ);
    }

    /// <summary>
    /// Converts sRGB to LAB.
    /// </summary>
    public static (float L, float A, float B) SrgbToLab(float r, float g, float b)
    {
        var linear = SrgbToLinear(r, g, b);
        var xyz = LinearRgbToXyz(linear.R, linear.G, linear.B);
        return XyzToLab(xyz.X, xyz.Y, xyz.Z);
    }

    /// <summary>
    /// Converts LAB to sRGB.
    /// </summary>
    public static (float R, float G, float B) LabToSrgb(float l, float a, float b)
    {
        var xyz = LabToXyz(l, a, b);
        var linear = XyzToLinearRgb(xyz.X, xyz.Y, xyz.Z);
        return LinearToSrgb(
            Math.Clamp(linear.R, 0f, 1f),
            Math.Clamp(linear.G, 0f, 1f),
            Math.Clamp(linear.B, 0f, 1f));
    }

    #endregion

    #region RGB ↔ CMYK

    /// <summary>
    /// Converts RGB to CMYK. All values are 0-1.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float C, float M, float Y, float K) RgbToCmyk(float r, float g, float b)
    {
        float k = 1f - MathF.Max(r, MathF.Max(g, b));

        if (k >= 0.9999f)
            return (0f, 0f, 0f, 1f);

        float invK = 1f / (1f - k);
        float c = (1f - r - k) * invK;
        float m = (1f - g - k) * invK;
        float y = (1f - b - k) * invK;

        return (c, m, y, k);
    }

    /// <summary>
    /// Converts CMYK to RGB. All values are 0-1.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float R, float G, float B) CmykToRgb(float c, float m, float y, float k)
    {
        float invK = 1f - k;
        float r = (1f - c) * invK;
        float g = (1f - m) * invK;
        float b = (1f - y) * invK;
        return (r, g, b);
    }

    #endregion

    #region Gamut Checking

    /// <summary>
    /// Checks if a color is within the sRGB gamut.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static bool IsInSrgbGamut(float r, float g, float b)
    {
        return r >= 0f && r <= 1f && g >= 0f && g <= 1f && b >= 0f && b <= 1f;
    }

    /// <summary>
    /// Clamps a color to the sRGB gamut.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static (float R, float G, float B) ClampToSrgbGamut(float r, float g, float b)
    {
        return (Math.Clamp(r, 0f, 1f), Math.Clamp(g, 0f, 1f), Math.Clamp(b, 0f, 1f));
    }

    #endregion
}
