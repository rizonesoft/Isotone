namespace Bezier.Core.Models;

/// <summary>
/// Types of transform handles for selection manipulation.
/// </summary>
public enum HandleType
{
    None,
    // Corner handles
    TopLeft,
    TopRight,
    BottomLeft,
    BottomRight,
    // Edge midpoint handles
    TopCenter,
    BottomCenter,
    LeftCenter,
    RightCenter,
    // Rotation handle
    Rotation,
    // Move (center)
    Move
}

/// <summary>
/// Cursor types for different handle interactions.
/// </summary>
public enum HandleCursor
{
    Default,
    Move,
    SizeNWSE,    // Top-left, Bottom-right
    SizeNESW,    // Top-right, Bottom-left
    SizeWE,      // Left, Right
    SizeNS,      // Top, Bottom
    Rotate
}

/// <summary>
/// Represents a transform handle for visual manipulation.
/// </summary>
public readonly record struct TransformHandle(
    HandleType Type,
    double X,
    double Y,
    double Size = 8.0)
{
    /// <summary>
    /// Gets the cursor type for this handle.
    /// </summary>
    public HandleCursor GetCursor() => Type switch
    {
        HandleType.TopLeft or HandleType.BottomRight => HandleCursor.SizeNWSE,
        HandleType.TopRight or HandleType.BottomLeft => HandleCursor.SizeNESW,
        HandleType.LeftCenter or HandleType.RightCenter => HandleCursor.SizeWE,
        HandleType.TopCenter or HandleType.BottomCenter => HandleCursor.SizeNS,
        HandleType.Rotation => HandleCursor.Rotate,
        HandleType.Move => HandleCursor.Move,
        _ => HandleCursor.Default
    };

    /// <summary>
    /// Tests if a point is within this handle's bounds.
    /// </summary>
    public bool HitTest(double px, double py)
    {
        var halfSize = Size / 2;
        return px >= X - halfSize && px <= X + halfSize &&
               py >= Y - halfSize && py <= Y + halfSize;
    }

    /// <summary>
    /// Gets the opposite handle type for proportional resizing.
    /// </summary>
    public HandleType GetOpposite() => Type switch
    {
        HandleType.TopLeft => HandleType.BottomRight,
        HandleType.TopRight => HandleType.BottomLeft,
        HandleType.BottomLeft => HandleType.TopRight,
        HandleType.BottomRight => HandleType.TopLeft,
        HandleType.TopCenter => HandleType.BottomCenter,
        HandleType.BottomCenter => HandleType.TopCenter,
        HandleType.LeftCenter => HandleType.RightCenter,
        HandleType.RightCenter => HandleType.LeftCenter,
        _ => HandleType.None
    };
}

/// <summary>
/// Generates transform handles for a bounding box.
/// </summary>
public static class TransformHandleGenerator
{
    private const double HandleSize = 8.0;
    private const double RotationHandleOffset = 25.0;

    /// <summary>
    /// Generates all handles for a given bounding box.
    /// </summary>
    public static IReadOnlyList<TransformHandle> GenerateHandles(
        double x, double y, double width, double height, 
        bool includeRotation = true)
    {
        var handles = new List<TransformHandle>(10);

        var right = x + width;
        var bottom = y + height;
        var centerX = x + width / 2;
        var centerY = y + height / 2;

        // Corner handles
        handles.Add(new TransformHandle(HandleType.TopLeft, x, y, HandleSize));
        handles.Add(new TransformHandle(HandleType.TopRight, right, y, HandleSize));
        handles.Add(new TransformHandle(HandleType.BottomLeft, x, bottom, HandleSize));
        handles.Add(new TransformHandle(HandleType.BottomRight, right, bottom, HandleSize));

        // Edge midpoint handles
        handles.Add(new TransformHandle(HandleType.TopCenter, centerX, y, HandleSize));
        handles.Add(new TransformHandle(HandleType.BottomCenter, centerX, bottom, HandleSize));
        handles.Add(new TransformHandle(HandleType.LeftCenter, x, centerY, HandleSize));
        handles.Add(new TransformHandle(HandleType.RightCenter, right, centerY, HandleSize));

        // Rotation handle (above top center)
        if (includeRotation)
        {
            handles.Add(new TransformHandle(HandleType.Rotation, centerX, y - RotationHandleOffset, HandleSize));
        }

        return handles;
    }

    /// <summary>
    /// Gets the anchor point for a resize operation based on handle type.
    /// </summary>
    public static (double X, double Y) GetAnchorPoint(
        HandleType handle, double x, double y, double width, double height)
    {
        var right = x + width;
        var bottom = y + height;
        var centerX = x + width / 2;
        var centerY = y + height / 2;

        return handle switch
        {
            HandleType.TopLeft => (right, bottom),
            HandleType.TopRight => (x, bottom),
            HandleType.BottomLeft => (right, y),
            HandleType.BottomRight => (x, y),
            HandleType.TopCenter => (centerX, bottom),
            HandleType.BottomCenter => (centerX, y),
            HandleType.LeftCenter => (right, centerY),
            HandleType.RightCenter => (x, centerY),
            _ => (centerX, centerY)
        };
    }
}
