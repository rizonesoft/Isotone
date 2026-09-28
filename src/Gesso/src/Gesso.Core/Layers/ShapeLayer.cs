namespace Gesso.Core.Layers;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// A layer containing vector shape data.
/// </summary>
public sealed partial class ShapeLayer : Layer
{
    [ObservableProperty]
    private ShapeType _shapeType = ShapeType.Rectangle;

    [ObservableProperty]
    private double _boundsX;

    [ObservableProperty]
    private double _boundsY;

    [ObservableProperty]
    private double _boundsWidth;

    [ObservableProperty]
    private double _boundsHeight;

    [ObservableProperty]
    private uint _fillColor = 0xFFFFFFFF; // ARGB white

    [ObservableProperty]
    private uint _strokeColor = 0xFF000000; // ARGB black

    [ObservableProperty]
    private double _strokeThickness = 1.0;

    [ObservableProperty]
    private double _cornerRadius;

    [ObservableProperty]
    private string? _pathData;

    public override LayerType LayerType => LayerType.Shape;

    public ShapeLayer()
    {
        Name = "Shape";
    }

    public ShapeLayer(ShapeType shapeType) : this()
    {
        ShapeType = shapeType;
        Name = shapeType.ToString();
    }

    public ShapeLayer(ShapeType shapeType, double x, double y, double width, double height) : this(shapeType)
    {
        BoundsX = x;
        BoundsY = y;
        BoundsWidth = width;
        BoundsHeight = height;
    }

    public override Layer Clone()
    {
        return new ShapeLayer(ShapeType, BoundsX, BoundsY, BoundsWidth, BoundsHeight)
        {
            Name = Name + " Copy",
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            FillColor = FillColor,
            StrokeColor = StrokeColor,
            StrokeThickness = StrokeThickness,
            CornerRadius = CornerRadius,
            PathData = PathData
        };
    }
}

/// <summary>
/// Types of vector shapes.
/// </summary>
public enum ShapeType
{
    Rectangle,
    Ellipse,
    Line,
    Polygon,
    Path,
    Star,
    Arrow,
    RoundedRectangle
}
