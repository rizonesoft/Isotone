namespace Bezier.Core.Models.Fills;

using Bezier.Core.Interfaces;

/// <summary>
/// Represents a pattern fill (tiled element reference).
/// </summary>
public class PatternFill : IFill
{
    /// <summary>Reference ID of the pattern element in defs.</summary>
    public string PatternId { get; set; } = string.Empty;

    /// <summary>Pattern tile width.</summary>
    public double Width { get; set; } = 10;

    /// <summary>Pattern tile height.</summary>
    public double Height { get; set; } = 10;

    /// <summary>Pattern X offset.</summary>
    public double X { get; set; }

    /// <summary>Pattern Y offset.</summary>
    public double Y { get; set; }

    /// <summary>Pattern units (userSpaceOnUse or objectBoundingBox).</summary>
    public bool UseObjectBoundingBox { get; set; } = true;

    public IFill Clone() => new PatternFill
    {
        PatternId = PatternId,
        Width = Width,
        Height = Height,
        X = X,
        Y = Y,
        UseObjectBoundingBox = UseObjectBoundingBox
    };
}
