namespace Pinxit.Core.Layers;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// A layer that applies non-destructive adjustments to layers below.
/// </summary>
public sealed partial class AdjustmentLayer : Layer
{
    [ObservableProperty]
    private AdjustmentType _adjustmentType;

    public override LayerType LayerType => LayerType.Adjustment;

    public AdjustmentLayer(AdjustmentType adjustmentType)
    {
        AdjustmentType = adjustmentType;
        Name = adjustmentType.ToString();
    }

    public override Layer Clone()
    {
        var clone = new AdjustmentLayer(AdjustmentType)
        {
            Name = Name + " Copy",
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode
        };

        return clone;
    }
}

/// <summary>
/// Types of adjustment layers available.
/// </summary>
public enum AdjustmentType
{
    BrightnessContrast,
    Levels,
    Curves,
    Exposure,
    Vibrance,
    HueSaturation,
    ColorBalance,
    BlackAndWhite,
    PhotoFilter,
    ChannelMixer,
    ColorLookup,
    Invert,
    Posterize,
    Threshold,
    GradientMap,
    SelectiveColor
}
