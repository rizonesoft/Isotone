namespace Bezier.Core.Models.Fills;

using Bezier.Core.Interfaces;

/// <summary>
/// Represents no fill (transparent/none).
/// </summary>
public class NoneFill : IFill
{
    /// <summary>
    /// Singleton instance of NoneFill.
    /// </summary>
    public static NoneFill Instance { get; } = new();

    private NoneFill() { }

    public IFill Clone() => Instance;
}
