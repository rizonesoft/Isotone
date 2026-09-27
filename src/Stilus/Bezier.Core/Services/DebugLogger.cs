using System.Collections.Concurrent;

namespace Bezier.Core.Services;

/// <summary>
/// In-memory debug logger for troubleshooting when console is unavailable.
/// Thread-safe circular buffer that stores recent log entries.
/// </summary>
public sealed class DebugLogger
{
    private static readonly Lazy<DebugLogger> _instance = new(() => new DebugLogger());
    private readonly ConcurrentQueue<LogEntry> _entries = new();
    private const int MaxEntries = 500;

    /// <summary>
    /// Gets the singleton instance.
    /// </summary>
    public static DebugLogger Instance => _instance.Value;

    /// <summary>
    /// Event raised when a new log entry is added.
    /// </summary>
    public event EventHandler<LogEntry>? LogAdded;

    /// <summary>
    /// Gets all current log entries.
    /// </summary>
    public IReadOnlyList<LogEntry> Entries => [.. _entries];

    /// <summary>
    /// Whether debug logging is enabled.
    /// </summary>
    public bool IsEnabled { get; set; } = true;

    private DebugLogger() { }

    /// <summary>
    /// Logs a debug message.
    /// </summary>
    public void Log(string category, string message)
    {
        if (!IsEnabled) return;

        var entry = new LogEntry(DateTime.Now, LogLevel.Debug, category, message);
        AddEntry(entry);
    }

    /// <summary>
    /// Logs an info message.
    /// </summary>
    public void Info(string category, string message)
    {
        if (!IsEnabled) return;

        var entry = new LogEntry(DateTime.Now, LogLevel.Info, category, message);
        AddEntry(entry);
    }

    /// <summary>
    /// Logs a warning message.
    /// </summary>
    public void Warn(string category, string message)
    {
        if (!IsEnabled) return;

        var entry = new LogEntry(DateTime.Now, LogLevel.Warning, category, message);
        AddEntry(entry);
    }

    /// <summary>
    /// Logs an error message.
    /// </summary>
    public void Error(string category, string message, Exception? ex = null)
    {
        if (!IsEnabled) return;

        var fullMessage = ex is not null ? $"{message}: {ex.Message}" : message;
        var entry = new LogEntry(DateTime.Now, LogLevel.Error, category, fullMessage);
        AddEntry(entry);
    }

    /// <summary>
    /// Logs hit test information for debugging selection issues.
    /// </summary>
    public void LogHitTest(string elementType, double clickX, double clickY, 
        (double X, double Y, double Width, double Height) bounds, bool hit)
    {
        if (!IsEnabled) return;

        var message = $"HitTest {elementType}: click=({clickX:F1},{clickY:F1}) " +
                      $"bounds=({bounds.X:F1},{bounds.Y:F1},{bounds.Width:F1}x{bounds.Height:F1}) " +
                      $"-> {(hit ? "HIT" : "miss")}";
        Log("Selection", message);
    }

    /// <summary>
    /// Clears all log entries.
    /// </summary>
    public void Clear()
    {
        while (_entries.TryDequeue(out _)) { }
    }

    /// <summary>
    /// Gets log entries filtered by category.
    /// </summary>
    public IEnumerable<LogEntry> GetByCategory(string category)
    {
        return _entries.Where(e => e.Category.Equals(category, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Gets log entries filtered by level.
    /// </summary>
    public IEnumerable<LogEntry> GetByLevel(LogLevel minLevel)
    {
        return _entries.Where(e => e.Level >= minLevel);
    }

    /// <summary>
    /// Exports all logs as formatted text.
    /// </summary>
    public string Export()
    {
        return string.Join(Environment.NewLine, 
            _entries.Select(e => $"[{e.Timestamp:HH:mm:ss.fff}] [{e.Level}] [{e.Category}] {e.Message}"));
    }

    private void AddEntry(LogEntry entry)
    {
        _entries.Enqueue(entry);

        // Trim old entries if over limit
        while (_entries.Count > MaxEntries && _entries.TryDequeue(out _)) { }

        LogAdded?.Invoke(this, entry);
    }
}

/// <summary>
/// Log severity level.
/// </summary>
public enum LogLevel
{
    Debug = 0,
    Info = 1,
    Warning = 2,
    Error = 3
}

/// <summary>
/// A single log entry.
/// </summary>
public record LogEntry(DateTime Timestamp, LogLevel Level, string Category, string Message);
