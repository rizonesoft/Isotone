namespace Gesso.Core.Colors;

/// <summary>
/// Represents a color profile for color management.
/// Wraps ICC profile data and provides color space information.
/// </summary>
public sealed class ColorProfile
{
    /// <summary>
    /// Standard sRGB color profile.
    /// </summary>
    public static ColorProfile SRGB { get; } = new("sRGB", ColorProfileType.RGB,
        whitePoint: (0.3127, 0.3290),
        primaries: new ColorPrimaries(
            red: (0.64, 0.33),
            green: (0.30, 0.60),
            blue: (0.15, 0.06)),
        gamma: 2.2);

    /// <summary>
    /// Adobe RGB (1998) color profile.
    /// </summary>
    public static ColorProfile AdobeRGB { get; } = new("Adobe RGB (1998)", ColorProfileType.RGB,
        whitePoint: (0.3127, 0.3290),
        primaries: new ColorPrimaries(
            red: (0.64, 0.33),
            green: (0.21, 0.71),
            blue: (0.15, 0.06)),
        gamma: 2.2);

    /// <summary>
    /// ProPhoto RGB color profile (wide gamut).
    /// </summary>
    public static ColorProfile ProPhotoRGB { get; } = new("ProPhoto RGB", ColorProfileType.RGB,
        whitePoint: (0.3457, 0.3585), // D50
        primaries: new ColorPrimaries(
            red: (0.7347, 0.2653),
            green: (0.1596, 0.8404),
            blue: (0.0366, 0.0001)),
        gamma: 1.8);

    /// <summary>
    /// Display P3 color profile (Apple wide gamut).
    /// </summary>
    public static ColorProfile DisplayP3 { get; } = new("Display P3", ColorProfileType.RGB,
        whitePoint: (0.3127, 0.3290),
        primaries: new ColorPrimaries(
            red: (0.68, 0.32),
            green: (0.265, 0.69),
            blue: (0.15, 0.06)),
        gamma: 2.2);

    public string Name { get; }
    public ColorProfileType ProfileType { get; }
    public (double X, double Y) WhitePoint { get; }
    public ColorPrimaries? Primaries { get; }
    public double Gamma { get; }
    public byte[]? IccData { get; }

    public ColorProfile(
        string name,
        ColorProfileType profileType,
        (double X, double Y) whitePoint,
        ColorPrimaries? primaries = null,
        double gamma = 2.2,
        byte[]? iccData = null)
    {
        Name = name;
        ProfileType = profileType;
        WhitePoint = whitePoint;
        Primaries = primaries;
        Gamma = gamma;
        IccData = iccData;
    }

    /// <summary>
    /// Creates a color profile from ICC profile data.
    /// </summary>
    public static ColorProfile FromIccData(byte[] iccData, string name = "Custom")
    {
        // Basic ICC parsing - in production, use a proper ICC library
        var profileType = ColorProfileType.RGB;

        if (iccData.Length >= 20)
        {
            // Check color space signature at offset 16
            var colorSpace = System.Text.Encoding.ASCII.GetString(iccData, 16, 4).Trim();
            profileType = colorSpace switch
            {
                "RGB" => ColorProfileType.RGB,
                "CMYK" => ColorProfileType.CMYK,
                "GRAY" => ColorProfileType.Grayscale,
                "Lab" => ColorProfileType.LAB,
                _ => ColorProfileType.RGB
            };
        }

        return new ColorProfile(name, profileType, (0.3127, 0.3290), iccData: iccData);
    }

    public override string ToString() => Name;
}

/// <summary>
/// Type of color profile.
/// </summary>
public enum ColorProfileType
{
    RGB,
    CMYK,
    Grayscale,
    LAB
}

/// <summary>
/// RGB color primaries (chromaticity coordinates).
/// </summary>
public readonly struct ColorPrimaries
{
    public (double X, double Y) Red { get; }
    public (double X, double Y) Green { get; }
    public (double X, double Y) Blue { get; }

    public ColorPrimaries((double X, double Y) red, (double X, double Y) green, (double X, double Y) blue)
    {
        Red = red;
        Green = green;
        Blue = blue;
    }
}
