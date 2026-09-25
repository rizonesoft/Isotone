namespace Bezier.Core.Interfaces;

/// <summary>
/// Represents an undoable/redoable editor command.
/// </summary>
public interface IEditorCommand
{
    /// <summary>
    /// Gets a description of this command for display in the UI.
    /// </summary>
    string Description { get; }
    
    /// <summary>
    /// Gets whether this command can be undone.
    /// </summary>
    bool IsUndoable { get; }
    
    /// <summary>
    /// Executes the command.
    /// </summary>
    void Execute();
    
    /// <summary>
    /// Undoes the command, reverting changes.
    /// </summary>
    void Undo();
}
