namespace Pinxit.Core.Layers;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// A layer containing raster (pixel) data.
/// </summary>
public sealed partial class RasterLayer : Layer
{
    [ObservableProperty]
    private int _width;

    [ObservableProperty]
    private int _height;

    public override LayerType LayerType => LayerType.Raster;

    public RasterLayer(int width, int height)
    {
        Width = width;
        Height = height;
        Name = "Layer";
    }

    public RasterLayer(int width, int height, string name)
        : this(width, height)
    {
        Name = name;
    }

    public override Layer Clone()
    {
        var clone = new RasterLayer(Width, Height, Name + " Copy")
        {
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode
        };

        return clone;
    }
}
