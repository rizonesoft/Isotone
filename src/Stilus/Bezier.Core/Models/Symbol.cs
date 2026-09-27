using System.Collections.ObjectModel;
using System.ComponentModel;

namespace Bezier.Core.Models;

/// <summary>
/// Represents a reusable symbol definition.
/// </summary>
public class Symbol : INotifyPropertyChanged
{
    private string _name = "Symbol";
    private string _category = "Uncategorized";
    private DateTime _createdAt = DateTime.UtcNow;
    private DateTime _modifiedAt = DateTime.UtcNow;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets the unique identifier for this symbol.
    /// </summary>
    public Guid Id { get; init; } = Guid.NewGuid();

    /// <summary>
    /// Gets or sets the symbol name.
    /// </summary>
    public string Name
    {
        get => _name;
        set { _name = value; OnPropertyChanged(nameof(Name)); }
    }

    /// <summary>
    /// Gets or sets the category for organization.
    /// </summary>
    public string Category
    {
        get => _category;
        set { _category = value; OnPropertyChanged(nameof(Category)); }
    }

    /// <summary>
    /// Gets or sets when this symbol was created.
    /// </summary>
    public DateTime CreatedAt
    {
        get => _createdAt;
        set { _createdAt = value; OnPropertyChanged(nameof(CreatedAt)); }
    }

    /// <summary>
    /// Gets or sets when this symbol was last modified.
    /// </summary>
    public DateTime ModifiedAt
    {
        get => _modifiedAt;
        set { _modifiedAt = value; OnPropertyChanged(nameof(ModifiedAt)); }
    }

    /// <summary>
    /// Gets or sets the symbol's view box (for scaling).
    /// </summary>
    public (double X, double Y, double Width, double Height) ViewBox { get; set; } = (0, 0, 100, 100);

    /// <summary>
    /// Gets the elements that make up this symbol.
    /// </summary>
    public ObservableCollection<VectorElement> Elements { get; } = [];

    /// <summary>
    /// Gets or sets optional description/tags.
    /// </summary>
    public string? Description { get; set; }

    /// <summary>
    /// Gets or sets the thumbnail data (base64 encoded PNG).
    /// </summary>
    public string? ThumbnailData { get; set; }

    /// <summary>
    /// Gets the bounding box of the symbol content.
    /// </summary>
    public (double X, double Y, double Width, double Height) GetBounds()
    {
        if (Elements.Count == 0)
            return ViewBox;

        var first = Elements[0].GetBoundingBox();
        var minX = first.X;
        var minY = first.Y;
        var maxX = first.X + first.Width;
        var maxY = first.Y + first.Height;

        for (var i = 1; i < Elements.Count; i++)
        {
            var bounds = Elements[i].GetBoundingBox();
            minX = Math.Min(minX, bounds.X);
            minY = Math.Min(minY, bounds.Y);
            maxX = Math.Max(maxX, bounds.X + bounds.Width);
            maxY = Math.Max(maxY, bounds.Y + bounds.Height);
        }

        return (minX, minY, maxX - minX, maxY - minY);
    }

    /// <summary>
    /// Creates a deep clone of this symbol.
    /// </summary>
    public Symbol Clone()
    {
        var clone = new Symbol
        {
            Name = Name + " Copy",
            Category = Category,
            ViewBox = ViewBox,
            Description = Description,
            ThumbnailData = ThumbnailData
        };

        foreach (var element in Elements)
        {
            clone.Elements.Add(element.Clone());
        }

        return clone;
    }

    /// <summary>
    /// Marks the symbol as modified.
    /// </summary>
    public void MarkModified()
    {
        ModifiedAt = DateTime.UtcNow;
        OnPropertyChanged(nameof(ModifiedAt));
    }
}

/// <summary>
/// Represents an instance of a symbol placed on the canvas.
/// </summary>
public class SymbolInstance : VectorElement
{
    private Guid _symbolId;
    private double _width = 100;
    private double _height = 100;
    private bool _maintainAspectRatio = true;

