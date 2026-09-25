namespace Bezier.Core.Services;

using Bezier.Core.Models;

/// <summary>
/// Provides transform operations for vector elements.
/// </summary>
public static class TransformService
{
    /// <summary>
    /// Calculates the new bounds after a resize operation.
    /// </summary>
    public static (double X, double Y, double Width, double Height) CalculateResize(
        double originalX, double originalY, double originalWidth, double originalHeight,
        HandleType handle, double deltaX, double deltaY,
        bool proportional = false, bool fromCenter = false)
    {
        var x = originalX;
        var y = originalY;
        var width = originalWidth;
        var height = originalHeight;

        // Calculate aspect ratio for proportional resize
        var aspectRatio = originalWidth / originalHeight;

        switch (handle)
        {
            case HandleType.TopLeft:
                x += deltaX;
                y += deltaY;
                width -= deltaX;
                height -= deltaY;
                if (proportional)
                {
                    var size = Math.Max(width, height);
                    width = size;
                    height = size / aspectRatio;
                    x = originalX + originalWidth - width;
                    y = originalY + originalHeight - height;
                }
                break;

            case HandleType.TopRight:
                y += deltaY;
                width += deltaX;
                height -= deltaY;
                if (proportional)
                {
                    var size = Math.Max(width, height);
                    width = size;
                    height = size / aspectRatio;
                    y = originalY + originalHeight - height;
                }
                break;

            case HandleType.BottomLeft:
                x += deltaX;
                width -= deltaX;
                height += deltaY;
                if (proportional)
                {
                    var size = Math.Max(width, height);
                    width = size;
                    height = size / aspectRatio;
                    x = originalX + originalWidth - width;
                }
                break;

            case HandleType.BottomRight:
                width += deltaX;
                height += deltaY;
                if (proportional)
                {
                    var size = Math.Max(width, height);
                    width = size;
                    height = size / aspectRatio;
                }
                break;

            case HandleType.TopCenter:
                y += deltaY;
                height -= deltaY;
                break;

            case HandleType.BottomCenter:
                height += deltaY;
                break;

            case HandleType.LeftCenter:
                x += deltaX;
                width -= deltaX;
                break;

            case HandleType.RightCenter:
                width += deltaX;
                break;
        }

        // Handle center-based resize
        if (fromCenter)
        {
            var centerX = originalX + originalWidth / 2;
            var centerY = originalY + originalHeight / 2;
            
            var newCenterX = x + width / 2;
            var newCenterY = y + height / 2;
            
            var offsetX = centerX - newCenterX;
            var offsetY = centerY - newCenterY;
            
            x += offsetX;
            y += offsetY;
            
            // Double the change for center-based resize
            width += (width - originalWidth);
            height += (height - originalHeight);
            x = centerX - width / 2;
            y = centerY - height / 2;
        }

        // Ensure minimum size
        width = Math.Max(width, 1);
        height = Math.Max(height, 1);

        return (x, y, width, height);
    }

    /// <summary>
    /// Calculates the rotation angle from a point relative to a center.
    /// </summary>
    public static double CalculateRotationAngle(
        double centerX, double centerY,
        double pointX, double pointY)
    {
        var dx = pointX - centerX;
        var dy = pointY - centerY;
        var angle = Math.Atan2(dy, dx) * (180 / Math.PI);
        
        // Adjust so 0 degrees is at the top
        angle += 90;
        
        return angle;
    }

    /// <summary>
    /// Snaps an angle to the nearest increment.
    /// </summary>
    public static double SnapAngle(double angle, double snapIncrement = 15.0)
    {
        return Math.Round(angle / snapIncrement) * snapIncrement;
    }

    /// <summary>
    /// Normalizes an angle to be between 0 and 360 degrees.
    /// </summary>
    public static double NormalizeAngle(double angle)
    {
        angle %= 360;
        if (angle < 0) angle += 360;
        return angle;
    }

    /// <summary>
    /// Calculates the scale factors for a resize operation.
    /// </summary>
    public static (double ScaleX, double ScaleY) CalculateScale(
        double originalWidth, double originalHeight,
        double newWidth, double newHeight)
    {
        var scaleX = originalWidth > 0 ? newWidth / originalWidth : 1;
        var scaleY = originalHeight > 0 ? newHeight / originalHeight : 1;
        return (scaleX, scaleY);
    }

    /// <summary>
    /// Transforms a point around a center point by rotation and scale.
    /// </summary>
    public static (double X, double Y) TransformPoint(
        double x, double y,
        double centerX, double centerY,
        double rotation, double scaleX, double scaleY)
    {
        // Translate to origin
        var dx = x - centerX;
        var dy = y - centerY;

        // Scale
        dx *= scaleX;
        dy *= scaleY;

        // Rotate
        var radians = rotation * Math.PI / 180;
        var cos = Math.Cos(radians);
        var sin = Math.Sin(radians);
        var rx = dx * cos - dy * sin;
        var ry = dx * sin + dy * cos;

        // Translate back
        return (rx + centerX, ry + centerY);
    }
}
