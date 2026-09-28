namespace Gesso.Core.History;

/// <summary>
/// Represents an undoable command in the history system.
/// </summary>
public interface ICommand
{
    /// <summary>
    /// Gets the display name of the command for the history panel.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Executes the command.
    /// </summary>
    void Execute();

    /// <summary>
    /// Undoes the command.
    /// </summary>
    void Undo();

    /// <summary>
    /// Gets whether this command can be merged with another command.
    /// </summary>
    bool CanMergeWith(ICommand other);

    /// <summary>
    /// Merges this command with another command.
    /// </summary>
    ICommand MergeWith(ICommand other);
}
