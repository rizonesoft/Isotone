namespace Gesso.Core.Documents;

/// <summary>
/// Represents the color space of a document.
/// </summary>
public enum ColorSpace
{
    /// <summary>
    /// Standard RGB color space.
    /// </summary>
    SRGB,

    /// <summary>
    /// Adobe RGB color space with wider gamut.
    /// </summary>
    AdobeRGB,

    /// <summary>
    /// ProPhoto RGB color space for professional photography.
    /// </summary>
    ProPhotoRGB,

    /// <summary>
    /// CMYK color space for print workflows.
    /// </summary>
    CMYK,

    /// <summary>
    /// CIE LAB color space.
    /// </summary>
    LAB,

    /// <summary>
    /// Grayscale color space.
    /// </summary>
    Grayscale
}
