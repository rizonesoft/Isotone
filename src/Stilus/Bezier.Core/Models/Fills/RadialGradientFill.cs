namespace Bezier.Core.Models.Fills;

using Bezier.Core.Interfaces;

/// <summary>
/// Represents a radial gradient fill.
/// </summary>
public class RadialGradientFill : IFill
{
    /// <summary>Center X coordinate (0.0 to 1.0 relative to element bounds).</summary>
    public double CenterX { get; set; } = 0.5;

    /// <summary>Center Y coordinate (0.0 to 1.0 relative to element bounds).</summary>
    public double CenterY { get; set; } = 0.5;

    /// <summary>Radius X (0.0 to 1.0 relative to element width).</summary>
    public double RadiusX { get; set; } = 0.5;

    /// <summary>Radius Y (0.0 to 1.0 relative to element height).</summary>
    public double RadiusY { get; set; } = 0.5;

    /// <summary>Focal point X (0.0 to 1.0, defaults to center).</summary>
    public double FocalX { get; set; } = 0.5;

    /// <summary>Focal point Y (0.0 to 1.0, defaults to center).</summary>
    public double FocalY { get; set; } = 0.5;

    /// <summary>Gradient color stops.</summary>
    public List<GradientStop> Stops { get; set; } = [];

    /// <summary>How colors extend beyond the gradient bounds.</summary>
    public GradientSpreadMode SpreadMode { get; set; } = GradientSpreadMode.Pad;

    /// <summary>
    /// Creates a simple two-color radial gradient.
    /// </summary>
    public static RadialGradientFill Create(uint centerColor, uint edgeColor)
    {
        return new RadialGradientFill
        {
            CenterX = 0.5, CenterY = 0.5,
            RadiusX = 0.5, RadiusY = 0.5,
            Stops =
            [
                new GradientStop(0, centerColor),
                new GradientStop(1, edgeColor)
            ]
        };
    }

    public IFill Clone() => new RadialGradientFill
    {
        CenterX = CenterX,
        CenterY = CenterY,
        RadiusX = RadiusX,
        RadiusY = RadiusY,
        FocalX = FocalX,
        FocalY = FocalY,
        Stops = [.. Stops],
        SpreadMode = SpreadMode
    };
}
