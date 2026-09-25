namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;

/// <summary>
/// Command for grouping multiple elements into a single group.
/// </summary>
public class GroupCommand : IEditorCommand
{
    private readonly VectorDocument _document;
    private readonly VectorElement[] _elements;
    private readonly int[] _originalIndices;
    private SvgGroup? _group;

    /// <summary>
    /// Creates a group command.
    /// </summary>
    /// <param name="document">The document containing the elements.</param>
    /// <param name="elements">The elements to group.</param>
    public GroupCommand(VectorDocument document, IEnumerable<VectorElement> elements)
    {
        _document = document ?? throw new ArgumentNullException(nameof(document));
        _elements = elements.ToArray();
        
        if (_elements.Length < 2)
            throw new ArgumentException("At least 2 elements are required to create a group", nameof(elements));

        // Store original indices for proper restoration
        _originalIndices = _elements
            .Select(e => document.Elements.IndexOf(e))
            .ToArray();
    }

    /// <inheritdoc/>
    public string Description => $"Group {_elements.Length} elements";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        // Create the group
        _group = new SvgGroup
        {
            Name = "Group"
        };

        // Find the insertion point (lowest index of selected elements)
        var insertIndex = _originalIndices.Where(i => i >= 0).DefaultIfEmpty(0).Min();

        // Remove elements from document (in reverse order to preserve indices)
        foreach (var element in _elements.OrderByDescending(e => _document.Elements.IndexOf(e)))
        {
            _document.Elements.Remove(element);
        }

        // Add elements to group (preserving original order)
        var orderedElements = _elements
            .Select((e, i) => (Element: e, OriginalIndex: _originalIndices[i]))
            .OrderBy(x => x.OriginalIndex)
            .Select(x => x.Element);

        foreach (var element in orderedElements)
        {
            _group.Children.Add(element);
        }

        // Insert group at the lowest original index
        insertIndex = Math.Min(insertIndex, _document.Elements.Count);
        _document.Elements.Insert(insertIndex, _group);
        _document.IsDirty = true;
    }

    /// <inheritdoc/>
    public void Undo()
    {
        if (_group is null) return;

        // Remove the group
        _document.Elements.Remove(_group);

        // Restore elements at their original positions
        var elementsWithIndices = _elements
            .Select((e, i) => (Element: e, OriginalIndex: _originalIndices[i]))
            .OrderBy(x => x.OriginalIndex);

        foreach (var (element, originalIndex) in elementsWithIndices)
        {
            var insertIndex = Math.Min(originalIndex, _document.Elements.Count);
            _document.Elements.Insert(insertIndex, element);
        }

        // Clear group children
        _group.Children.Clear();
        _document.IsDirty = true;
    }
}
