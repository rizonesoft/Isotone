namespace Imago.Core.History.Commands;

/// <summary>
/// Base class for undoable commands with common functionality.
/// </summary>
public abstract class CommandBase : ICommand
{
    /// <inheritdoc />
    public abstract string Name { get; }

    /// <summary>
    /// Gets the timestamp when this command was created.
    /// </summary>
    public DateTime CreatedAt { get; } = DateTime.UtcNow;

    /// <summary>
    /// Gets the command category for grouping in UI.
    /// </summary>
    public virtual CommandCategory Category => CommandCategory.General;

    /// <inheritdoc />
    public abstract void Execute();

    /// <inheritdoc />
    public abstract void Undo();

    /// <inheritdoc />
    public virtual bool CanMergeWith(ICommand other) => false;

    /// <inheritdoc />
    public virtual ICommand MergeWith(ICommand other) => this;
}

/// <summary>
/// Categories of commands for UI organization.
/// </summary>
public enum CommandCategory
{
    General,
    Layer,
    Selection,
    Paint,
    Transform,
    Filter,
    Adjustment,
    Text
}

/// <summary>
/// A command that captures before/after state using snapshots.
/// </summary>
public abstract class SnapshotCommand : CommandBase, IDisposable
{
    private HistorySnapshot? _beforeSnapshot;
    private HistorySnapshot? _afterSnapshot;
    private bool _disposed;

    /// <summary>
    /// Gets the size of the state being captured.
    /// </summary>
    protected abstract int StateSize { get; }

    /// <summary>
    /// Captures the current state to a span.
    /// </summary>
    protected abstract void CaptureState(Span<byte> target);

    /// <summary>
    /// Restores state from a span.
    /// </summary>
    protected abstract void RestoreState(ReadOnlySpan<byte> source);

    /// <summary>
    /// Performs the actual operation (called during Execute).
    /// </summary>
    protected abstract void PerformOperation();

    /// <inheritdoc />
    public sealed override void Execute()
    {
        // Capture before state
        _beforeSnapshot = HistorySnapshot.Create(StateSize, CaptureState);

        // Perform the operation
        PerformOperation();

        // Capture after state
        _afterSnapshot = HistorySnapshot.Create(StateSize, CaptureState);
    }

    /// <inheritdoc />
    public sealed override void Undo()
    {
        if (_beforeSnapshot is null)
            throw new InvalidOperationException("Cannot undo: no before snapshot");

        _beforeSnapshot.RestoreTo(RestoreState);
    }

    /// <summary>
    /// Re-applies the command after an undo.
    /// </summary>
    public void Redo()
    {
        if (_afterSnapshot is null)
            throw new InvalidOperationException("Cannot redo: no after snapshot");

        _afterSnapshot.RestoreTo(RestoreState);
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;

        if (disposing)
        {
            _beforeSnapshot?.Dispose();
            _afterSnapshot?.Dispose();
        }

        _disposed = true;
    }
}

/// <summary>
/// A simple command using delegates for execute/undo.
/// </summary>
public sealed class DelegateCommand : CommandBase
{
    private readonly Action _execute;
    private readonly Action _undo;
    private readonly string _name;

    public DelegateCommand(string name, Action execute, Action undo)
    {
        _name = name;
        _execute = execute;
        _undo = undo;
    }

    public override string Name => _name;

    public override void Execute() => _execute();

    public override void Undo() => _undo();
}

/// <summary>
/// A command that can be coalesced with similar commands within a time window.
/// </summary>
public abstract class CoalescingCommand : CommandBase
{
    /// <summary>
    /// Time window for coalescing (commands within this window can be merged).
    /// </summary>
    public virtual TimeSpan CoalesceWindow => TimeSpan.FromMilliseconds(500);

    /// <inheritdoc />
    public override bool CanMergeWith(ICommand other)
    {
        if (other is not CoalescingCommand)
            return false;

        // Same type and within time window
        return other.GetType() == GetType() &&
               DateTime.UtcNow - CreatedAt < CoalesceWindow;
    }
}
