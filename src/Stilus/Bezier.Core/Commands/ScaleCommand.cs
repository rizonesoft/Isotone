namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;

/// <summary>
/// Command for scaling one or more elements.
/// </summary>
public class ScaleCommand : IEditorCommand
{
    private readonly VectorElement[] _elements;
    private readonly double _scaleX;
    private readonly double _scaleY;
    private readonly double[] _previousScaleX;
    private readonly double[] _previousScaleY;

    /// <summary>
    /// Creates a scale command for the specified elements.
    /// </summary>
    /// <param name="elements">The elements to scale.</param>
    /// <param name="scaleX">The horizontal scale factor.</param>
    /// <param name="scaleY">The vertical scale factor.</param>
    public ScaleCommand(IEnumerable<VectorElement> elements, double scaleX, double scaleY)
    {
        _elements = elements.ToArray();
        _scaleX = scaleX;
        _scaleY = scaleY;
        _previousScaleX = _elements.Select(e => e.Transform.ScaleX).ToArray();
        _previousScaleY = _elements.Select(e => e.Transform.ScaleY).ToArray();
    }

    /// <summary>
    /// Creates a scale command for a single element.
    /// </summary>
    public ScaleCommand(VectorElement element, double scaleX, double scaleY)
        : this([element], scaleX, scaleY)
    {
    }

    /// <inheritdoc/>
    public string Description => _elements.Length == 1
        ? $"Scale {_elements[0].Name ?? "element"}"
        : $"Scale {_elements.Length} elements";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        foreach (var element in _elements)
        {
            element.Transform = element.Transform with
            {
                ScaleX = element.Transform.ScaleX * _scaleX,
                ScaleY = element.Transform.ScaleY * _scaleY
            };
        }
    }

    /// <inheritdoc/>
    public void Undo()
    {
        for (var i = 0; i < _elements.Length; i++)
        {
            _elements[i].Transform = _elements[i].Transform with
            {
                ScaleX = _previousScaleX[i],
                ScaleY = _previousScaleY[i]
            };
        }
    }
}
