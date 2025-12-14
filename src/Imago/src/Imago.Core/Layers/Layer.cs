namespace Imago.Core.Layers;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Base class for all layer types in Imago.
/// </summary>
public abstract partial class Layer : ObservableObject
{
    [ObservableProperty]
    private string _name = "Layer";

    [ObservableProperty]
    private bool _isVisible = true;

    [ObservableProperty]
    private bool _isLocked;

    [ObservableProperty]
    private double _opacity = 1.0;

    [ObservableProperty]
    private BlendMode _blendMode = BlendMode.Normal;

    [ObservableProperty]
    private bool _isSelected;

    public Guid Id { get; } = Guid.NewGuid();

    public DateTime CreatedAt { get; } = DateTime.UtcNow;

    /// <summary>
    /// Gets the layer type identifier.
    /// </summary>
    public abstract LayerType LayerType { get; }

    /// <summary>
    /// Creates a deep clone of the layer.
    /// </summary>
    public abstract Layer Clone();
}
