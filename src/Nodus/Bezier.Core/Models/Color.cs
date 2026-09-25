namespace Bezier.Core.Models;

/// <summary>
/// Represents a color with RGBA components and conversion utilities.
/// </summary>
public readonly struct Color : IEquatable<Color>
{
    /// <summary>Red component (0-255).</summary>
    public byte R { get; init; }

    /// <summary>Green component (0-255).</summary>
    public byte G { get; init; }

    /// <summary>Blue component (0-255).</summary>
    public byte B { get; init; }

    /// <summary>Alpha component (0-255).</summary>
    public byte A { get; init; }

    /// <summary>
    /// Creates a color from RGBA components.
    /// </summary>
    public Color(byte r, byte g, byte b, byte a = 255)
    {
        R = r;
        G = g;
        B = b;
        A = a;
    }

    /// <summary>
    /// Creates a color from a 32-bit ARGB value.
    /// </summary>
    public static Color FromArgb(uint argb) => new(
        (byte)((argb >> 16) & 0xFF),
        (byte)((argb >> 8) & 0xFF),
        (byte)(argb & 0xFF),
        (byte)((argb >> 24) & 0xFF)
    );

    /// <summary>
    /// Creates a color from RGB components with full opacity.
    /// </summary>
    public static Color FromRgb(byte r, byte g, byte b) => new(r, g, b, 255);

    /// <summary>
    /// Creates a color from HSL values.
    /// </summary>
    /// <param name="h">Hue (0-360)</param>
    /// <param name="s">Saturation (0-1)</param>
    /// <param name="l">Lightness (0-1)</param>
    /// <param name="a">Alpha (0-255)</param>
    public static Color FromHsl(double h, double s, double l, byte a = 255)
    {
        h = ((h % 360) + 360) % 360;
        s = Math.Clamp(s, 0, 1);
        l = Math.Clamp(l, 0, 1);

        var c = (1 - Math.Abs(2 * l - 1)) * s;
        var x = c * (1 - Math.Abs((h / 60) % 2 - 1));
        var m = l - c / 2;

        double r, g, b;
        if (h < 60) { r = c; g = x; b = 0; }
        else if (h < 120) { r = x; g = c; b = 0; }
        else if (h < 180) { r = 0; g = c; b = x; }
        else if (h < 240) { r = 0; g = x; b = c; }
        else if (h < 300) { r = x; g = 0; b = c; }
        else { r = c; g = 0; b = x; }

        return new Color(
            (byte)Math.Round((r + m) * 255),
            (byte)Math.Round((g + m) * 255),
            (byte)Math.Round((b + m) * 255),
            a
        );
    }

    /// <summary>
    /// Creates a color from HSV values.
    /// </summary>
    /// <param name="h">Hue (0-360)</param>
    /// <param name="s">Saturation (0-1)</param>
    /// <param name="v">Value/Brightness (0-1)</param>
    /// <param name="a">Alpha (0-255)</param>
    public static Color FromHsv(double h, double s, double v, byte a = 255)
    {
        h = ((h % 360) + 360) % 360;
        s = Math.Clamp(s, 0, 1);
        v = Math.Clamp(v, 0, 1);

        var c = v * s;
        var x = c * (1 - Math.Abs((h / 60) % 2 - 1));
        var m = v - c;

        double r, g, b;
        if (h < 60) { r = c; g = x; b = 0; }
        else if (h < 120) { r = x; g = c; b = 0; }
        else if (h < 180) { r = 0; g = c; b = x; }
        else if (h < 240) { r = 0; g = x; b = c; }
        else if (h < 300) { r = x; g = 0; b = c; }
        else { r = c; g = 0; b = x; }

        return new Color(
            (byte)Math.Round((r + m) * 255),
            (byte)Math.Round((g + m) * 255),
            (byte)Math.Round((b + m) * 255),
            a
        );
    }

    /// <summary>
    /// Parses a hex color string (#RGB, #RGBA, #RRGGBB, #RRGGBBAA).
    /// </summary>
    public static Color FromHex(string hex)
    {
        if (string.IsNullOrEmpty(hex))
            return new Color(0, 0, 0, 255);

        hex = hex.TrimStart('#');

        return hex.Length switch
        {
            3 => new Color(
                (byte)(Convert.ToByte(hex[0..1], 16) * 17),
                (byte)(Convert.ToByte(hex[1..2], 16) * 17),
                (byte)(Convert.ToByte(hex[2..3], 16) * 17),
                255),
            4 => new Color(
                (byte)(Convert.ToByte(hex[0..1], 16) * 17),
                (byte)(Convert.ToByte(hex[1..2], 16) * 17),
                (byte)(Convert.ToByte(hex[2..3], 16) * 17),
                (byte)(Convert.ToByte(hex[3..4], 16) * 17)),
            6 => new Color(
                Convert.ToByte(hex[0..2], 16),
                Convert.ToByte(hex[2..4], 16),
                Convert.ToByte(hex[4..6], 16),
                255),
            8 => new Color(
                Convert.ToByte(hex[0..2], 16),
                Convert.ToByte(hex[2..4], 16),
                Convert.ToByte(hex[4..6], 16),
                Convert.ToByte(hex[6..8], 16)),
            _ => new Color(0, 0, 0, 255)
        };
    }

    /// <summary>
    /// Converts to 32-bit ARGB value.
    /// </summary>
    public uint ToArgb() => (uint)((A << 24) | (R << 16) | (G << 8) | B);

    /// <summary>
    /// Converts to hex string (#RRGGBB or #RRGGBBAA if alpha != 255).
    /// </summary>
    public string ToHex(bool includeAlpha = false)
    {
        if (includeAlpha || A != 255)
            return $"#{R:X2}{G:X2}{B:X2}{A:X2}";
        return $"#{R:X2}{G:X2}{B:X2}";
    }

    /// <summary>
    /// Converts to HSL values.
    /// </summary>
    public (double H, double S, double L) ToHsl()
    {
        var r = R / 255.0;
        var g = G / 255.0;
        var b = B / 255.0;

        var max = Math.Max(r, Math.Max(g, b));
        var min = Math.Min(r, Math.Min(g, b));
        var l = (max + min) / 2;

        if (Math.Abs(max - min) < double.Epsilon)
            return (0, 0, l);

        var d = max - min;
        var s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

        double h;
        if (Math.Abs(max - r) < double.Epsilon)
            h = ((g - b) / d + (g < b ? 6 : 0)) * 60;
        else if (Math.Abs(max - g) < double.Epsilon)
            h = ((b - r) / d + 2) * 60;
        else
            h = ((r - g) / d + 4) * 60;

        return (h, s, l);
    }

    /// <summary>
    /// Converts to HSV values.
    /// </summary>
    public (double H, double S, double V) ToHsv()
    {
        var r = R / 255.0;
        var g = G / 255.0;
        var b = B / 255.0;

        var max = Math.Max(r, Math.Max(g, b));
        var min = Math.Min(r, Math.Min(g, b));
        var v = max;

        if (Math.Abs(max - min) < double.Epsilon)
            return (0, 0, v);

        var d = max - min;
        var s = max > 0 ? d / max : 0;

        double h;
        if (Math.Abs(max - r) < double.Epsilon)
            h = ((g - b) / d + (g < b ? 6 : 0)) * 60;
        else if (Math.Abs(max - g) < double.Epsilon)
            h = ((b - r) / d + 2) * 60;
        else
            h = ((r - g) / d + 4) * 60;

        return (h, s, v);
    }

    /// <summary>
    /// Returns a new color with modified alpha.
    /// </summary>
    public Color WithAlpha(byte alpha) => new(R, G, B, alpha);

    /// <summary>
    /// Returns a new color with modified alpha (0-1 range).
    /// </summary>
    public Color WithAlpha(double alpha) => new(R, G, B, (byte)(Math.Clamp(alpha, 0, 1) * 255));

    /// <summary>
    /// Linearly interpolates between two colors.
    /// </summary>
    public static Color Lerp(Color a, Color b, double t)
    {
        t = Math.Clamp(t, 0, 1);
        return new Color(
            (byte)(a.R + (b.R - a.R) * t),
            (byte)(a.G + (b.G - a.G) * t),
            (byte)(a.B + (b.B - a.B) * t),
            (byte)(a.A + (b.A - a.A) * t)
        );
    }

    /// <summary>
    /// Gets the luminance (perceived brightness) of the color.
    /// </summary>
    public double Luminance => 0.299 * R / 255 + 0.587 * G / 255 + 0.114 * B / 255;

    /// <summary>
    /// Returns whether this is a light color (luminance > 0.5).
    /// </summary>
    public bool IsLight => Luminance > 0.5;

    /// <summary>
    /// Returns a contrasting color (black or white) for readability.
    /// </summary>
    public Color ContrastColor => IsLight ? Black : White;

    // Common colors
    public static Color Transparent => new(0, 0, 0, 0);
    public static Color Black => new(0, 0, 0, 255);
    public static Color White => new(255, 255, 255, 255);
    public static Color Red => new(255, 0, 0, 255);
    public static Color Green => new(0, 255, 0, 255);
    public static Color Blue => new(0, 0, 255, 255);
    public static Color Yellow => new(255, 255, 0, 255);
    public static Color Cyan => new(0, 255, 255, 255);
    public static Color Magenta => new(255, 0, 255, 255);

    public bool Equals(Color other) => R == other.R && G == other.G && B == other.B && A == other.A;
    public override bool Equals(object? obj) => obj is Color other && Equals(other);
    public override int GetHashCode() => HashCode.Combine(R, G, B, A);
    public static bool operator ==(Color left, Color right) => left.Equals(right);
    public static bool operator !=(Color left, Color right) => !left.Equals(right);

    public override string ToString() => ToHex(A != 255);
}
