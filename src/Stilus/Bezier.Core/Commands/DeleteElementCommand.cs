namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;

/// <summary>
/// Command for deleting one or more elements from a document.
/// </summary>
public class DeleteElementCommand : IEditorCommand
{
    private readonly VectorDocument _document;
    private readonly (VectorElement Element, int Index)[] _deletedElements;

    /// <summary>
    /// Creates a delete element command for multiple elements.
    /// </summary>
    /// <param name="document">The document containing the elements.</param>
    /// <param name="elements">The elements to delete.</param>
    public DeleteElementCommand(VectorDocument document, IEnumerable<VectorElement> elements)
    {
        _document = document ?? throw new ArgumentNullException(nameof(document));
        
        // Store elements with their original indices for proper restoration
        _deletedElements = elements
            .Select(e => (Element: e, Index: document.Elements.IndexOf(e)))
            .Where(x => x.Index >= 0)
            .OrderByDescending(x => x.Index) // Delete from end to preserve indices
            .ToArray();
    }

    /// <summary>
    /// Creates a delete element command for a single element.
    /// </summary>
    public DeleteElementCommand(VectorDocument document, VectorElement element)
        : this(document, [element])
    {
    }

    /// <inheritdoc/>
    public string Description => _deletedElements.Length == 1
        ? $"Delete {_deletedElements[0].Element.Name ?? "element"}"
        : $"Delete {_deletedElements.Length} elements";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        foreach (var (element, _) in _deletedElements)
        {
            _document.Elements.Remove(element);
        }
        _document.IsDirty = true;
    }

    /// <inheritdoc/>
    public void Undo()
    {
        // Restore in reverse order (ascending index) to maintain correct positions
        foreach (var (element, index) in _deletedElements.OrderBy(x => x.Index))
        {
            if (index >= 0 && index <= _document.Elements.Count)
            {
                _document.Elements.Insert(index, element);
            }
            else
            {
                _document.Elements.Add(element);
            }
        }
        _document.IsDirty = true;
    }
}
