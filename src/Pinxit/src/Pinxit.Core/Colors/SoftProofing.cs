namespace Pinxit.Core.Colors;

using System.Runtime.CompilerServices;

/// <summary>
/// Provides soft-proofing functionality for simulating how colors will appear
/// on different output devices (printers, displays).
/// </summary>
public sealed class SoftProofing
{
    private readonly ColorProfile _sourceProfile;
    private readonly ColorProfile _proofProfile;
    private readonly RenderingIntent _renderingIntent;
    private readonly bool _simulatePaperWhite;
    private readonly bool _simulateBlackInk;

    /// <summary>
    /// Gets whether gamut warning is enabled.
    /// </summary>
    public bool ShowGamutWarning { get; set; }

    /// <summary>
    /// Color used to indicate out-of-gamut colors.
    /// </summary>
    public Rgba32 GamutWarningColor { get; set; } = new(255, 0, 255); // Magenta

    public SoftProofing(
        ColorProfile sourceProfile,
        ColorProfile proofProfile,
        RenderingIntent renderingIntent = RenderingIntent.RelativeColorimetric,
        bool simulatePaperWhite = false,
        bool simulateBlackInk = false)
    {
        _sourceProfile = sourceProfile;
        _proofProfile = proofProfile;
        _renderingIntent = renderingIntent;
        _simulatePaperWhite = simulatePaperWhite;
        _simulateBlackInk = simulateBlackInk;
    }

    /// <summary>
    /// Applies soft-proofing to a color.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public Rgba32 Apply(Rgba32 color)
    {
        var (r, g, b, a) = color.ToNormalized();
        var (proofedR, proofedG, proofedB) = ApplyProofing(r, g, b);

        // Check for gamut warning
        if (ShowGamutWarning && !IsInProofGamut(r, g, b))
        {
            return GamutWarningColor;
        }

        return Rgba32.FromNormalized(proofedR, proofedG, proofedB, a);
    }

    /// <summary>
    /// Applies soft-proofing to normalized RGB values.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public (float R, float G, float B) ApplyProofing(float r, float g, float b)
    {
        // For CMYK proofing, convert through CMYK and back
        if (_proofProfile.ProfileType == ColorProfileType.CMYK)
        {
            var cmyk = ColorConverter.RgbToCmyk(r, g, b);
            var (pr, pg, pb) = ColorConverter.CmykToRgb(cmyk.C, cmyk.M, cmyk.Y, cmyk.K);

            if (_simulatePaperWhite)
            {
                // Simulate uncoated paper (slightly warm white)
                pr *= 0.95f;
                pg *= 0.93f;
                pb *= 0.88f;
            }

            if (_simulateBlackInk)
            {
                // Simulate ink density limits
                float minVal = 0.05f;
                pr = MathF.Max(pr, minVal);
                pg = MathF.Max(pg, minVal);
                pb = MathF.Max(pb, minVal);
            }

            return (pr, pg, pb);
        }

        // For RGB proofing profiles, apply gamut mapping
        return _renderingIntent switch
        {
            RenderingIntent.Perceptual => ApplyPerceptualMapping(r, g, b),
            RenderingIntent.Saturation => ApplySaturationMapping(r, g, b),
            RenderingIntent.AbsoluteColorimetric => (r, g, b),
            _ => ApplyRelativeColorimetricMapping(r, g, b)
        };
    }

    /// <summary>
    /// Checks if a color is within the proof profile's gamut.
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public bool IsInProofGamut(float r, float g, float b)
    {
        if (_proofProfile.ProfileType == ColorProfileType.CMYK)
        {
            // CMYK has a smaller gamut than sRGB
            // Check if the round-trip conversion changes the color significantly
            var cmyk = ColorConverter.RgbToCmyk(r, g, b);
            var (backR, backG, backB) = ColorConverter.CmykToRgb(cmyk.C, cmyk.M, cmyk.Y, cmyk.K);

            float deltaR = MathF.Abs(r - backR);
            float deltaG = MathF.Abs(g - backG);
            float deltaB = MathF.Abs(b - backB);

            return deltaR < 0.01f && deltaG < 0.01f && deltaB < 0.01f;
        }

        return ColorConverter.IsInSrgbGamut(r, g, b);
    }

    private (float R, float G, float B) ApplyPerceptualMapping(float r, float g, float b)
    {
        // Perceptual: compress entire gamut to fit
        // Simple implementation: reduce saturation for out-of-gamut colors
        var hsv = HsvColor.FromRgb(r, g, b);
        if (!ColorConverter.IsInSrgbGamut(r, g, b))
        {
            hsv = hsv with { S = hsv.S * 0.8f };
        }
        return hsv.ToRgb();
    }

    private (float R, float G, float B) ApplySaturationMapping(float r, float g, float b)
    {
        // Saturation: maintain relative saturation
        var hsv = HsvColor.FromRgb(r, g, b);
        return hsv.ToRgb();
    }

    private (float R, float G, float B) ApplyRelativeColorimetricMapping(float r, float g, float b)
    {
        // Relative colorimetric: clip out-of-gamut colors
        return ColorConverter.ClampToSrgbGamut(r, g, b);
    }
}

/// <summary>
/// ICC rendering intent for color conversions.
/// </summary>
public enum RenderingIntent
{
    /// <summary>
    /// Perceptual: compress gamut to maintain relationships.
    /// Best for photographs.
    /// </summary>
    Perceptual = 0,

    /// <summary>
    /// Relative Colorimetric: clip out-of-gamut colors, adjust white point.
    /// Best for proofing.
    /// </summary>
    RelativeColorimetric = 1,

    /// <summary>
    /// Saturation: maintain saturation at expense of accuracy.
    /// Best for graphics.
    /// </summary>
    Saturation = 2,

    /// <summary>
    /// Absolute Colorimetric: exact color matching, no white point adjustment.
    /// Best for spot colors.
    /// </summary>
    AbsoluteColorimetric = 3
}
