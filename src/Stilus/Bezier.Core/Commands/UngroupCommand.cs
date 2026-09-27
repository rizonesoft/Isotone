namespace Bezier.Core.Commands;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;

/// <summary>
/// Command for ungrouping a group into its constituent elements.
/// </summary>
public class UngroupCommand : IEditorCommand
{
    private readonly VectorDocument _document;
    private readonly SvgGroup _group;
    private readonly int _groupIndex;
    private readonly VectorElement[] _children;

    /// <summary>
    /// Creates an ungroup command.
    /// </summary>
    /// <param name="document">The document containing the group.</param>
    /// <param name="group">The group to ungroup.</param>
    public UngroupCommand(VectorDocument document, SvgGroup group)
    {
        _document = document ?? throw new ArgumentNullException(nameof(document));
        _group = group ?? throw new ArgumentNullException(nameof(group));
        _groupIndex = document.Elements.IndexOf(group);
        
        if (_groupIndex < 0)
            throw new ArgumentException("Group not found in document", nameof(group));

        // Store children for restoration
        _children = group.Children.ToArray();
    }

    /// <inheritdoc/>
    public string Description => $"Ungroup {_group.Name ?? "group"}";

    /// <inheritdoc/>
    public bool IsUndoable => true;

    /// <inheritdoc/>
    public void Execute()
    {
        // Remove the group
        _document.Elements.Remove(_group);

        // Insert children at the group's position
        var insertIndex = _groupIndex;
        foreach (var child in _children)
        {
            // Apply group transform to children if needed
            if (!_group.Transform.IsIdentity)
            {
                child.Transform = CombineTransforms(child.Transform, _group.Transform);
            }

            _document.Elements.Insert(insertIndex, child);
            insertIndex++;
        }

        // Clear group children
        _group.Children.Clear();
        _document.IsDirty = true;
    }

    /// <inheritdoc/>
    public void Undo()
    {
        // Remove children from document
        foreach (var child in _children)
        {
            _document.Elements.Remove(child);
            
            // Restore original transform (remove group transform)
            if (!_group.Transform.IsIdentity)
            {
                child.Transform = RemoveParentTransform(child.Transform, _group.Transform);
            }
        }

        // Restore children to group
        foreach (var child in _children)
        {
            _group.Children.Add(child);
        }

        // Insert group back
        var insertIndex = Math.Min(_groupIndex, _document.Elements.Count);
        _document.Elements.Insert(insertIndex, _group);
        _document.IsDirty = true;
    }

    private static Transform CombineTransforms(Transform child, Transform parent)
    {
        // Combine transforms using matrix multiplication
        return parent.Multiply(child);
    }

    private static Transform RemoveParentTransform(Transform combined, Transform parent)
    {
        // Remove parent transform by multiplying with inverse
        return parent.Invert().Multiply(combined);
    }
}
