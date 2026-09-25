namespace Bezier.Core.Models;

using Bezier.Core.Interfaces;

/// <summary>
/// Line cap style for stroke endpoints.
/// </summary>
public enum LineCap
{
    Butt,
    Round,
    Square
}

/// <summary>
/// Line join style for stroke corners.
/// </summary>
public enum LineJoin
{
    Miter,
    Round,
    Bevel
}

/// <summary>
/// Represents stroke properties for vector elements.
/// </summary>
public class Stroke
{
    /// <summary>
    /// The stroke fill (color, gradient, etc). Null means no stroke.
    /// </summary>
    public IFill? Fill { get; set; }

    /// <summary>
    /// Stroke width in pixels.
    /// </summary>
    public double Width { get; set; } = 1.0;

    /// <summary>
    /// Stroke opacity from 0.0 to 1.0.
    /// </summary>
    public double Opacity { get; set; } = 1.0;

    /// <summary>
    /// Line cap style.
    /// </summary>
    public LineCap LineCap { get; set; } = LineCap.Butt;

    /// <summary>
    /// Line join style.
    /// </summary>
    public LineJoin LineJoin { get; set; } = LineJoin.Miter;

    /// <summary>
    /// Miter limit for miter joins.
    /// </summary>
    public double MiterLimit { get; set; } = 4.0;

    /// <summary>
    /// Dash array for dashed lines. Null means solid line.
    /// </summary>
    public double[]? DashArray { get; set; }

    /// <summary>
    /// Dash offset for dashed lines.
    /// </summary>
    public double DashOffset { get; set; }

    /// <summary>
    /// Creates a deep copy of this stroke.
    /// </summary>
    public Stroke Clone() => new()
    {
        Fill = Fill?.Clone(),
        Width = Width,
        Opacity = Opacity,
        LineCap = LineCap,
        LineJoin = LineJoin,
        MiterLimit = MiterLimit,
        DashArray = DashArray?.ToArray(),
        DashOffset = DashOffset
    };

    /// <summary>
    /// Returns whether this stroke should be rendered.
    /// </summary>
    public bool IsVisible => Fill is not null && Width > 0 && Opacity > 0;
}
