namespace Bezier.Core.Services;

using Bezier.Core.Models;

/// <summary>
/// Horizontal alignment options.
/// </summary>
public enum HorizontalAlignment
{
    Left,
    Center,
    Right
}

/// <summary>
/// Vertical alignment options.
/// </summary>
public enum VerticalAlignment
{
    Top,
    Middle,
    Bottom
}

/// <summary>
/// Reference for alignment operations.
/// </summary>
public enum AlignmentReference
{
    /// <summary>Align to the combined bounds of all selected elements.</summary>
    Selection,
    /// <summary>Align to the canvas/document bounds.</summary>
    Canvas,
    /// <summary>Align to the first selected element (key object).</summary>
    KeyObject
}

/// <summary>
/// Provides alignment and distribution operations for vector elements.
/// </summary>
public static class AlignmentService
{
    /// <summary>
    /// Aligns elements horizontally.
    /// </summary>
    /// <param name="elements">Elements to align.</param>
    /// <param name="alignment">Alignment type.</param>
    /// <param name="reference">Reference for alignment.</param>
    /// <param name="canvasWidth">Canvas width (for Canvas reference).</param>
    /// <returns>Dictionary of element IDs to their X offset changes.</returns>
    public static Dictionary<Guid, double> AlignHorizontal(
        IReadOnlyList<VectorElement> elements,
        HorizontalAlignment alignment,
        AlignmentReference reference = AlignmentReference.Selection,
        double canvasWidth = 0)
    {
        var offsets = new Dictionary<Guid, double>();
        if (elements.Count == 0) return offsets;

        var targetX = GetHorizontalTarget(elements, alignment, reference, canvasWidth);

        foreach (var element in elements)
        {
            var bounds = element.GetBoundingBox();
            double currentX = alignment switch
            {
                HorizontalAlignment.Left => bounds.X,
                HorizontalAlignment.Center => bounds.X + bounds.Width / 2,
                HorizontalAlignment.Right => bounds.X + bounds.Width,
                _ => bounds.X
            };

            var offset = targetX - currentX;
            if (Math.Abs(offset) > 0.001)
            {
                offsets[element.Id] = offset;
            }
        }

        return offsets;
    }

    /// <summary>
    /// Aligns elements vertically.
    /// </summary>
    /// <param name="elements">Elements to align.</param>
    /// <param name="alignment">Alignment type.</param>
    /// <param name="reference">Reference for alignment.</param>
    /// <param name="canvasHeight">Canvas height (for Canvas reference).</param>
    /// <returns>Dictionary of element IDs to their Y offset changes.</returns>
    public static Dictionary<Guid, double> AlignVertical(
        IReadOnlyList<VectorElement> elements,
        VerticalAlignment alignment,
        AlignmentReference reference = AlignmentReference.Selection,
        double canvasHeight = 0)
    {
        var offsets = new Dictionary<Guid, double>();
        if (elements.Count == 0) return offsets;

        var targetY = GetVerticalTarget(elements, alignment, reference, canvasHeight);

        foreach (var element in elements)
        {
            var bounds = element.GetBoundingBox();
            double currentY = alignment switch
            {
                VerticalAlignment.Top => bounds.Y,
                VerticalAlignment.Middle => bounds.Y + bounds.Height / 2,
                VerticalAlignment.Bottom => bounds.Y + bounds.Height,
                _ => bounds.Y
            };

            var offset = targetY - currentY;
            if (Math.Abs(offset) > 0.001)
            {
                offsets[element.Id] = offset;
            }
        }

        return offsets;
    }

    /// <summary>
    /// Distributes elements horizontally with equal spacing.
    /// </summary>
    /// <param name="elements">Elements to distribute (minimum 3).</param>
    /// <returns>Dictionary of element IDs to their X offset changes.</returns>
    public static Dictionary<Guid, double> DistributeHorizontal(IReadOnlyList<VectorElement> elements)
    {
        var offsets = new Dictionary<Guid, double>();
        if (elements.Count < 3) return offsets;

        // Sort by center X position
        var sorted = elements
            .Select(e => (Element: e, Bounds: e.GetBoundingBox()))
            .OrderBy(x => x.Bounds.X + x.Bounds.Width / 2)
            .ToList();

        var first = sorted[0];
        var last = sorted[^1];

        var firstCenter = first.Bounds.X + first.Bounds.Width / 2;
        var lastCenter = last.Bounds.X + last.Bounds.Width / 2;
        var totalSpan = lastCenter - firstCenter;
        var spacing = totalSpan / (elements.Count - 1);

        for (var i = 1; i < sorted.Count - 1; i++)
        {
            var (element, bounds) = sorted[i];
            var currentCenter = bounds.X + bounds.Width / 2;
            var targetCenter = firstCenter + spacing * i;
            var offset = targetCenter - currentCenter;

            if (Math.Abs(offset) > 0.001)
            {
                offsets[element.Id] = offset;
            }
        }

        return offsets;
    }

