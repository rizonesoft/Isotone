namespace Pinxit.Core.Layers;

/// <summary>
/// Defines the types of layers available in Pinxit.
/// </summary>
public enum LayerType
{
    /// <summary>
    /// A raster layer containing pixel data.
    /// </summary>
    Raster,

    /// <summary>
    /// An adjustment layer that applies non-destructive effects.
    /// </summary>
    Adjustment,

    /// <summary>
    /// A group layer containing other layers.
    /// </summary>
    Group,

    /// <summary>
    /// A text layer with editable text content.
    /// </summary>
    Text,

    /// <summary>
    /// A shape layer containing vector shapes.
    /// </summary>
    Shape,

    /// <summary>
    /// A smart object layer referencing external content.
    /// </summary>
    SmartObject
}
