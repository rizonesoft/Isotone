namespace Bezier.Core.Interfaces;

/// <summary>
/// Represents a fill for vector elements (solid color, gradient, pattern, etc.)
/// </summary>
/// <remarks>
/// <para>
/// This interface defines the domain model for fills. Rendering conversion to
/// platform-specific paint objects (e.g., SkiaSharp SKPaint) is handled by
/// converter services in the Desktop project to maintain clean separation of concerns.
/// </para>
/// <para>
/// Implementations include:
/// <list type="bullet">
/// <item><description><see cref="Models.Fills.NoneFill"/> - Transparent/no fill</description></item>
/// <item><description><see cref="Models.Fills.SolidFill"/> - Solid color fill</description></item>
/// <item><description><see cref="Models.Fills.LinearGradientFill"/> - Linear gradient</description></item>
/// <item><description><see cref="Models.Fills.RadialGradientFill"/> - Radial gradient</description></item>
/// <item><description><see cref="Models.Fills.PatternFill"/> - Tiled pattern fill</description></item>
/// </list>
/// </para>
/// </remarks>
public interface IFill
{
    /// <summary>
    /// Creates a deep copy of this fill.
    /// </summary>
    /// <returns>A new instance with identical properties.</returns>
    IFill Clone();
}