    /// <summary>
    /// Distributes elements vertically with equal spacing.
    /// </summary>
    /// <param name="elements">Elements to distribute (minimum 3).</param>
    /// <returns>Dictionary of element IDs to their Y offset changes.</returns>
    public static Dictionary<Guid, double> DistributeVertical(IReadOnlyList<VectorElement> elements)
    {
        var offsets = new Dictionary<Guid, double>();
        if (elements.Count < 3) return offsets;

        // Sort by center Y position
        var sorted = elements
            .Select(e => (Element: e, Bounds: e.GetBoundingBox()))
            .OrderBy(x => x.Bounds.Y + x.Bounds.Height / 2)
            .ToList();

        var first = sorted[0];
        var last = sorted[^1];

        var firstCenter = first.Bounds.Y + first.Bounds.Height / 2;
        var lastCenter = last.Bounds.Y + last.Bounds.Height / 2;
        var totalSpan = lastCenter - firstCenter;
        var spacing = totalSpan / (elements.Count - 1);

        for (var i = 1; i < sorted.Count - 1; i++)
        {
            var (element, bounds) = sorted[i];
            var currentCenter = bounds.Y + bounds.Height / 2;
            var targetCenter = firstCenter + spacing * i;
            var offset = targetCenter - currentCenter;

            if (Math.Abs(offset) > 0.001)
            {
                offsets[element.Id] = offset;
            }
        }

        return offsets;
    }

    /// <summary>
    /// Distributes elements horizontally with equal gaps between them.
    /// </summary>
    public static Dictionary<Guid, double> DistributeHorizontalGaps(IReadOnlyList<VectorElement> elements)
    {
        var offsets = new Dictionary<Guid, double>();
        if (elements.Count < 3) return offsets;

        // Sort by left edge
        var sorted = elements
            .Select(e => (Element: e, Bounds: e.GetBoundingBox()))
            .OrderBy(x => x.Bounds.X)
            .ToList();

        var first = sorted[0];
        var last = sorted[^1];

        // Calculate total width of all elements
        var totalElementWidth = sorted.Sum(x => x.Bounds.Width);
        
        // Calculate total span from left of first to right of last
        var totalSpan = (last.Bounds.X + last.Bounds.Width) - first.Bounds.X;
        
        // Calculate gap between elements
        var totalGap = totalSpan - totalElementWidth;
        var gapSize = totalGap / (elements.Count - 1);

        var currentX = first.Bounds.X + first.Bounds.Width + gapSize;

        for (var i = 1; i < sorted.Count - 1; i++)
        {
            var (element, bounds) = sorted[i];
            var offset = currentX - bounds.X;

            if (Math.Abs(offset) > 0.001)
            {
                offsets[element.Id] = offset;
            }

            currentX += bounds.Width + gapSize;
        }

        return offsets;
    }

    /// <summary>
    /// Distributes elements vertically with equal gaps between them.
    /// </summary>
    public static Dictionary<Guid, double> DistributeVerticalGaps(IReadOnlyList<VectorElement> elements)
    {
        var offsets = new Dictionary<Guid, double>();
        if (elements.Count < 3) return offsets;

        // Sort by top edge
        var sorted = elements
            .Select(e => (Element: e, Bounds: e.GetBoundingBox()))
            .OrderBy(x => x.Bounds.Y)
            .ToList();

        var first = sorted[0];
        var last = sorted[^1];

        // Calculate total height of all elements
        var totalElementHeight = sorted.Sum(x => x.Bounds.Height);
        
        // Calculate total span from top of first to bottom of last
        var totalSpan = (last.Bounds.Y + last.Bounds.Height) - first.Bounds.Y;
        
        // Calculate gap between elements
        var totalGap = totalSpan - totalElementHeight;
        var gapSize = totalGap / (elements.Count - 1);

        var currentY = first.Bounds.Y + first.Bounds.Height + gapSize;

        for (var i = 1; i < sorted.Count - 1; i++)
        {
            var (element, bounds) = sorted[i];
            var offset = currentY - bounds.Y;

            if (Math.Abs(offset) > 0.001)
            {
                offsets[element.Id] = offset;
            }

            currentY += bounds.Height + gapSize;
        }

        return offsets;
    }

