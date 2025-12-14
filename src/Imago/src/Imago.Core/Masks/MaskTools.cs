namespace Imago.Core.Masks;

using System.Runtime.CompilerServices;
using Imago.Core.Selections;

/// <summary>
/// Tools for editing and refining masks.
/// </summary>
public static class MaskTools
{
    /// <summary>
    /// Creates a layer mask from a selection.
    /// </summary>
    public static LayerMask FromSelection(Selection selection)
    {
        ArgumentNullException.ThrowIfNull(selection);

        var mask = new LayerMask(selection.Width, selection.Height, 0);
        selection.GetReadOnlyMaskData().CopyTo(mask.GetRawData());
        return mask;
    }

    /// <summary>
    /// Creates a selection from a layer mask.
    /// </summary>
    public static Selection ToSelection(LayerMask mask)
    {
        ArgumentNullException.ThrowIfNull(mask);

        var selection = new Selection(mask.Width, mask.Height);
        mask.GetReadOnlyRawData().CopyTo(selection.GetMaskData());
        selection.UpdateBounds();
        return selection;
    }

    /// <summary>
    /// Applies levels adjustment to a mask.
    /// </summary>
    public static void ApplyLevels(LayerMask mask, byte inputBlack, byte inputWhite, byte outputBlack, byte outputWhite)
    {
        ArgumentNullException.ThrowIfNull(mask);

        var data = mask.GetRawData();
        float inputRange = Math.Max(1, inputWhite - inputBlack);
        float outputRange = outputWhite - outputBlack;

        for (int i = 0; i < data.Length; i++)
        {
            float normalized = Math.Clamp((data[i] - inputBlack) / inputRange, 0f, 1f);
            data[i] = (byte)(outputBlack + normalized * outputRange);
        }
    }

    /// <summary>
    /// Applies contrast adjustment to a mask.
    /// </summary>
    public static void ApplyContrast(LayerMask mask, float contrast)
    {
        ArgumentNullException.ThrowIfNull(mask);

        var data = mask.GetRawData();
        float factor = (259f * (contrast + 255f)) / (255f * (259f - contrast));

        for (int i = 0; i < data.Length; i++)
        {
            float value = factor * (data[i] - 128f) + 128f;
            data[i] = (byte)Math.Clamp(value, 0f, 255f);
        }
    }

    /// <summary>
    /// Expands or contracts the mask edge.
    /// </summary>
    public static void ExpandContract(LayerMask mask, int pixels)
    {
        ArgumentNullException.ThrowIfNull(mask);

        if (pixels == 0) return;

        var original = mask.Clone();
        try
        {
            var src = original.GetReadOnlyRawData();
            var dst = mask.GetRawData();
            int width = mask.Width;
            int height = mask.Height;
            int radius = Math.Abs(pixels);
            bool expand = pixels > 0;

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    byte result = expand ? (byte)0 : (byte)255;

                    for (int ky = -radius; ky <= radius; ky++)
                    {
                        for (int kx = -radius; kx <= radius; kx++)
                        {
                            int sx = x + kx;
                            int sy = y + ky;

                            if (sx >= 0 && sx < width && sy >= 0 && sy < height)
                            {
                                byte value = src[sy * width + sx];
                                if (expand)
                                    result = Math.Max(result, value);
                                else
                                    result = Math.Min(result, value);
                            }
                        }
                    }

                    dst[y * width + x] = result;
                }
            }
        }
        finally
        {
            original.Dispose();
        }
    }

    /// <summary>
    /// Smooths the mask edges.
    /// </summary>
    public static void Smooth(LayerMask mask, int iterations = 1)
    {
        ArgumentNullException.ThrowIfNull(mask);

        for (int i = 0; i < iterations; i++)
        {
            mask.ApplyFeather(1);
        }
    }

    /// <summary>
    /// Refines mask edges using edge detection.
    /// </summary>
    public static void RefineEdge(LayerMask mask, float radius, float contrast, float shiftEdge)
    {
        ArgumentNullException.ThrowIfNull(mask);

        // Apply feathering
        if (radius > 0)
        {
            mask.ApplyFeather(radius);
        }

        // Apply contrast to sharpen edges
        if (Math.Abs(contrast) > 0.01f)
        {
            ApplyContrast(mask, contrast * 128f);
        }

        // Shift edge in/out
        if (Math.Abs(shiftEdge) > 0.01f)
        {
            int pixels = (int)(shiftEdge * 10);
            ExpandContract(mask, pixels);
        }
    }

    /// <summary>
    /// Detects and enhances edges in the mask.
    /// </summary>
    public static void DetectEdges(LayerMask mask)
    {
        ArgumentNullException.ThrowIfNull(mask);

        var original = mask.Clone();
        try
        {
            var src = original.GetReadOnlyRawData();
            var dst = mask.GetRawData();
            int width = mask.Width;
            int height = mask.Height;

            // Sobel edge detection
            for (int y = 1; y < height - 1; y++)
            {
                for (int x = 1; x < width - 1; x++)
                {
                    int gx = -src[(y - 1) * width + (x - 1)] + src[(y - 1) * width + (x + 1)]
                           - 2 * src[y * width + (x - 1)] + 2 * src[y * width + (x + 1)]
                           - src[(y + 1) * width + (x - 1)] + src[(y + 1) * width + (x + 1)];

                    int gy = -src[(y - 1) * width + (x - 1)] - 2 * src[(y - 1) * width + x] - src[(y - 1) * width + (x + 1)]
                           + src[(y + 1) * width + (x - 1)] + 2 * src[(y + 1) * width + x] + src[(y + 1) * width + (x + 1)];

                    int magnitude = (int)Math.Sqrt(gx * gx + gy * gy);
                    dst[y * width + x] = (byte)Math.Min(255, magnitude);
                }
            }
        }
        finally
        {
            original.Dispose();
        }
    }

    /// <summary>
    /// Applies threshold to convert mask to binary (black/white).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static void ApplyThreshold(LayerMask mask, byte threshold)
    {
        ArgumentNullException.ThrowIfNull(mask);

        var data = mask.GetRawData();
        for (int i = 0; i < data.Length; i++)
        {
            data[i] = data[i] >= threshold ? (byte)255 : (byte)0;
        }
    }
}
