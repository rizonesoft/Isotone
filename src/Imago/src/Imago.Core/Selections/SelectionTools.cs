namespace Imago.Core.Selections;

using System.Runtime.CompilerServices;

/// <summary>
/// Provides tools for creating selections of various shapes.
/// </summary>
public static class SelectionTools
{
    /// <summary>
    /// Creates a rectangular selection.
    /// </summary>
    public static void SelectRectangle(Selection selection, int x, int y, int width, int height, byte value = 255)
    {
        ArgumentNullException.ThrowIfNull(selection);

        int x1 = Math.Max(0, x);
        int y1 = Math.Max(0, y);
        int x2 = Math.Min(selection.Width, x + width);
        int y2 = Math.Min(selection.Height, y + height);

        var mask = selection.GetMaskData();
        int stride = selection.Width;

        for (int py = y1; py < y2; py++)
        {
            var row = mask.Slice(py * stride + x1, x2 - x1);
            row.Fill(value);
        }

        selection.UpdateBounds();
    }

    /// <summary>
    /// Creates an elliptical selection with anti-aliasing.
    /// </summary>
    public static void SelectEllipse(Selection selection, int centerX, int centerY, int radiusX, int radiusY, bool antiAlias = true)
    {
        ArgumentNullException.ThrowIfNull(selection);

        int x1 = Math.Max(0, centerX - radiusX - 1);
        int y1 = Math.Max(0, centerY - radiusY - 1);
        int x2 = Math.Min(selection.Width, centerX + radiusX + 2);
        int y2 = Math.Min(selection.Height, centerY + radiusY + 2);

        var mask = selection.GetMaskData();
        int stride = selection.Width;

        float rxSq = radiusX * radiusX;
        float rySq = radiusY * radiusY;

        for (int py = y1; py < y2; py++)
        {
            float dy = py - centerY;
            float dySq = dy * dy;

            for (int px = x1; px < x2; px++)
            {
                float dx = px - centerX;
                float dist = (dx * dx / rxSq) + (dySq / rySq);

                byte value;
                if (dist <= 1.0f)
                {
                    value = 255;
                }
                else if (antiAlias && dist < 1.5f)
                {
                    // Anti-alias edge
                    value = (byte)(255 * (1.5f - dist) * 2f);
                }
                else
                {
                    continue;
                }

                mask[py * stride + px] = value;
            }
        }

        selection.UpdateBounds();
    }

