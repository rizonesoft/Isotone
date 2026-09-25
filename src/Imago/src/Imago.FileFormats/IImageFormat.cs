namespace Imago.FileFormats;

/// <summary>
/// Interface for image format handlers.
/// </summary>
public interface IImageFormat
{
    /// <summary>
    /// Gets the format name (e.g., "PNG", "JPEG").
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets the file extensions supported by this format.
    /// </summary>
    IReadOnlyList<string> Extensions { get; }

    /// <summary>
    /// Gets the MIME type for this format.
    /// </summary>
    string MimeType { get; }

    /// <summary>
    /// Gets whether this format supports reading.
    /// </summary>
    bool CanRead { get; }

    /// <summary>
    /// Gets whether this format supports writing.
    /// </summary>
    bool CanWrite { get; }

    /// <summary>
    /// Gets whether this format supports layers.
    /// </summary>
    bool SupportsLayers { get; }

    /// <summary>
    /// Gets whether this format supports transparency.
    /// </summary>
    bool SupportsTransparency { get; }
}
