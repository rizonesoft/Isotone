using System.ComponentModel;
using Bezier.Core.Interfaces;

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
    private Transform _transform = Transform.Identity;
    private IFill? _fill;
    private Stroke? _stroke;

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
    /// Transformation matrix for this element.
    /// </summary>
    public Transform Transform
    {
        get => _transform;
        set { _transform = value; OnPropertyChanged(nameof(Transform)); }
    }

    /// <summary>
    /// Fill for this element (color, gradient, pattern, or null for no fill).
    /// </summary>
    public IFill? Fill
    {
        get => _fill;
        set { _fill = value; OnPropertyChanged(nameof(Fill)); }
    }

    /// <summary>
    /// Stroke for this element (null for no stroke).
    /// </summary>
    public Stroke? Stroke
    {
        get => _stroke;
        set { _stroke = value; OnPropertyChanged(nameof(Stroke)); }
    }

    /// <summary>
    /// Creates a deep copy of this element.
    /// </summary>
    public abstract VectorElement Clone();

    /// <summary>
    /// Tests if the given point hits this element (in world coordinates).
    /// </summary>
    public virtual bool HitTest(double x, double y)
    {
        // Transform the point to local coordinates and test against local bounds
        if (Transform.IsIdentity)
            return HitTestLocal(x, y);
        
        var localPoint = Transform.Invert().TransformPoint(x, y);
        return HitTestLocal(localPoint.X, localPoint.Y);
    }

    /// <summary>
    /// Tests if the given point (in local coordinates) hits this element.
    /// Override this in derived classes for shape-specific hit testing.
    /// </summary>
    protected abstract bool HitTestLocal(double x, double y);

    /// <summary>
    /// Gets the bounding box of this element in world coordinates (with transform applied).
    /// </summary>
    public virtual (double X, double Y, double Width, double Height) GetBoundingBox()
    {
        var localBounds = GetLocalBoundingBox();
        
        if (Transform.IsIdentity)
            return localBounds;

        // Transform all four corners and find the axis-aligned bounding box
        var corners = new[]
        {
            Transform.TransformPoint(localBounds.X, localBounds.Y),
            Transform.TransformPoint(localBounds.X + localBounds.Width, localBounds.Y),
            Transform.TransformPoint(localBounds.X, localBounds.Y + localBounds.Height),
            Transform.TransformPoint(localBounds.X + localBounds.Width, localBounds.Y + localBounds.Height)
        };

        var minX = corners.Min(c => c.X);
        var minY = corners.Min(c => c.Y);
        var maxX = corners.Max(c => c.X);
        var maxY = corners.Max(c => c.Y);

        return (minX, minY, maxX - minX, maxY - minY);
    }

    /// <summary>
    /// Gets the bounding box in local coordinates (without transform).
    /// Override this in derived classes.
    /// </summary>
    protected abstract (double X, double Y, double Width, double Height) GetLocalBoundingBox();

    /// <summary>
    /// Converts this element to an SVG string representation.
    /// </summary>
    public abstract string ToSvgString();

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets common SVG attributes (id, opacity, transform, etc.) as a string.
    /// </summary>
    protected string GetCommonSvgAttributes()
    {
        var attrs = new List<string>();

        if (!string.IsNullOrEmpty(Name))
            attrs.Add($"id=\"{Name}\"");

        if (Opacity < 1.0)
            attrs.Add($"opacity=\"{Opacity:G6}\"");

        if (!Transform.IsIdentity)
            attrs.Add($"transform=\"{Transform.ToSvgString()}\"");

        return attrs.Count > 0 ? " " + string.Join(" ", attrs) : string.Empty;
    }
}