    /// <summary>
    /// Creates a selection from a polygon (lasso/freehand).
    /// </summary>
    public static void SelectPolygon(Selection selection, ReadOnlySpan<(int X, int Y)> points, bool antiAlias = true)
    {
        ArgumentNullException.ThrowIfNull(selection);

        if (points.Length < 3) return;

        // Find bounding box
        int minX = int.MaxValue, minY = int.MaxValue;
        int maxX = int.MinValue, maxY = int.MinValue;

        foreach (var p in points)
        {
            minX = Math.Min(minX, p.X);
            minY = Math.Min(minY, p.Y);
            maxX = Math.Max(maxX, p.X);
            maxY = Math.Max(maxY, p.Y);
        }

        minX = Math.Max(0, minX);
        minY = Math.Max(0, minY);
        maxX = Math.Min(selection.Width - 1, maxX);
        maxY = Math.Min(selection.Height - 1, maxY);

        var mask = selection.GetMaskData();
        int stride = selection.Width;

        // Scanline fill algorithm
        for (int y = minY; y <= maxY; y++)
        {
            for (int x = minX; x <= maxX; x++)
            {
                if (IsPointInPolygon(x, y, points))
                {
                    mask[y * stride + x] = 255;
                }
                else if (antiAlias)
                {
                    // Check for edge proximity for anti-aliasing
                    float minDist = GetMinDistanceToPolygonEdge(x, y, points);
                    if (minDist < 1.5f)
                    {
                        byte existing = mask[y * stride + x];
                        byte edgeValue = (byte)(255 * Math.Max(0, 1f - minDist));
                        mask[y * stride + x] = Math.Max(existing, edgeValue);
                    }
                }
            }
        }

        selection.UpdateBounds();
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private static bool IsPointInPolygon(int x, int y, ReadOnlySpan<(int X, int Y)> points)
    {
        bool inside = false;
        int j = points.Length - 1;

        for (int i = 0; i < points.Length; i++)
        {
            if ((points[i].Y > y) != (points[j].Y > y) &&
                x < (points[j].X - points[i].X) * (y - points[i].Y) / (points[j].Y - points[i].Y) + points[i].X)
            {
                inside = !inside;
            }
            j = i;
        }

        return inside;
    }

    private static float GetMinDistanceToPolygonEdge(int x, int y, ReadOnlySpan<(int X, int Y)> points)
    {
        float minDist = float.MaxValue;
        int j = points.Length - 1;

        for (int i = 0; i < points.Length; i++)
        {
            float dist = PointToSegmentDistance(x, y, points[i].X, points[i].Y, points[j].X, points[j].Y);
            minDist = Math.Min(minDist, dist);
            j = i;
        }

        return minDist;
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private static float PointToSegmentDistance(float px, float py, float x1, float y1, float x2, float y2)
    {
        float dx = x2 - x1;
        float dy = y2 - y1;
        float lengthSq = dx * dx + dy * dy;

        if (lengthSq < 0.0001f)
            return MathF.Sqrt((px - x1) * (px - x1) + (py - y1) * (py - y1));

        float t = Math.Clamp(((px - x1) * dx + (py - y1) * dy) / lengthSq, 0f, 1f);
        float projX = x1 + t * dx;
        float projY = y1 + t * dy;

        return MathF.Sqrt((px - projX) * (px - projX) + (py - projY) * (py - projY));
    }

    /// <summary>
    /// Creates a magic wand selection based on color similarity.
    /// </summary>
    public static void SelectByColor(
        Selection selection,
        ReadOnlySpan<byte> imageData,
        int imageWidth,
        int startX,
        int startY,
        int tolerance,
        bool contiguous = true)
    {
        ArgumentNullException.ThrowIfNull(selection);

        if (startX < 0 || startX >= imageWidth || startY < 0)
            return;

        int imageHeight = imageData.Length / (imageWidth * 4);
        if (startY >= imageHeight) return;

        int startIndex = (startY * imageWidth + startX) * 4;
        byte targetR = imageData[startIndex];
        byte targetG = imageData[startIndex + 1];
        byte targetB = imageData[startIndex + 2];

        var mask = selection.GetMaskData();

        if (contiguous)
        {
            // Flood fill from start point
            FloodFillSelect(mask, imageData, imageWidth, imageHeight, startX, startY, targetR, targetG, targetB, tolerance);
        }
        else
        {
            // Select all matching pixels
            for (int y = 0; y < imageHeight; y++)
            {
                for (int x = 0; x < imageWidth; x++)
                {
                    int idx = (y * imageWidth + x) * 4;
                    if (ColorMatches(imageData[idx], imageData[idx + 1], imageData[idx + 2], targetR, targetG, targetB, tolerance))
                    {
                        mask[y * imageWidth + x] = 255;
                    }
                }
            }
        }

        selection.UpdateBounds();
    }

    private static void FloodFillSelect(
        Span<byte> mask,
        ReadOnlySpan<byte> imageData,
        int width,
        int height,
        int startX,
        int startY,
        byte targetR,
        byte targetG,
        byte targetB,
        int tolerance)
    {
        var stack = new Stack<(int X, int Y)>();
        stack.Push((startX, startY));

        while (stack.Count > 0)
        {
            var (x, y) = stack.Pop();

            if (x < 0 || x >= width || y < 0 || y >= height)
                continue;

            int maskIdx = y * width + x;
            if (mask[maskIdx] == 255)
                continue;

            int imgIdx = maskIdx * 4;
            if (!ColorMatches(imageData[imgIdx], imageData[imgIdx + 1], imageData[imgIdx + 2], targetR, targetG, targetB, tolerance))
                continue;

            mask[maskIdx] = 255;

            stack.Push((x + 1, y));
            stack.Push((x - 1, y));
            stack.Push((x, y + 1));
            stack.Push((x, y - 1));
        }
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private static bool ColorMatches(byte r, byte g, byte b, byte targetR, byte targetG, byte targetB, int tolerance)
    {
        int dr = r - targetR;
        int dg = g - targetG;
        int db = b - targetB;
        return (dr * dr + dg * dg + db * db) <= tolerance * tolerance * 3;
    }

    /// <summary>
    /// Selects pixels by color range.
    /// </summary>
    public static void SelectByColorRange(
        Selection selection,
        ReadOnlySpan<byte> imageData,
        int imageWidth,
        byte minR, byte maxR,
        byte minG, byte maxG,
        byte minB, byte maxB,
        byte minA = 0, byte maxA = 255)
    {
        ArgumentNullException.ThrowIfNull(selection);

        int imageHeight = imageData.Length / (imageWidth * 4);
        var mask = selection.GetMaskData();

        for (int y = 0; y < imageHeight; y++)
        {
            for (int x = 0; x < imageWidth; x++)
            {
                int idx = (y * imageWidth + x) * 4;
                byte r = imageData[idx];
                byte g = imageData[idx + 1];
                byte b = imageData[idx + 2];
                byte a = imageData[idx + 3];

                if (r >= minR && r <= maxR &&
                    g >= minG && g <= maxG &&
                    b >= minB && b <= maxB &&
                    a >= minA && a <= maxA)
                {
                    mask[y * imageWidth + x] = 255;
                }
            }
        }

        selection.UpdateBounds();
    }
}
