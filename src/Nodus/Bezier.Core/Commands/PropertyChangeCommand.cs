namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;

/// <summary>
/// Command for changing a property value on an object.
/// </summary>
/// <typeparam name="T">The type of the property value.</typeparam>
public class PropertyChangeCommand<T> : IEditorCommand
{
    private readonly object _target;
    private readonly string _propertyName;
    private readonly T _newValue;
    private readonly T _oldValue;
    private readonly Action<T> _setter;
    private readonly Func<T> _getter;

    /// <summary>
    /// Creates a property change command using reflection.
    /// </summary>
    /// <param name="target">The object containing the property.</param>
    /// <param name="propertyName">The name of the property to change.</param>
    /// <param name="newValue">The new value for the property.</param>
    public PropertyChangeCommand(object target, string propertyName, T newValue)
    {
        _target = target ?? throw new ArgumentNullException(nameof(target));
        _propertyName = propertyName ?? throw new ArgumentNullException(nameof(propertyName));
        _newValue = newValue;

        var property = target.GetType().GetProperty(propertyName)
            ?? throw new ArgumentException($"Property '{propertyName}' not found on type '{target.GetType().Name}'");

        _getter = () => (T)property.GetValue(_target)!;
        _setter = value => property.SetValue(_target, value);
        _oldValue = _getter();
    }

    /// <summary>
    /// Creates a property change command using explicit getter and setter.
    /// </summary>
    /// <param name="description">Description of the change.</param>
    /// <param name="getter">Function to get the current value.</param>
    /// <param name="setter">Action to set the new value.</param>
    /// <param name="newValue">The new value.</param>
    public PropertyChangeCommand(string description, Func<T> getter, Action<T> setter, T newValue)
    {
        _target = null!;
        _propertyName = description;
        _getter = getter ?? throw new ArgumentNullException(nameof(getter));
        _setter = setter ?? throw new ArgumentNullException(nameof(setter));
        _newValue = newValue;
        _oldValue = _getter();
    }

    /// <inheritdoc/>
    public string Description => $"Change {_propertyName}";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        _setter(_newValue);
    }

    /// <inheritdoc/>
    public void Undo()
    {
        _setter(_oldValue);
    }
}
