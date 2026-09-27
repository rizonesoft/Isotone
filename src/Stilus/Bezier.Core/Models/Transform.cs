namespace Bezier.Core.Models;

/// <summary>
/// Represents a 2D transformation matrix (3x3 affine matrix).
/// Supports translate, rotate, scale, and skew operations.
/// </summary>
public readonly struct Transform
{
    /// <summary>Scale X (M11)</summary>
    public double ScaleX { get; init; }
    
    /// <summary>Skew Y (M12)</summary>
    public double SkewY { get; init; }
    
    /// <summary>Skew X (M21)</summary>
    public double SkewX { get; init; }
    
    /// <summary>Scale Y (M22)</summary>
    public double ScaleY { get; init; }
    
    /// <summary>Translate X (M31)</summary>
    public double TranslateX { get; init; }
    
    /// <summary>Translate Y (M32)</summary>
    public double TranslateY { get; init; }

    /// <summary>
    /// Identity transform (no transformation).
    /// </summary>
    public static Transform Identity => new()
    {
        ScaleX = 1,
        ScaleY = 1,
        SkewX = 0,
        SkewY = 0,
        TranslateX = 0,
        TranslateY = 0
    };

    /// <summary>
    /// Creates a translation transform.
    /// </summary>
    public static Transform CreateTranslation(double x, double y) => new()
    {
        ScaleX = 1,
        ScaleY = 1,
        TranslateX = x,
        TranslateY = y
    };

    /// <summary>
    /// Creates a scale transform.
    /// </summary>
    public static Transform CreateScale(double scaleX, double scaleY) => new()
    {
        ScaleX = scaleX,
        ScaleY = scaleY,
        TranslateX = 0,
        TranslateY = 0
    };

    /// <summary>
    /// Creates a rotation transform (angle in degrees).
    /// </summary>
    public static Transform CreateRotation(double angleDegrees)
    {
        var radians = angleDegrees * Math.PI / 180.0;
        var cos = Math.Cos(radians);
        var sin = Math.Sin(radians);
        return new Transform
        {
            ScaleX = cos,
            SkewY = sin,
            SkewX = -sin,
            ScaleY = cos,
            TranslateX = 0,
            TranslateY = 0
        };
    }

    /// <summary>
    /// Creates a rotation transform around a specific point.
    /// </summary>
    public static Transform CreateRotation(double angleDegrees, double centerX, double centerY)
    {
        return CreateTranslation(-centerX, -centerY)
            .Multiply(CreateRotation(angleDegrees))
            .Multiply(CreateTranslation(centerX, centerY));
    }

    /// <summary>
    /// Creates a skew transform (angles in degrees).
    /// </summary>
    public static Transform CreateSkew(double skewXDegrees, double skewYDegrees)
    {
        var tanX = Math.Tan(skewXDegrees * Math.PI / 180.0);
        var tanY = Math.Tan(skewYDegrees * Math.PI / 180.0);
        return new Transform
        {
            ScaleX = 1,
            SkewY = tanY,
            SkewX = tanX,
            ScaleY = 1,
            TranslateX = 0,
            TranslateY = 0
        };
    }

    /// <summary>
    /// Multiplies this transform by another transform.
    /// </summary>
    public Transform Multiply(Transform other)
    {
        return new Transform
        {
            ScaleX = ScaleX * other.ScaleX + SkewY * other.SkewX,
            SkewY = ScaleX * other.SkewY + SkewY * other.ScaleY,
            SkewX = SkewX * other.ScaleX + ScaleY * other.SkewX,
            ScaleY = SkewX * other.SkewY + ScaleY * other.ScaleY,
            TranslateX = TranslateX * other.ScaleX + TranslateY * other.SkewX + other.TranslateX,
            TranslateY = TranslateX * other.SkewY + TranslateY * other.ScaleY + other.TranslateY
        };
    }

    /// <summary>
    /// Computes the inverse of this transform.
    /// </summary>
    public Transform Invert()
    {
        var det = ScaleX * ScaleY - SkewX * SkewY;
        if (Math.Abs(det) < double.Epsilon)
        {
            return Identity; // Non-invertible, return identity
        }

        var invDet = 1.0 / det;
        return new Transform
        {
            ScaleX = ScaleY * invDet,
            SkewY = -SkewY * invDet,
            SkewX = -SkewX * invDet,
            ScaleY = ScaleX * invDet,
            TranslateX = (SkewX * TranslateY - ScaleY * TranslateX) * invDet,
            TranslateY = (SkewY * TranslateX - ScaleX * TranslateY) * invDet
        };
    }

    /// <summary>
    /// Transforms a point using this matrix.
    /// </summary>
    public (double X, double Y) TransformPoint(double x, double y)
    {
        return (
            x * ScaleX + y * SkewX + TranslateX,
            x * SkewY + y * ScaleY + TranslateY
        );
    }

    /// <summary>
    /// Returns whether this is the identity transform.
    /// </summary>
    public bool IsIdentity => 
        Math.Abs(ScaleX - 1) < double.Epsilon &&
        Math.Abs(ScaleY - 1) < double.Epsilon &&
        Math.Abs(SkewX) < double.Epsilon &&
        Math.Abs(SkewY) < double.Epsilon &&
        Math.Abs(TranslateX) < double.Epsilon &&
        Math.Abs(TranslateY) < double.Epsilon;

    /// <summary>
    /// Converts to SVG transform attribute string.
    /// </summary>
    public string ToSvgString()
    {
        if (IsIdentity)
            return string.Empty;

        return $"matrix({ScaleX:G6},{SkewY:G6},{SkewX:G6},{ScaleY:G6},{TranslateX:G6},{TranslateY:G6})";
    }

    public override string ToString() => ToSvgString();
}
