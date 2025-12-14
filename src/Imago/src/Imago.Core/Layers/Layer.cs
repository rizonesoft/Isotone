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

    [ObservableProperty]
    private bool _isExpanded = true;

    [ObservableProperty]
    private int _zIndex;

    /// <summary>
    /// Unique identifier for the layer.
    /// </summary>
    public Guid Id { get; } = Guid.NewGuid();

    /// <summary>
    /// When the layer was created.
    /// </summary>
    public DateTime CreatedAt { get; } = DateTime.UtcNow;

    /// <summary>
    /// Parent layer (null if root level).
    /// </summary>
    public Layer? Parent { get; internal set; }

    /// <summary>
    /// Gets the depth in the layer hierarchy (0 = root).
    /// </summary>
    public int Depth
    {
        get
        {
            int depth = 0;
            var current = Parent;
            while (current is not null)
            {
                depth++;
                current = current.Parent;
            }
            return depth;
        }
    }

    /// <summary>
    /// Gets whether this layer is a child of another layer.
    /// </summary>
    public bool HasParent => Parent is not null;

    /// <summary>
    /// Gets the layer type identifier.
    /// </summary>
    public abstract LayerType LayerType { get; }

    /// <summary>
    /// Creates a deep clone of the layer.
    /// </summary>
    public abstract Layer Clone();

    /// <summary>
    /// Gets the effective opacity considering parent opacity.
    /// </summary>
    public double EffectiveOpacity
    {
        get
        {
            double opacity = Opacity;
            var current = Parent;
            while (current is not null)
            {
                opacity *= current.Opacity;
                current = current.Parent;
            }
            return opacity;
        }
    }

    /// <summary>
    /// Gets whether the layer is effectively visible (considering parent visibility).
    /// </summary>
    public bool EffectivelyVisible
    {
        get
        {
            if (!IsVisible) return false;
            var current = Parent;
            while (current is not null)
            {
                if (!current.IsVisible) return false;
                current = current.Parent;
            }
            return true;
        }
    }
}
