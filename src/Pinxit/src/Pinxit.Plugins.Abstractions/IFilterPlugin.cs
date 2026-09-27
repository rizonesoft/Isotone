namespace Pinxit.Plugins;

/// <summary>
/// Interface for filter plugins that process images.
/// </summary>
public interface IFilterPlugin : IPlugin
{
    /// <summary>
    /// Gets the category of the filter (e.g., "Blur", "Sharpen").
    /// </summary>
    string Category { get; }

    /// <summary>
    /// Gets whether the filter supports real-time preview.
    /// </summary>
    bool SupportsPreview { get; }

    /// <summary>
    /// Gets the filter parameters.
    /// </summary>
    IReadOnlyList<FilterParameter> Parameters { get; }

    /// <summary>
    /// Applies the filter to the image data.
    /// </summary>
    void Apply(Span<byte> imageData, int width, int height, IDictionary<string, object> parameters);
}

/// <summary>
/// Represents a filter parameter.
/// </summary>
public sealed class FilterParameter
{
    public required string Name { get; init; }
    public required string DisplayName { get; init; }
    public required FilterParameterType Type { get; init; }
    public required object DefaultValue { get; init; }
    public object? MinValue { get; init; }
    public object? MaxValue { get; init; }
}

/// <summary>
/// Types of filter parameters.
/// </summary>
public enum FilterParameterType
{
    Integer,
    Float,
    Boolean,
    Color,
    String,
    Enum
}
