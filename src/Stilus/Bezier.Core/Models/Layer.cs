using System.Collections.ObjectModel;
using System.ComponentModel;

namespace Bezier.Core.Models;

/// <summary>
/// Represents a layer in the document that can contain elements.
/// </summary>
public class Layer : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private string _name = "Layer";
    private bool _isVisible = true;
    private bool _isLocked;
    private bool _isExpanded = true;
    private double _opacity = 1.0;
    private BlendMode _blendMode = BlendMode.Normal;
    private Layer? _parent;

    /// <summary>
    /// Gets or sets the unique identifier for this layer.
    /// </summary>
    public Guid Id { get; init; } = Guid.NewGuid();

    /// <summary>
    /// Gets or sets the layer name.
    /// </summary>
    public string Name
    {
        get => _name;
        set { _name = value; OnPropertyChanged(nameof(Name)); }
    }

    /// <summary>
    /// Gets or sets whether this layer is visible.
    /// </summary>
    public bool IsVisible
    {
        get => _isVisible;
        set { _isVisible = value; OnPropertyChanged(nameof(IsVisible)); }
    }

    /// <summary>
    /// Gets or sets whether this layer is locked.
    /// </summary>
    public bool IsLocked
    {
        get => _isLocked;
        set { _isLocked = value; OnPropertyChanged(nameof(IsLocked)); }
    }

    /// <summary>
    /// Gets or sets whether this layer is expanded in the UI.
    /// </summary>
    public bool IsExpanded
    {
        get => _isExpanded;
        set { _isExpanded = value; OnPropertyChanged(nameof(IsExpanded)); }
    }

    /// <summary>
    /// Gets or sets the layer opacity (0.0 to 1.0).
    /// </summary>
    public double Opacity
    {
        get => _opacity;
        set { _opacity = Math.Clamp(value, 0, 1); OnPropertyChanged(nameof(Opacity)); }
    }

    /// <summary>
    /// Gets or sets the blend mode for this layer.
    /// </summary>
    public BlendMode BlendMode
    {
        get => _blendMode;
        set { _blendMode = value; OnPropertyChanged(nameof(BlendMode)); }
    }

    /// <summary>
    /// Gets or sets the parent layer (for nested groups).
    /// </summary>
    public Layer? Parent
    {
        get => _parent;
        set { _parent = value; OnPropertyChanged(nameof(Parent)); }
    }

    /// <summary>
    /// Gets the elements in this layer.
    /// </summary>
    public ObservableCollection<VectorElement> Elements { get; } = [];

    /// <summary>
    /// Gets the child layers (for groups).
    /// </summary>
    public ObservableCollection<Layer> Children { get; } = [];

    /// <summary>
    /// Gets whether this layer is a group (has children).
    /// </summary>
    public bool IsGroup => Children.Count > 0;

    /// <summary>
    /// Gets the depth of this layer in the hierarchy.
    /// </summary>
    public int Depth
    {
        get
        {
            var depth = 0;
            var current = Parent;
            while (current != null)
            {
                depth++;
                current = current.Parent;
            }
            return depth;
        }
    }

    /// <summary>
    /// Gets whether this layer is effectively visible (considering parent visibility).
    /// </summary>
    public bool IsEffectivelyVisible
    {
        get
        {
            if (!IsVisible) return false;
            return Parent?.IsEffectivelyVisible ?? true;
        }
    }

    /// <summary>
    /// Gets whether this layer is effectively locked (considering parent lock state).
    /// </summary>
    public bool IsEffectivelyLocked
    {
        get
        {
            if (IsLocked) return true;
            return Parent?.IsEffectivelyLocked ?? false;
        }
    }

    /// <summary>
    /// Adds an element to this layer.
    /// </summary>
    public void AddElement(VectorElement element)
    {
        element.Parent = null; // Clear any previous parent reference
        Elements.Add(element);
    }

    /// <summary>
    /// Removes an element from this layer.
    /// </summary>
    public bool RemoveElement(VectorElement element)
    {
        return Elements.Remove(element);
    }

    /// <summary>
    /// Adds a child layer.
    /// </summary>
    public void AddChild(Layer child)
    {
        child.Parent = this;
        Children.Add(child);
    }

    /// <summary>
    /// Removes a child layer.
    /// </summary>
    public bool RemoveChild(Layer child)
    {
        if (Children.Remove(child))
        {
            child.Parent = null;
            return true;
        }
        return false;
    }

    /// <summary>
    /// Gets all elements recursively (including from child layers).
    /// </summary>
    public IEnumerable<VectorElement> GetAllElements()
    {
        foreach (var element in Elements)
        {
            yield return element;
        }

        foreach (var child in Children)
        {
            foreach (var element in child.GetAllElements())
            {
                yield return element;
            }
        }
    }

    /// <summary>
    /// Gets all visible elements recursively.
    /// </summary>
    public IEnumerable<VectorElement> GetVisibleElements()
    {
        if (!IsEffectivelyVisible) yield break;

        foreach (var element in Elements)
        {
            if (element.IsVisible)
                yield return element;
        }

        foreach (var child in Children)
        {
            foreach (var element in child.GetVisibleElements())
            {
                yield return element;
            }
        }
    }

    /// <summary>
    /// Finds an element by ID in this layer or its children.
    /// </summary>
    public VectorElement? FindElement(Guid id)
    {
        var found = Elements.FirstOrDefault(e => e.Id == id);
        if (found != null) return found;

        foreach (var child in Children)
        {
            found = child.FindElement(id);
            if (found != null) return found;
        }

        return null;
    }

    /// <summary>
    /// Creates a clone of this layer.
    /// </summary>
    public Layer Clone()
    {
        var clone = new Layer
        {
            Name = Name + " Copy",
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            IsExpanded = IsExpanded,
            Opacity = Opacity,
            BlendMode = BlendMode
        };

        foreach (var element in Elements)
        {
            clone.Elements.Add(element.Clone());
        }

        foreach (var child in Children)
        {
            clone.AddChild(child.Clone());
        }

        return clone;
    }
}
