namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;

/// <summary>
/// Specifies the type of reorder operation.
/// </summary>
public enum ReorderType
{
    /// <summary>Move to the front (top) of the stack.</summary>
    BringToFront,
    /// <summary>Move forward one position.</summary>
    BringForward,
    /// <summary>Move backward one position.</summary>
    SendBackward,
    /// <summary>Move to the back (bottom) of the stack.</summary>
    SendToBack
}

/// <summary>
/// Command for reordering elements in the document (z-order).
/// </summary>
public class ReorderCommand : IEditorCommand
{
    private readonly VectorDocument _document;
    private readonly VectorElement _element;
    private readonly ReorderType _reorderType;
    private readonly int _originalIndex;
    private int _newIndex;

    /// <summary>
    /// Creates a reorder command.
    /// </summary>
    /// <param name="document">The document containing the element.</param>
    /// <param name="element">The element to reorder.</param>
    /// <param name="reorderType">The type of reorder operation.</param>
    public ReorderCommand(VectorDocument document, VectorElement element, ReorderType reorderType)
    {
        _document = document ?? throw new ArgumentNullException(nameof(document));
        _element = element ?? throw new ArgumentNullException(nameof(element));
        _reorderType = reorderType;
        _originalIndex = document.Elements.IndexOf(element);
        
        if (_originalIndex < 0)
            throw new ArgumentException("Element not found in document", nameof(element));
    }

    /// <inheritdoc/>
    public string Description => _reorderType switch
    {
        ReorderType.BringToFront => $"Bring {_element.Name ?? "element"} to front",
        ReorderType.BringForward => $"Bring {_element.Name ?? "element"} forward",
        ReorderType.SendBackward => $"Send {_element.Name ?? "element"} backward",
        ReorderType.SendToBack => $"Send {_element.Name ?? "element"} to back",
        _ => "Reorder element"
    };

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        var count = _document.Elements.Count;
        
        _newIndex = _reorderType switch
        {
            ReorderType.BringToFront => count - 1,
            ReorderType.BringForward => Math.Min(_originalIndex + 1, count - 1),
            ReorderType.SendBackward => Math.Max(_originalIndex - 1, 0),
            ReorderType.SendToBack => 0,
            _ => _originalIndex
        };

        if (_newIndex != _originalIndex)
        {
            _document.Elements.RemoveAt(_originalIndex);
            _document.Elements.Insert(_newIndex, _element);
            _document.IsDirty = true;
        }
    }

    /// <inheritdoc/>
    public void Undo()
    {
        if (_newIndex != _originalIndex)
        {
            _document.Elements.RemoveAt(_newIndex);
            _document.Elements.Insert(_originalIndex, _element);
            _document.IsDirty = true;
        }
    }
}
