namespace Pinxit.Core.Masks;

using Pinxit.Core.Layers;

/// <summary>
/// Provides clipping mask behavior where a layer clips to the content of the layer below.
/// </summary>
public static class ClippingMask
{
    /// <summary>
    /// Gets the effective opacity at a pixel considering the clipping base layer.
    /// </summary>
    public static byte GetClippedOpacity(Layer clippedLayer, Layer baseLayer, int x, int y, Func<Layer, int, int, byte> getLayerAlpha)
    {
        ArgumentNullException.ThrowIfNull(clippedLayer);
        ArgumentNullException.ThrowIfNull(baseLayer);

        // Get base layer's alpha at this pixel
        byte baseAlpha = getLayerAlpha(baseLayer, x, y);
        if (baseAlpha == 0)
            return 0;

        // Get clipped layer's alpha
        byte clippedAlpha = getLayerAlpha(clippedLayer, x, y);

        // Multiply alphas
        return (byte)((clippedAlpha * baseAlpha) / 255);
    }

    /// <summary>
    /// Applies clipping mask to a layer's opacity map.
    /// </summary>
    public static void ApplyClipping(
        Span<byte> clippedAlpha,
        ReadOnlySpan<byte> baseAlpha,
        int width,
        int height)
    {
        if (clippedAlpha.Length != baseAlpha.Length)
            throw new ArgumentException("Alpha buffers must have same size");

        for (int i = 0; i < clippedAlpha.Length; i++)
        {
            clippedAlpha[i] = (byte)((clippedAlpha[i] * baseAlpha[i]) / 255);
        }
    }

    /// <summary>
    /// Builds the effective mask for a layer considering all masks.
    /// </summary>
    public static void BuildEffectiveMask(
        Span<byte> result,
        int width,
        int height,
        LayerMask? layerMask,
        VectorMask? vectorMask,
        ReadOnlySpan<byte> clippingBase)
    {
        // Start with full opacity
        result.Fill(255);

        // Apply layer mask
        if (layerMask?.IsEnabled == true)
        {
            var maskData = layerMask.GetReadOnlyRawData();
            for (int i = 0; i < result.Length; i++)
            {
                byte maskValue = maskData[i];
                if (layerMask.IsInverted)
                    maskValue = (byte)(255 - maskValue);
                if (layerMask.Density < 1.0f)
                    maskValue = (byte)(maskValue * layerMask.Density);

                result[i] = (byte)((result[i] * maskValue) / 255);
            }
        }

        // Apply vector mask (rasterize first)
        if (vectorMask?.IsEnabled == true)
        {
            using var rasterized = vectorMask.Rasterize(width, height);
            var maskData = rasterized.GetReadOnlyRawData();
            for (int i = 0; i < result.Length; i++)
            {
                result[i] = (byte)((result[i] * maskData[i]) / 255);
            }
        }

        // Apply clipping mask
        if (!clippingBase.IsEmpty)
        {
            for (int i = 0; i < result.Length; i++)
            {
                result[i] = (byte)((result[i] * clippingBase[i]) / 255);
            }
        }
    }
}
