namespace Bezier.Core.Services;

using Bezier.Core.Interfaces;

/// <summary>
/// Manages undo/redo history using the Command pattern.
/// </summary>
public class HistoryManager
{
    private readonly Stack<IEditorCommand> _undoStack = new();
    private readonly Stack<IEditorCommand> _redoStack = new();
    private int _maxHistorySize = 100;

    /// <summary>
    /// Gets or sets the maximum number of commands to keep in history.
    /// </summary>
    public int MaxHistorySize
    {
        get => _maxHistorySize;
        set
        {
            _maxHistorySize = Math.Max(1, value);
            TrimHistory();
        }
    }

    /// <summary>
    /// Gets whether there are commands to undo.
    /// </summary>
    public bool CanUndo => _undoStack.Count > 0;

    /// <summary>
    /// Gets whether there are commands to redo.
    /// </summary>
    public bool CanRedo => _redoStack.Count > 0;

    /// <summary>
    /// Gets the number of commands in the undo stack.
    /// </summary>
    public int UndoCount => _undoStack.Count;

    /// <summary>
    /// Gets the number of commands in the redo stack.
    /// </summary>
    public int RedoCount => _redoStack.Count;

    /// <summary>
    /// Gets the description of the next command to undo.
    /// </summary>
    public string? NextUndoDescription => _undoStack.Count > 0 ? _undoStack.Peek().Description : null;

    /// <summary>
    /// Gets the description of the next command to redo.
    /// </summary>
    public string? NextRedoDescription => _redoStack.Count > 0 ? _redoStack.Peek().Description : null;

    /// <summary>
    /// Event raised when the history state changes.
    /// </summary>
    public event EventHandler? HistoryChanged;

    /// <summary>
    /// Executes a command and adds it to the undo stack.
    /// </summary>
    /// <param name="command">The command to execute.</param>
    public void ExecuteCommand(IEditorCommand command)
    {
        ArgumentNullException.ThrowIfNull(command);

        command.Execute();

        if (command.IsUndoable)
        {
            _undoStack.Push(command);
            _redoStack.Clear();
            TrimHistory();
        }

        OnHistoryChanged();
    }

    /// <summary>
    /// Undoes the most recent command.
    /// </summary>
    /// <returns>True if a command was undone; false if the undo stack is empty.</returns>
    public bool Undo()
    {
        if (_undoStack.Count == 0)
            return false;

        var command = _undoStack.Pop();
        command.Undo();
        _redoStack.Push(command);

        OnHistoryChanged();
        return true;
    }

    /// <summary>
    /// Redoes the most recently undone command.
    /// </summary>
    /// <returns>True if a command was redone; false if the redo stack is empty.</returns>
    public bool Redo()
    {
        if (_redoStack.Count == 0)
            return false;

        var command = _redoStack.Pop();
        command.Execute();
        _undoStack.Push(command);

        OnHistoryChanged();
        return true;
    }

    /// <summary>
    /// Clears all history.
    /// </summary>
    public void Clear()
    {
        _undoStack.Clear();
        _redoStack.Clear();
        OnHistoryChanged();
    }

    /// <summary>
    /// Gets a list of undo command descriptions (most recent first).
    /// </summary>
    public IReadOnlyList<string> GetUndoDescriptions()
    {
        return _undoStack.Select(c => c.Description).ToList();
    }

    /// <summary>
    /// Gets a list of redo command descriptions (most recent first).
    /// </summary>
    public IReadOnlyList<string> GetRedoDescriptions()
    {
        return _redoStack.Select(c => c.Description).ToList();
    }

    private void TrimHistory()
    {
        while (_undoStack.Count > _maxHistorySize)
        {
            // Remove oldest items (bottom of stack)
            var items = _undoStack.ToArray();
            _undoStack.Clear();
            for (var i = 0; i < _maxHistorySize; i++)
            {
                _undoStack.Push(items[items.Length - 1 - i]);
            }
            // Re-reverse to maintain order
            items = _undoStack.ToArray();
            _undoStack.Clear();
            foreach (var item in items)
            {
                _undoStack.Push(item);
            }
        }
    }

    private void OnHistoryChanged()
    {
        HistoryChanged?.Invoke(this, EventArgs.Empty);
    }
}