    /// <summary>
    /// Gets the combined bounding box of multiple elements.
    /// </summary>
    public static (double X, double Y, double Width, double Height) GetCombinedBounds(
        IReadOnlyList<VectorElement> elements)
    {
        if (elements.Count == 0)
            return (0, 0, 0, 0);

        var first = elements[0].GetBoundingBox();
        var minX = first.X;
        var minY = first.Y;
        var maxX = first.X + first.Width;
        var maxY = first.Y + first.Height;

        for (var i = 1; i < elements.Count; i++)
        {
            var bounds = elements[i].GetBoundingBox();
            minX = Math.Min(minX, bounds.X);
            minY = Math.Min(minY, bounds.Y);
            maxX = Math.Max(maxX, bounds.X + bounds.Width);
            maxY = Math.Max(maxY, bounds.Y + bounds.Height);
        }

        return (minX, minY, maxX - minX, maxY - minY);
    }

    private static double GetHorizontalTarget(
        IReadOnlyList<VectorElement> elements,
        HorizontalAlignment alignment,
        AlignmentReference reference,
        double canvasWidth)
    {
        if (reference == AlignmentReference.Canvas)
        {
            return alignment switch
            {
                HorizontalAlignment.Left => 0,
                HorizontalAlignment.Center => canvasWidth / 2,
                HorizontalAlignment.Right => canvasWidth,
                _ => 0
            };
        }

        if (reference == AlignmentReference.KeyObject && elements.Count > 0)
        {
            var keyBounds = elements[0].GetBoundingBox();
            return alignment switch
            {
                HorizontalAlignment.Left => keyBounds.X,
                HorizontalAlignment.Center => keyBounds.X + keyBounds.Width / 2,
                HorizontalAlignment.Right => keyBounds.X + keyBounds.Width,
                _ => keyBounds.X
            };
        }

        // Selection bounds
        var combined = GetCombinedBounds(elements);
        return alignment switch
        {
            HorizontalAlignment.Left => combined.X,
            HorizontalAlignment.Center => combined.X + combined.Width / 2,
            HorizontalAlignment.Right => combined.X + combined.Width,
            _ => combined.X
        };
    }

    private static double GetVerticalTarget(
        IReadOnlyList<VectorElement> elements,
        VerticalAlignment alignment,
        AlignmentReference reference,
        double canvasHeight)
    {
        if (reference == AlignmentReference.Canvas)
        {
            return alignment switch
            {
                VerticalAlignment.Top => 0,
                VerticalAlignment.Middle => canvasHeight / 2,
                VerticalAlignment.Bottom => canvasHeight,
                _ => 0
            };
        }

        if (reference == AlignmentReference.KeyObject && elements.Count > 0)
        {
            var keyBounds = elements[0].GetBoundingBox();
            return alignment switch
            {
                VerticalAlignment.Top => keyBounds.Y,
                VerticalAlignment.Middle => keyBounds.Y + keyBounds.Height / 2,
                VerticalAlignment.Bottom => keyBounds.Y + keyBounds.Height,
                _ => keyBounds.Y
            };
        }

        // Selection bounds
        var combined = GetCombinedBounds(elements);
        return alignment switch
        {
            VerticalAlignment.Top => combined.Y,
            VerticalAlignment.Middle => combined.Y + combined.Height / 2,
            VerticalAlignment.Bottom => combined.Y + combined.Height,
            _ => combined.Y
        };
    }

    /// <summary>
    /// Applies horizontal offsets to elements.
    /// </summary>
    public static void ApplyHorizontalOffsets(
        IReadOnlyList<VectorElement> elements,
        Dictionary<Guid, double> offsets)
    {
        foreach (var element in elements)
        {
            if (offsets.TryGetValue(element.Id, out var offset))
            {
                element.Transform = element.Transform with
                {
                    TranslateX = element.Transform.TranslateX + offset
                };
            }
        }
    }

    /// <summary>
    /// Applies vertical offsets to elements.
    /// </summary>
    public static void ApplyVerticalOffsets(
        IReadOnlyList<VectorElement> elements,
        Dictionary<Guid, double> offsets)
    {
        foreach (var element in elements)
        {
            if (offsets.TryGetValue(element.Id, out var offset))
            {
                element.Transform = element.Transform with
                {
                    TranslateY = element.Transform.TranslateY + offset
                };
            }
        }
    }
}
