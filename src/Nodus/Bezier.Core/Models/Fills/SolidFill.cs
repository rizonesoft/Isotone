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

    public IFill Clone() => new SolidFill { Color = this.Color };
}
