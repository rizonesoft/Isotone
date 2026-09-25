namespace Bezier.Core.Models.Fills;

using Bezier.Core.Interfaces;

/// <summary>
/// Gradient spread mode for how colors extend beyond the gradient bounds.
/// </summary>
public enum GradientSpreadMode
{
    /// <summary>Extend edge colors beyond bounds.</summary>
    Pad,
    /// <summary>Reflect/mirror the gradient.</summary>
    Reflect,
    /// <summary>Repeat the gradient pattern.</summary>
    Repeat
}

/// <summary>
/// Represents a color stop in a gradient.
/// </summary>
public readonly struct GradientStop
{
    /// <summary>Position along the gradient (0.0 to 1.0).</summary>
    public double Offset { get; init; }

    /// <summary>Color at this stop in ARGB format.</summary>
    public uint Color { get; init; }

    public GradientStop(double offset, uint color)
    {
        Offset = Math.Clamp(offset, 0.0, 1.0);
        Color = color;
    }

    /// <summary>Creates a gradient stop from RGBA values.</summary>
    public static GradientStop FromRgba(double offset, byte r, byte g, byte b, byte a = 255)
    {
        var color = ((uint)a << 24) | ((uint)r << 16) | ((uint)g << 8) | b;
        return new GradientStop(offset, color);
    }
}

/// <summary>
/// Represents a linear gradient fill.
/// </summary>
public class LinearGradientFill : IFill
{
    /// <summary>Start X coordinate (0.0 to 1.0 relative to element bounds).</summary>
    public double StartX { get; set; }

    /// <summary>Start Y coordinate (0.0 to 1.0 relative to element bounds).</summary>
    public double StartY { get; set; }

    /// <summary>End X coordinate (0.0 to 1.0 relative to element bounds).</summary>
    public double EndX { get; set; } = 1.0;

    /// <summary>End Y coordinate (0.0 to 1.0 relative to element bounds).</summary>
    public double EndY { get; set; }

    /// <summary>Gradient color stops.</summary>
    public List<GradientStop> Stops { get; set; } = [];

    /// <summary>How colors extend beyond the gradient bounds.</summary>
    public GradientSpreadMode SpreadMode { get; set; } = GradientSpreadMode.Pad;

    /// <summary>
    /// Creates a simple two-color horizontal gradient.
    /// </summary>
    public static LinearGradientFill Create(uint startColor, uint endColor)
    {
        return new LinearGradientFill
        {
            StartX = 0, StartY = 0.5,
            EndX = 1, EndY = 0.5,
            Stops =
            [
                new GradientStop(0, startColor),
                new GradientStop(1, endColor)
            ]
        };
    }

    public IFill Clone() => new LinearGradientFill
    {
        StartX = StartX,
        StartY = StartY,
        EndX = EndX,
        EndY = EndY,
        Stops = [.. Stops],
        SpreadMode = SpreadMode
    };
}
