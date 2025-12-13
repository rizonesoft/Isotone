namespace Bezier.Core.Interfaces;

/// <summary>
/// Represents a fill for vector elements (solid color, gradient, pattern, etc.)
/// </summary>
public interface IFill
{
    /// <summary>
    /// Creates a deep copy of this fill.
    /// </summary>
    IFill Clone();
}
