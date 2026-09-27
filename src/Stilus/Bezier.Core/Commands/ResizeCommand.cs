namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;

/// <summary>
/// Command for resizing one or more vector elements.
/// </summary>
public class ResizeCommand : IEditorCommand
{
    private readonly IReadOnlyList<VectorElement> _elements;
    private readonly double _scaleX;
    private readonly double _scaleY;
    private readonly double _anchorX;
    private readonly double _anchorY;
    private readonly Dictionary<VectorElement, (double X, double Y, double Width, double Height)> _originalBounds = [];

    /// <inheritdoc/>
    public string Description => _elements.Count == 1 
        ? $"Resize {_elements[0].Name}" 
        : $"Resize {_elements.Count} elements";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <summary>
    /// Creates a new resize command.
    /// </summary>
    /// <param name="elements">Elements to resize.</param>
    /// <param name="scaleX">Horizontal scale factor.</param>
    /// <param name="scaleY">Vertical scale factor.</param>
    /// <param name="anchorX">X coordinate of the anchor point.</param>
    /// <param name="anchorY">Y coordinate of the anchor point.</param>
    public ResizeCommand(IEnumerable<VectorElement> elements, double scaleX, double scaleY, double anchorX, double anchorY)
    {
        _elements = elements.ToList();
        _scaleX = scaleX;
        _scaleY = scaleY;
        _anchorX = anchorX;
        _anchorY = anchorY;

        // Store original bounds
        foreach (var element in _elements)
        {
            var bounds = element.GetBoundingBox();
            _originalBounds[element] = bounds;
        }
    }

    /// <summary>
    /// Creates a resize command from a single element.
    /// </summary>
    public ResizeCommand(VectorElement element, double scaleX, double scaleY, double anchorX, double anchorY)
        : this([element], scaleX, scaleY, anchorX, anchorY)
    {
    }

    /// <inheritdoc/>
    public void Execute()
    {
        foreach (var element in _elements)
        {
            var original = _originalBounds[element];
            
            // Calculate new position relative to anchor
            var relX = original.X - _anchorX;
            var relY = original.Y - _anchorY;
            
            var newX = _anchorX + relX * _scaleX;
            var newY = _anchorY + relY * _scaleY;
            var newWidth = original.Width * _scaleX;
            var newHeight = original.Height * _scaleY;

            // Apply scale transform
            var currentTransform = element.Transform;
            element.Transform = new Transform
            {
                ScaleX = currentTransform.ScaleX * _scaleX,
                ScaleY = currentTransform.ScaleY * _scaleY,
                SkewX = currentTransform.SkewX,
                SkewY = currentTransform.SkewY,
                TranslateX = newX - original.X + currentTransform.TranslateX,
                TranslateY = newY - original.Y + currentTransform.TranslateY
            };
        }
    }

    /// <inheritdoc/>
    public void Undo()
    {
        foreach (var element in _elements)
        {
            var original = _originalBounds[element];
            
            // Calculate inverse scale
            var invScaleX = _scaleX != 0 ? 1.0 / _scaleX : 1;
            var invScaleY = _scaleY != 0 ? 1.0 / _scaleY : 1;
            
            // Calculate position back
            var currentTransform = element.Transform;
            var relX = original.X - _anchorX;
            var relY = original.Y - _anchorY;
            var scaledRelX = relX * _scaleX;
            var scaledRelY = relY * _scaleY;

            element.Transform = new Transform
            {
                ScaleX = currentTransform.ScaleX * invScaleX,
                ScaleY = currentTransform.ScaleY * invScaleY,
                SkewX = currentTransform.SkewX,
                SkewY = currentTransform.SkewY,
                TranslateX = currentTransform.TranslateX - (scaledRelX - relX),
                TranslateY = currentTransform.TranslateY - (scaledRelY - relY)
            };
        }
    }
}
