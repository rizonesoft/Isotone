namespace Bezier.Core.Interfaces;

/// <summary>
/// Represents an option for a tool.
/// </summary>
public interface IToolOption
{
    /// <summary>
    /// Gets the unique identifier for this option.
    /// </summary>
    string Id { get; }

    /// <summary>
    /// Gets the display name.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets the tooltip text.
    /// </summary>
    string? Tooltip { get; }

    /// <summary>
    /// Gets whether this option is enabled.
    /// </summary>
    bool IsEnabled { get; }
}

/// <summary>
/// A numeric tool option with min/max constraints.
/// </summary>
public class NumericToolOption : IToolOption
{
    public string Id { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public string? Tooltip { get; init; }
    public bool IsEnabled { get; set; } = true;

    public double Value { get; set; }
    public double Minimum { get; set; } = 0;
    public double Maximum { get; set; } = 100;
    public double Step { get; set; } = 1;
    public string? Unit { get; init; }

    public event EventHandler<double>? ValueChanged;

    public void SetValue(double value)
    {
        var clamped = Math.Clamp(value, Minimum, Maximum);
        if (Math.Abs(Value - clamped) > double.Epsilon)
        {
            Value = clamped;
            ValueChanged?.Invoke(this, clamped);
        }
    }
}

/// <summary>
/// A boolean toggle tool option.
/// </summary>
public class ToggleToolOption : IToolOption
{
    public string Id { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public string? Tooltip { get; init; }
    public bool IsEnabled { get; set; } = true;

    public bool IsChecked { get; set; }

    public event EventHandler<bool>? CheckedChanged;

    public void SetChecked(bool value)
    {
        if (IsChecked != value)
        {
            IsChecked = value;
            CheckedChanged?.Invoke(this, value);
        }
    }
}

/// <summary>
/// A dropdown selection tool option.
/// </summary>
public class DropdownToolOption : IToolOption
{
    public string Id { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public string? Tooltip { get; init; }
    public bool IsEnabled { get; set; } = true;

    public IReadOnlyList<string> Items { get; init; } = [];
    public int SelectedIndex { get; set; }
    public string? SelectedItem => SelectedIndex >= 0 && SelectedIndex < Items.Count 
        ? Items[SelectedIndex] 
        : null;

    public event EventHandler<int>? SelectionChanged;

    public void SetSelectedIndex(int index)
    {
        if (index >= 0 && index < Items.Count && SelectedIndex != index)
        {
            SelectedIndex = index;
            SelectionChanged?.Invoke(this, index);
        }
    }
}

/// <summary>
/// A color picker tool option.
/// </summary>
public class ColorToolOption : IToolOption
{
    public string Id { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public string? Tooltip { get; init; }
    public bool IsEnabled { get; set; } = true;

    public uint Color { get; set; } = 0xFF000000;
    public bool ShowAlpha { get; init; } = true;

    public event EventHandler<uint>? ColorChanged;

    public void SetColor(uint color)
    {
        if (Color != color)
        {
            Color = color;
            ColorChanged?.Invoke(this, color);
        }
    }
}

/// <summary>
/// Provides tool options for a specific tool.
/// </summary>
public interface IToolOptionsProvider
{
    /// <summary>
    /// Gets the options for this tool.
    /// </summary>
    IReadOnlyList<IToolOption> Options { get; }

    /// <summary>
    /// Event raised when any option changes.
    /// </summary>
    event EventHandler? OptionsChanged;
}
