namespace Pinxit.Core.Layers;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// A layer that references external content (linked or embedded).
/// Smart objects preserve source data and allow non-destructive transformations.
/// </summary>
public sealed partial class SmartObjectLayer : Layer
{
    [ObservableProperty]
    private string? _sourcePath;

    [ObservableProperty]
    private SmartObjectType _smartObjectType = SmartObjectType.Embedded;

    [ObservableProperty]
    private int _sourceWidth;

    [ObservableProperty]
    private int _sourceHeight;

    [ObservableProperty]
    private double _scaleX = 1.0;

    [ObservableProperty]
    private double _scaleY = 1.0;

    [ObservableProperty]
    private double _rotation;

    [ObservableProperty]
    private bool _isOutOfDate;

    [ObservableProperty]
    private DateTime _lastSyncTime;

    public override LayerType LayerType => LayerType.SmartObject;

    /// <summary>
    /// Gets the display width after applying scale.
    /// </summary>
    public int DisplayWidth => (int)(SourceWidth * ScaleX);

    /// <summary>
    /// Gets the display height after applying scale.
    /// </summary>
    public int DisplayHeight => (int)(SourceHeight * ScaleY);

    public SmartObjectLayer()
    {
        Name = "Smart Object";
        LastSyncTime = DateTime.UtcNow;
    }

    public SmartObjectLayer(string sourcePath, int width, int height) : this()
    {
        SourcePath = sourcePath;
        SourceWidth = width;
        SourceHeight = height;
        Name = System.IO.Path.GetFileName(sourcePath) ?? "Smart Object";
    }

    /// <summary>
    /// Marks the smart object as needing to be re-synced with source.
    /// </summary>
    public void MarkOutOfDate()
    {
        IsOutOfDate = true;
    }

    /// <summary>
    /// Marks the smart object as synced with source.
    /// </summary>
    public void MarkSynced()
    {
        IsOutOfDate = false;
        LastSyncTime = DateTime.UtcNow;
    }

    public override Layer Clone()
    {
        return new SmartObjectLayer
        {
            Name = Name + " Copy",
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            SourcePath = SourcePath,
            SmartObjectType = SmartObjectType,
            SourceWidth = SourceWidth,
            SourceHeight = SourceHeight,
            ScaleX = ScaleX,
            ScaleY = ScaleY,
            Rotation = Rotation,
            IsOutOfDate = IsOutOfDate,
            LastSyncTime = LastSyncTime
        };
    }
}

/// <summary>
/// Types of smart object embedding.
/// </summary>
public enum SmartObjectType
{
    /// <summary>
    /// Content is embedded within the document.
    /// </summary>
    Embedded,

    /// <summary>
    /// Content is linked to an external file.
    /// </summary>
    Linked
}
