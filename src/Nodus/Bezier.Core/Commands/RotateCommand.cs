namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;

/// <summary>
/// Command for rotating one or more elements.
/// </summary>
public class RotateCommand : IEditorCommand
{
    private readonly VectorElement[] _elements;
    private readonly double _angleDegrees;
    private readonly double _centerX;
    private readonly double _centerY;

    /// <summary>
    /// Creates a rotate command for the specified elements.
    /// </summary>
    /// <param name="elements">The elements to rotate.</param>
    /// <param name="angleDegrees">The rotation angle in degrees.</param>
    /// <param name="centerX">The X coordinate of the rotation center.</param>
    /// <param name="centerY">The Y coordinate of the rotation center.</param>
    public RotateCommand(IEnumerable<VectorElement> elements, double angleDegrees, double centerX = 0, double centerY = 0)
    {
        _elements = elements.ToArray();
        _angleDegrees = angleDegrees;
        _centerX = centerX;
        _centerY = centerY;
    }

    /// <summary>
    /// Creates a rotate command for a single element.
    /// </summary>
    public RotateCommand(VectorElement element, double angleDegrees, double centerX = 0, double centerY = 0)
        : this([element], angleDegrees, centerX, centerY)
    {
    }

    /// <inheritdoc/>
    public string Description => _elements.Length == 1
        ? $"Rotate {_elements[0].Name ?? "element"}"
        : $"Rotate {_elements.Length} elements";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        var rotation = Transform.CreateRotation(_angleDegrees, _centerX, _centerY);
        foreach (var element in _elements)
        {
            element.Transform = element.Transform.Multiply(rotation);
        }
    }

    /// <inheritdoc/>
    public void Undo()
    {
        var rotation = Transform.CreateRotation(-_angleDegrees, _centerX, _centerY);
        foreach (var element in _elements)
        {
            element.Transform = element.Transform.Multiply(rotation);
        }
    }
}
