namespace Bezier.Core.Models;

/// <summary>
/// Types of control points for bezier paths.
/// </summary>
public enum ControlPointType
{
    /// <summary>
    /// Corner point - handles move independently.
    /// </summary>
    Corner,

    /// <summary>
    /// Smooth point - handles are collinear but can have different lengths.
    /// </summary>
    Smooth,

    /// <summary>
    /// Symmetric point - handles are collinear and equal length.
    /// </summary>
    Symmetric
}

/// <summary>
/// Represents a control point on a bezier path with optional handles.
/// </summary>
public class ControlPoint
{
    /// <summary>
    /// Gets or sets the position of the anchor point.
    /// </summary>
    public (double X, double Y) Position { get; set; }

    /// <summary>
    /// Gets or sets the incoming control handle (relative to position).
    /// Null for corner points without incoming curve.
    /// </summary>
    public (double X, double Y)? InHandle { get; set; }

    /// <summary>
    /// Gets or sets the outgoing control handle (relative to position).
    /// Null for corner points without outgoing curve.
    /// </summary>
    public (double X, double Y)? OutHandle { get; set; }

    /// <summary>
    /// Gets or sets the type of this control point.
    /// </summary>
    public ControlPointType Type { get; set; } = ControlPointType.Corner;

    /// <summary>
    /// Gets the absolute position of the incoming handle.
    /// </summary>
    public (double X, double Y)? InHandleAbsolute => InHandle.HasValue
        ? (Position.X + InHandle.Value.X, Position.Y + InHandle.Value.Y)
        : null;

    /// <summary>
    /// Gets the absolute position of the outgoing handle.
    /// </summary>
    public (double X, double Y)? OutHandleAbsolute => OutHandle.HasValue
        ? (Position.X + OutHandle.Value.X, Position.Y + OutHandle.Value.Y)
        : null;

    /// <summary>
    /// Creates a corner point at the specified position.
    /// </summary>
    public static ControlPoint CreateCorner(double x, double y) => new()
    {
        Position = (x, y),
        Type = ControlPointType.Corner
    };

    /// <summary>
    /// Creates a smooth point with symmetric handles.
    /// </summary>
    public static ControlPoint CreateSmooth(double x, double y, double handleX, double handleY) => new()
    {
        Position = (x, y),
        InHandle = (-handleX, -handleY),
        OutHandle = (handleX, handleY),
        Type = ControlPointType.Smooth
    };

    /// <summary>
    /// Creates a symmetric point with equal-length handles.
    /// </summary>
    public static ControlPoint CreateSymmetric(double x, double y, double handleX, double handleY) => new()
    {
        Position = (x, y),
        InHandle = (-handleX, -handleY),
        OutHandle = (handleX, handleY),
        Type = ControlPointType.Symmetric
    };

    /// <summary>
    /// Sets the outgoing handle and adjusts the incoming handle based on point type.
    /// </summary>
    public void SetOutHandle(double x, double y)
    {
        OutHandle = (x, y);

        switch (Type)
        {
            case ControlPointType.Smooth:
                // Keep handles collinear but allow different lengths
                var outLength = Math.Sqrt(x * x + y * y);
                if (outLength > 0 && InHandle.HasValue)
                {
                    var inLength = Math.Sqrt(InHandle.Value.X * InHandle.Value.X + InHandle.Value.Y * InHandle.Value.Y);
                    var scale = inLength / outLength;
                    InHandle = (-x * scale, -y * scale);
                }
                else
                {
                    InHandle = (-x, -y);
                }
                break;

            case ControlPointType.Symmetric:
                // Handles are always opposite and equal length
                InHandle = (-x, -y);
                break;

            case ControlPointType.Corner:
                // Independent handles - don't adjust InHandle
                break;
        }
    }

    /// <summary>
    /// Sets the incoming handle and adjusts the outgoing handle based on point type.
    /// </summary>
    public void SetInHandle(double x, double y)
    {
        InHandle = (x, y);

        switch (Type)
        {
            case ControlPointType.Smooth:
                var inLength = Math.Sqrt(x * x + y * y);
                if (inLength > 0 && OutHandle.HasValue)
                {
                    var outLength = Math.Sqrt(OutHandle.Value.X * OutHandle.Value.X + OutHandle.Value.Y * OutHandle.Value.Y);
                    var scale = outLength / inLength;
                    OutHandle = (-x * scale, -y * scale);
                }
                else
                {
                    OutHandle = (-x, -y);
                }
                break;

            case ControlPointType.Symmetric:
                OutHandle = (-x, -y);
                break;

            case ControlPointType.Corner:
                break;
        }
    }

    /// <summary>
    /// Converts this point to a corner type (handles become independent).
    /// </summary>
    public void ConvertToCorner()
    {
        Type = ControlPointType.Corner;
    }

    /// <summary>
    /// Converts this point to smooth type (handles become collinear).
    /// </summary>
    public void ConvertToSmooth()
    {
        Type = ControlPointType.Smooth;
        if (OutHandle.HasValue)
        {
            SetOutHandle(OutHandle.Value.X, OutHandle.Value.Y);
        }
    }

    /// <summary>
    /// Converts this point to symmetric type (handles become equal).
    /// </summary>
    public void ConvertToSymmetric()
    {
        Type = ControlPointType.Symmetric;
        if (OutHandle.HasValue)
        {
            SetOutHandle(OutHandle.Value.X, OutHandle.Value.Y);
        }
    }

    /// <summary>
    /// Tests if a point is near this control point's anchor.
    /// </summary>
    public bool HitTestAnchor(double x, double y, double tolerance = 8)
    {
        var dx = Position.X - x;
        var dy = Position.Y - y;
        return dx * dx + dy * dy <= tolerance * tolerance;
    }

    /// <summary>
    /// Tests if a point is near the incoming handle.
    /// </summary>
    public bool HitTestInHandle(double x, double y, double tolerance = 6)
    {
        if (!InHandleAbsolute.HasValue) return false;
        var (hx, hy) = InHandleAbsolute.Value;
        var dx = hx - x;
        var dy = hy - y;
        return dx * dx + dy * dy <= tolerance * tolerance;
    }

    /// <summary>
    /// Tests if a point is near the outgoing handle.
    /// </summary>
    public bool HitTestOutHandle(double x, double y, double tolerance = 6)
    {
        if (!OutHandleAbsolute.HasValue) return false;
        var (hx, hy) = OutHandleAbsolute.Value;
        var dx = hx - x;
        var dy = hy - y;
        return dx * dx + dy * dy <= tolerance * tolerance;
    }

    /// <summary>
    /// Creates a deep copy of this control point.
    /// </summary>
    public ControlPoint Clone() => new()
    {
        Position = Position,
        InHandle = InHandle,
        OutHandle = OutHandle,
        Type = Type
    };
}
