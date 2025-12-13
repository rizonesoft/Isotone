using System.ComponentModel;

namespace Bezier.Core.Models;

/// <summary>
/// Blend modes for compositing elements.
/// </summary>
public enum BlendMode
{
    Normal,
    Multiply,
    Screen,
    Overlay,
    Darken,
    Lighten,
    ColorDodge,
    ColorBurn,
    HardLight,
    SoftLight,
    Difference,
    Exclusion
}

/// <summary>
/// Abstract base class for all vector elements.
/// </summary>
public abstract class VectorElement : INotifyPropertyChanged
{
    private Guid _id = Guid.NewGuid();
    private string _name = string.Empty;
    private bool _isVisible = true;
    private bool _isLocked;
    private double _opacity = 1.0;
    private BlendMode _blendMode = BlendMode.Normal;
    private VectorElement? _parent;

    public event PropertyChangedEventHandler? PropertyChanged;

    /// <summary>
    /// Unique identifier for this element.
    /// </summary>
    public Guid Id
    {
        get => _id;
        set { _id = value; OnPropertyChanged(nameof(Id)); }
    }

    /// <summary>
    /// User-facing name/label for this element.
    /// </summary>
    public string Name
    {
        get => _name;
        set { _name = value; OnPropertyChanged(nameof(Name)); }
    }

    /// <summary>
    /// Whether this element is visible.
    /// </summary>
    public bool IsVisible
    {
        get => _isVisible;
        set { _isVisible = value; OnPropertyChanged(nameof(IsVisible)); }
    }

    /// <summary>
    /// Whether this element is locked (cannot be selected/edited).
    /// </summary>
    public bool IsLocked
    {
        get => _isLocked;
        set { _isLocked = value; OnPropertyChanged(nameof(IsLocked)); }
    }

    /// <summary>
    /// Opacity from 0.0 (transparent) to 1.0 (opaque).
    /// </summary>
    public double Opacity
    {
        get => _opacity;
        set { _opacity = Math.Clamp(value, 0.0, 1.0); OnPropertyChanged(nameof(Opacity)); }
    }

    /// <summary>
    /// Blend mode for compositing.
    /// </summary>
    public BlendMode BlendMode
    {
        get => _blendMode;
        set { _blendMode = value; OnPropertyChanged(nameof(BlendMode)); }
    }

    /// <summary>
    /// Parent element (group) if any.
    /// </summary>
    public VectorElement? Parent
    {
        get => _parent;
        set { _parent = value; OnPropertyChanged(nameof(Parent)); }
    }

    /// <summary>
    /// Creates a deep copy of this element.
    /// </summary>
    public abstract VectorElement Clone();

    /// <summary>
    /// Tests if the given point hits this element.
    /// </summary>
    public abstract bool HitTest(double x, double y);

    /// <summary>
    /// Gets the bounding box of this element.
    /// </summary>
    public abstract (double X, double Y, double Width, double Height) GetBoundingBox();

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
