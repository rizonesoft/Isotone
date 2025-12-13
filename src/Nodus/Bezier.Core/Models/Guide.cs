namespace Bezier.Core.Models;

/// <summary>
/// Orientation of a guide line.
/// </summary>
public enum GuideOrientation
{
    Horizontal,
    Vertical
}

/// <summary>
/// Represents a guide line on the canvas.
/// </summary>
public class Guide
{
    /// <summary>
    /// Gets or sets the unique identifier for this guide.
    /// </summary>
    public Guid Id { get; set; } = Guid.NewGuid();

    /// <summary>
    /// Gets or sets the orientation of the guide.
    /// </summary>
    public GuideOrientation Orientation { get; set; }

    /// <summary>
    /// Gets or sets the position of the guide (X for vertical, Y for horizontal).
    /// </summary>
    public double Position { get; set; }

    /// <summary>
    /// Gets or sets whether the guide is locked.
    /// </summary>
    public bool IsLocked { get; set; }

    /// <summary>
    /// Gets or sets the color of the guide (ARGB).
    /// </summary>
    public uint Color { get; set; } = 0xFF00BFFF; // Deep sky blue

    /// <summary>
    /// Creates a horizontal guide at the specified Y position.
    /// </summary>
    public static Guide Horizontal(double y) => new()
    {
        Orientation = GuideOrientation.Horizontal,
        Position = y
    };

    /// <summary>
    /// Creates a vertical guide at the specified X position.
    /// </summary>
    public static Guide Vertical(double x) => new()
    {
        Orientation = GuideOrientation.Vertical,
        Position = x
    };

    /// <summary>
    /// Tests if a point is near this guide.
    /// </summary>
    public bool HitTest(double x, double y, double tolerance = 5)
    {
        return Orientation switch
        {
            GuideOrientation.Horizontal => Math.Abs(y - Position) <= tolerance,
            GuideOrientation.Vertical => Math.Abs(x - Position) <= tolerance,
            _ => false
        };
    }
}
