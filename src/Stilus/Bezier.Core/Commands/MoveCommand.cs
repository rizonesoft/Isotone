namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;

/// <summary>
/// Command for moving one or more elements.
/// </summary>
public class MoveCommand : IEditorCommand
{
    private readonly VectorElement[] _elements;
    private readonly double _deltaX;
    private readonly double _deltaY;

    /// <summary>
    /// Creates a move command for the specified elements.
    /// </summary>
    /// <param name="elements">The elements to move.</param>
    /// <param name="deltaX">The horizontal distance to move.</param>
    /// <param name="deltaY">The vertical distance to move.</param>
    public MoveCommand(IEnumerable<VectorElement> elements, double deltaX, double deltaY)
    {
        _elements = elements.ToArray();
        _deltaX = deltaX;
        _deltaY = deltaY;
    }

    /// <summary>
    /// Creates a move command for a single element.
    /// </summary>
    public MoveCommand(VectorElement element, double deltaX, double deltaY)
        : this([element], deltaX, deltaY)
    {
    }

    /// <inheritdoc/>
    public string Description => _elements.Length == 1
        ? $"Move {_elements[0].Name ?? "element"}"
        : $"Move {_elements.Length} elements";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        foreach (var element in _elements)
        {
            element.Transform = element.Transform with
            {
                TranslateX = element.Transform.TranslateX + _deltaX,
                TranslateY = element.Transform.TranslateY + _deltaY
            };
        }
    }

    /// <inheritdoc/>
    public void Undo()
    {
        foreach (var element in _elements)
        {
            element.Transform = element.Transform with
            {
                TranslateX = element.Transform.TranslateX - _deltaX,
                TranslateY = element.Transform.TranslateY - _deltaY
            };
        }
    }
}
