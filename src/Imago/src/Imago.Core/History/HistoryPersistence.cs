namespace Imago.Core.History;

using System.IO;
using System.Text.Json;
using Serilog;

/// <summary>
/// Provides crash recovery persistence for command history.
/// Saves history state to disk for recovery after unexpected termination.
/// </summary>
public sealed class HistoryPersistence : IDisposable
{
    private static readonly ILogger s_logger = Log.ForContext<HistoryPersistence>();

    private readonly string _persistencePath;
    private readonly TimeSpan _autoSaveInterval;
    private Timer? _autoSaveTimer;
    private CommandHistory? _trackedHistory;

    public HistoryPersistence(string? basePath = null, TimeSpan? autoSaveInterval = null)
    {
        var appDataPath = basePath ?? Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "Imago",
            "recovery");

        Directory.CreateDirectory(appDataPath);
        _persistencePath = Path.Combine(appDataPath, "history.json");
        _autoSaveInterval = autoSaveInterval ?? TimeSpan.FromSeconds(30);
    }

    /// <summary>
    /// Starts tracking a command history for auto-save.
    /// </summary>
    public void StartTracking(CommandHistory history)
    {
        _trackedHistory = history;
        _autoSaveTimer = new Timer(OnAutoSave, null, _autoSaveInterval, _autoSaveInterval);
        s_logger.Debug("History persistence started, interval: {Interval}s", _autoSaveInterval.TotalSeconds);
    }

    /// <summary>
    /// Stops tracking and auto-save.
    /// </summary>
    public void StopTracking()
    {
        _autoSaveTimer?.Dispose();
        _autoSaveTimer = null;
        _trackedHistory = null;
        s_logger.Debug("History persistence stopped");
    }

    /// <summary>
    /// Saves the current history state to disk.
    /// </summary>
    public void Save(CommandHistory history)
    {
        try
        {
            var state = new HistoryState
            {
                SavedAt = DateTime.UtcNow,
                UndoCount = history.UndoStack.Count,
                RedoCount = history.RedoStack.Count,
                CommandNames = history.UndoStack.Select(c => c.Name).ToList()
            };

            var json = JsonSerializer.Serialize(state, HistoryJsonContext.Default.HistoryState);
            File.WriteAllText(_persistencePath, json);

            s_logger.Debug("History saved: {UndoCount} undo, {RedoCount} redo", state.UndoCount, state.RedoCount);
        }
        catch (Exception ex)
        {
            s_logger.Warning(ex, "Failed to save history state");
        }
    }

    /// <summary>
    /// Checks if a recovery file exists.
    /// </summary>
    public bool HasRecoveryData()
    {
        return File.Exists(_persistencePath);
    }

    /// <summary>
    /// Loads recovery information (metadata only, not full state).
    /// </summary>
    public HistoryRecoveryInfo? LoadRecoveryInfo()
    {
        if (!HasRecoveryData()) return null;

        try
        {
            var json = File.ReadAllText(_persistencePath);
            var state = JsonSerializer.Deserialize(json, HistoryJsonContext.Default.HistoryState);

            if (state is null) return null;

            return new HistoryRecoveryInfo
            {
                SavedAt = state.SavedAt,
                UndoCount = state.UndoCount,
                CommandNames = state.CommandNames
            };
        }
        catch (Exception ex)
        {
            s_logger.Warning(ex, "Failed to load recovery info");
            return null;
        }
    }

    /// <summary>
    /// Clears the recovery data (call after successful load or user dismissal).
    /// </summary>
    public void ClearRecoveryData()
    {
        try
        {
            if (File.Exists(_persistencePath))
            {
                File.Delete(_persistencePath);
                s_logger.Debug("Recovery data cleared");
            }
        }
        catch (Exception ex)
        {
            s_logger.Warning(ex, "Failed to clear recovery data");
        }
    }

    private void OnAutoSave(object? state)
    {
        if (_trackedHistory is not null)
        {
            Save(_trackedHistory);
        }
    }

    public void Dispose()
    {
        _autoSaveTimer?.Dispose();
        _autoSaveTimer = null;
    }
}

/// <summary>
/// Serializable history state for persistence.
/// </summary>
public sealed class HistoryState
{
    public DateTime SavedAt { get; set; }
    public int UndoCount { get; set; }
    public int RedoCount { get; set; }
    public List<string> CommandNames { get; set; } = [];
}

/// <summary>
/// Recovery information shown to user after crash.
/// </summary>
public sealed class HistoryRecoveryInfo
{
    public DateTime SavedAt { get; set; }
    public int UndoCount { get; set; }
    public List<string> CommandNames { get; set; } = [];
}

/// <summary>
/// JSON serialization context for AOT compatibility.
/// </summary>
[System.Text.Json.Serialization.JsonSerializable(typeof(HistoryState))]
internal sealed partial class HistoryJsonContext : System.Text.Json.Serialization.JsonSerializerContext
{
}
