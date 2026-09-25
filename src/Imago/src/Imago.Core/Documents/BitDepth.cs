namespace Imago.Core.Documents;

/// <summary>
/// Represents the bit depth per channel of an image.
/// </summary>
public enum BitDepth
{
    /// <summary>
    /// 8 bits per channel (0-255). Standard for web and most displays.
    /// </summary>
    Bpc8 = 8,

    /// <summary>
    /// 16 bits per channel (0-65535). Professional photography and editing.
    /// </summary>
    Bpc16 = 16,

    /// <summary>
    /// 32 bits per channel (floating point). HDR and scientific imaging.
    /// </summary>
    Bpc32 = 32
}

/// <summary>
/// Extension methods for BitDepth.
/// </summary>
public static class BitDepthExtensions
{
    /// <summary>
    /// Gets the number of bits per channel.
    /// </summary>
    public static int ToBitsPerChannel(this BitDepth bitDepth) => (int)bitDepth;

    /// <summary>
    /// Gets the bytes per channel.
    /// </summary>
    public static int ToBytesPerChannel(this BitDepth bitDepth) => bitDepth switch
    {
        BitDepth.Bpc8 => 1,
        BitDepth.Bpc16 => 2,
        BitDepth.Bpc32 => 4,
        _ => 1
    };

    /// <summary>
    /// Gets the maximum value for a channel at this bit depth.
    /// </summary>
    public static double MaxValue(this BitDepth bitDepth) => bitDepth switch
    {
        BitDepth.Bpc8 => 255.0,
        BitDepth.Bpc16 => 65535.0,
        BitDepth.Bpc32 => 1.0, // Normalized float
        _ => 255.0
    };
}
