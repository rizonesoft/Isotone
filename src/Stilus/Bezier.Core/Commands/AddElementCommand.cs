namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;

/// <summary>
/// Command for adding an element to a document.
/// </summary>
public class AddElementCommand : IEditorCommand
{
    private readonly VectorDocument _document;
    private readonly VectorElement _element;
    private readonly int _insertIndex;

    /// <summary>
    /// Creates an add element command.
    /// </summary>
    /// <param name="document">The document to add the element to.</param>
    /// <param name="element">The element to add.</param>
    /// <param name="insertIndex">The index at which to insert the element, or -1 to append.</param>
    public AddElementCommand(VectorDocument document, VectorElement element, int insertIndex = -1)
    {
        _document = document ?? throw new ArgumentNullException(nameof(document));
        _element = element ?? throw new ArgumentNullException(nameof(element));
        _insertIndex = insertIndex;
    }

    /// <inheritdoc/>
    public string Description => $"Add {_element.Name ?? _element.GetType().Name}";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        if (_insertIndex >= 0 && _insertIndex < _document.Elements.Count)
        {
            _document.Elements.Insert(_insertIndex, _element);
        }
        else
        {
            _document.Elements.Add(_element);
        }
        _document.IsDirty = true;
    }

    /// <inheritdoc/>
    public void Undo()
    {
        _document.Elements.Remove(_element);
        _document.IsDirty = true;
    }
}
