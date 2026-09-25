namespace Bezier.Core.Models.Fills;

using Bezier.Core.Interfaces;

/// <summary>
/// Represents a solid color fill.
/// </summary>
public class SolidFill : IFill
{
    /// <summary>
    /// Gets or sets the fill color in ARGB format.
    /// </summary>
    public uint Color { get; set; } = 0xFF000000; // Black

    /// <summary>
    /// Gets or sets the red component (0-255).
    /// </summary>
    public byte R
    {
        get => (byte)((Color >> 16) & 0xFF);
        set => Color = (Color & 0xFF00FFFF) | ((uint)value << 16);
    }

    /// <summary>
    /// Gets or sets the green component (0-255).
    /// </summary>
    public byte G
    {
        get => (byte)((Color >> 8) & 0xFF);
        set => Color = (Color & 0xFFFF00FF) | ((uint)value << 8);
    }

    /// <summary>
    /// Gets or sets the blue component (0-255).
    /// </summary>
    public byte B
    {
        get => (byte)(Color & 0xFF);
        set => Color = (Color & 0xFFFFFF00) | value;
    }

    /// <summary>
    /// Gets or sets the alpha component (0-255).
    /// </summary>
    public byte A
    {
        get => (byte)((Color >> 24) & 0xFF);
        set => Color = (Color & 0x00FFFFFF) | ((uint)value << 24);
    }

    /// <summary>
    /// Gets or sets the opacity (0.0 to 1.0).
    /// </summary>
    public double Opacity
    {
        get => A / 255.0;
        set => A = (byte)(Math.Clamp(value, 0, 1) * 255);
    }

    /// <summary>
    /// Creates a solid fill from RGB values with optional alpha.
    /// </summary>
    public static SolidFill FromRgb(byte r, byte g, byte b, byte a = 255) => new()
    {
        Color = ((uint)a << 24) | ((uint)r << 16) | ((uint)g << 8) | b
    };

    /// <summary>
    /// Creates a solid fill from a hex color string (#RGB, #RRGGBB, or #AARRGGBB).
    /// </summary>
    public static SolidFill FromHex(string hex)
    {
        hex = hex.TrimStart('#');
        uint color = 0xFF000000;

        if (hex.Length == 3)
        {
            var r = Convert.ToByte(new string(hex[0], 2), 16);
            var g = Convert.ToByte(new string(hex[1], 2), 16);
            var b = Convert.ToByte(new string(hex[2], 2), 16);
            color = 0xFF000000 | ((uint)r << 16) | ((uint)g << 8) | b;
        }
        else if (hex.Length == 6)
        {
            var r = Convert.ToByte(hex[..2], 16);
            var g = Convert.ToByte(hex[2..4], 16);
            var b = Convert.ToByte(hex[4..6], 16);
            color = 0xFF000000 | ((uint)r << 16) | ((uint)g << 8) | b;
        }
        else if (hex.Length == 8)
        {
            color = Convert.ToUInt32(hex, 16);
        }

        return new SolidFill { Color = color };
    }

    /// <summary>Common colors.</summary>
    public static SolidFill Black => new() { Color = 0xFF000000 };
    public static SolidFill White => new() { Color = 0xFFFFFFFF };
    public static SolidFill Red => new() { Color = 0xFFFF0000 };
    public static SolidFill Green => new() { Color = 0xFF00FF00 };
    public static SolidFill Blue => new() { Color = 0xFF0000FF };
    public static SolidFill Transparent => new() { Color = 0x00000000 };

    public IFill Clone() => new SolidFill { Color = Color };
}

