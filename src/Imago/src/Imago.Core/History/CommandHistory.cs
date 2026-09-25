namespace Imago.Core.History;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Manages undo/redo history for a document.
/// </summary>
public sealed partial class CommandHistory : ObservableObject
{
    private readonly List<ICommand> _undoStack = new();
    private readonly List<ICommand> _redoStack = new();
    private readonly int _maxHistorySize;

    [ObservableProperty]
    private bool _canUndo;

    [ObservableProperty]
    private bool _canRedo;

    [ObservableProperty]
    private string? _undoName;

    [ObservableProperty]
    private string? _redoName;

    public IReadOnlyList<ICommand> UndoStack => _undoStack;
    public IReadOnlyList<ICommand> RedoStack => _redoStack;

    public CommandHistory(int maxHistorySize = 100)
    {
        _maxHistorySize = maxHistorySize;
    }

    public void Execute(ICommand command)
    {
        ArgumentNullException.ThrowIfNull(command);

        if (_undoStack.Count > 0)
        {
            var lastCommand = _undoStack[^1];
            if (lastCommand.CanMergeWith(command))
            {
                _undoStack[^1] = lastCommand.MergeWith(command);
                UpdateState();
                return;
            }
        }

        command.Execute();
        _undoStack.Add(command);
        _redoStack.Clear();

        while (_undoStack.Count > _maxHistorySize)
        {
            _undoStack.RemoveAt(0);
        }

        UpdateState();
    }

    public void Undo()
    {
        if (_undoStack.Count == 0)
        {
            return;
        }

        var command = _undoStack[^1];
        _undoStack.RemoveAt(_undoStack.Count - 1);

        command.Undo();
        _redoStack.Add(command);

        UpdateState();
    }

    public void Redo()
    {
        if (_redoStack.Count == 0)
        {
            return;
        }

        var command = _redoStack[^1];
        _redoStack.RemoveAt(_redoStack.Count - 1);

        command.Execute();
        _undoStack.Add(command);

        UpdateState();
    }

    public void Clear()
    {
        _undoStack.Clear();
        _redoStack.Clear();
        UpdateState();
    }

    private void UpdateState()
    {
        CanUndo = _undoStack.Count > 0;
        CanRedo = _redoStack.Count > 0;
        UndoName = _undoStack.Count > 0 ? _undoStack[^1].Name : null;
        RedoName = _redoStack.Count > 0 ? _redoStack[^1].Name : null;
    }
}