    /// <summary>
    /// Gets or sets the ID of the master symbol.
    /// </summary>
    public Guid SymbolId
    {
        get => _symbolId;
        set { _symbolId = value; OnPropertyChanged(nameof(SymbolId)); }
    }

    /// <summary>
    /// Gets or sets the X position.
    /// </summary>
    public double X { get; set; }

    /// <summary>
    /// Gets or sets the Y position.
    /// </summary>
    public double Y { get; set; }

    /// <summary>
    /// Gets or sets the instance width.
    /// </summary>
    public double Width
    {
        get => _width;
        set { _width = Math.Max(1, value); OnPropertyChanged(nameof(Width)); }
    }

    /// <summary>
    /// Gets or sets the instance height.
    /// </summary>
    public double Height
    {
        get => _height;
        set { _height = Math.Max(1, value); OnPropertyChanged(nameof(Height)); }
    }

    /// <summary>
    /// Gets or sets whether to maintain aspect ratio when resizing.
    /// </summary>
    public bool MaintainAspectRatio
    {
        get => _maintainAspectRatio;
        set { _maintainAspectRatio = value; OnPropertyChanged(nameof(MaintainAspectRatio)); }
    }

    /// <summary>
    /// Gets or sets property overrides for this instance.
    /// </summary>
    public Dictionary<string, object?> Overrides { get; } = [];

    /// <summary>
    /// Gets whether this instance has any overrides.
    /// </summary>
    public bool HasOverrides => Overrides.Count > 0;

    /// <summary>
    /// Gets or sets whether this instance is detached from the master.
    /// </summary>
    public bool IsDetached { get; set; }

    protected override (double X, double Y, double Width, double Height) GetLocalBoundingBox()
    {
        return (X, Y, Width, Height);
    }

    protected override bool HitTestLocal(double x, double y)
    {
        const double tolerance = 5;
        return x >= X - tolerance && x <= X + Width + tolerance &&
               y >= Y - tolerance && y <= Y + Height + tolerance;
    }

    public override string ToSvgString()
    {
        var attrs = GetCommonSvgAttributes();
        return $"<use href=\"#{SymbolId}\" x=\"{X}\" y=\"{Y}\" width=\"{Width}\" height=\"{Height}\"{attrs}/>";
    }

    public override VectorElement Clone()
    {
        var clone = new SymbolInstance
        {
            Name = Name,
            SymbolId = SymbolId,
            X = X,
            Y = Y,
            Width = Width,
            Height = Height,
            MaintainAspectRatio = MaintainAspectRatio,
            IsDetached = IsDetached,
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            Transform = Transform,
            Fill = Fill?.Clone(),
            Stroke = Stroke?.Clone()
        };

        foreach (var kvp in Overrides)
        {
            clone.Overrides[kvp.Key] = kvp.Value;
        }

        return clone;
    }

    /// <summary>
    /// Sets an override value.
    /// </summary>
    public void SetOverride(string property, object? value)
    {
        Overrides[property] = value;
        OnPropertyChanged(nameof(Overrides));
        OnPropertyChanged(nameof(HasOverrides));
    }

    /// <summary>
    /// Removes an override.
    /// </summary>
    public void RemoveOverride(string property)
    {
        if (Overrides.Remove(property))
        {
            OnPropertyChanged(nameof(Overrides));
            OnPropertyChanged(nameof(HasOverrides));
        }
    }

    /// <summary>
    /// Clears all overrides.
    /// </summary>
    public void ClearOverrides()
    {
        Overrides.Clear();
        OnPropertyChanged(nameof(Overrides));
        OnPropertyChanged(nameof(HasOverrides));
    }

    /// <summary>
    /// Gets an override value or default.
    /// </summary>
    public T? GetOverride<T>(string property, T? defaultValue = default)
    {
        return Overrides.TryGetValue(property, out var value) && value is T typedValue
            ? typedValue
            : defaultValue;
    }
}
