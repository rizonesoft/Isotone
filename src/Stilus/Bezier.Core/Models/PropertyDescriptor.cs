namespace Bezier.Core.Models;

/// <summary>
/// Type of property for UI rendering.
/// </summary>
public enum PropertyType
{
    String,
    Number,
    Boolean,
    Color,
    Gradient,
    Dropdown,
    Slider,
    Point,
    Size,
    Angle,
    StrokeStyle,
    FontFamily,
    Custom
}

/// <summary>
/// Describes a property that can be edited in the property inspector.
/// </summary>
public class PropertyDescriptor
{
    /// <summary>
    /// Gets or sets the property identifier.
    /// </summary>
    public string Id { get; init; } = string.Empty;

    /// <summary>
    /// Gets or sets the display name.
    /// </summary>
    public string Name { get; init; } = string.Empty;

    /// <summary>
    /// Gets or sets the category/section name.
    /// </summary>
    public string Category { get; init; } = "General";

    /// <summary>
    /// Gets or sets the property type.
    /// </summary>
    public PropertyType Type { get; init; } = PropertyType.String;

    /// <summary>
    /// Gets or sets the current value.
    /// </summary>
    public object? Value { get; set; }

    /// <summary>
    /// Gets or sets the minimum value (for numeric types).
    /// </summary>
    public double? Minimum { get; init; }

    /// <summary>
    /// Gets or sets the maximum value (for numeric types).
    /// </summary>
    public double? Maximum { get; init; }

    /// <summary>
    /// Gets or sets the step increment (for numeric types).
    /// </summary>
    public double Step { get; init; } = 1;

    /// <summary>
    /// Gets or sets the unit suffix (e.g., "px", "%", "°").
    /// </summary>
    public string? Unit { get; init; }

    /// <summary>
    /// Gets or sets dropdown options (for Dropdown type).
    /// </summary>
    public IReadOnlyList<string>? Options { get; init; }

    /// <summary>
    /// Gets or sets whether the property is read-only.
    /// </summary>
    public bool IsReadOnly { get; init; }

    /// <summary>
    /// Gets or sets the tooltip text.
    /// </summary>
    public string? Tooltip { get; init; }

    /// <summary>
    /// Gets or sets the sort order within the category.
    /// </summary>
    public int Order { get; init; }

    /// <summary>
    /// Event raised when the value changes.
    /// </summary>
    public event EventHandler<object?>? ValueChanged;

    /// <summary>
    /// Sets the value and raises the ValueChanged event.
    /// </summary>
    public void SetValue(object? value)
    {
        if (!Equals(Value, value))
        {
            Value = value;
            ValueChanged?.Invoke(this, value);
        }
    }
}

/// <summary>
/// A group of related properties.
/// </summary>
public class PropertyGroup
{
    /// <summary>
    /// Gets or sets the group name.
    /// </summary>
    public string Name { get; init; } = string.Empty;

    /// <summary>
    /// Gets or sets whether the group is expanded.
    /// </summary>
    public bool IsExpanded { get; set; } = true;

    /// <summary>
    /// Gets or sets the sort order.
    /// </summary>
    public int Order { get; init; }

    /// <summary>
    /// Gets the properties in this group.
    /// </summary>
    public List<PropertyDescriptor> Properties { get; } = [];
}

/// <summary>
/// Provides property descriptors for a selected element.
/// </summary>
public interface IPropertyProvider
{
    /// <summary>
    /// Gets property groups for the element.
    /// </summary>
    IEnumerable<PropertyGroup> GetPropertyGroups();

    /// <summary>
    /// Applies a property change to the element.
    /// </summary>
    void ApplyPropertyChange(string propertyId, object? value);
}
