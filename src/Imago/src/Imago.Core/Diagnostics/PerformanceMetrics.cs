namespace Imago.Core.Diagnostics;

using System.Collections.Concurrent;
using System.Diagnostics;
using Serilog;

/// <summary>
/// Collects and reports aggregate performance metrics.
/// </summary>
public sealed class PerformanceMetrics
{
    private static readonly ILogger s_logger = Log.ForContext<PerformanceMetrics>();
    private static readonly Lazy<PerformanceMetrics> s_instance = new(() => new PerformanceMetrics());

    private readonly ConcurrentDictionary<string, OperationStats> _stats = new();

    /// <summary>
    /// Gets the singleton instance.
    /// </summary>
    public static PerformanceMetrics Instance => s_instance.Value;

    private PerformanceMetrics() { }

    /// <summary>
    /// Records an operation duration.
    /// </summary>
    public void Record(string operationName, TimeSpan duration)
    {
        _stats.AddOrUpdate(
            operationName,
            _ => new OperationStats(duration),
            (_, existing) => existing.Add(duration));
    }

    /// <summary>
    /// Records an operation duration in milliseconds.
    /// </summary>
    public void Record(string operationName, double milliseconds)
    {
        Record(operationName, TimeSpan.FromMilliseconds(milliseconds));
    }

    /// <summary>
    /// Gets statistics for a specific operation.
    /// </summary>
    public OperationStats? GetStats(string operationName)
    {
        return _stats.TryGetValue(operationName, out var stats) ? stats : null;
    }

    /// <summary>
    /// Logs a summary of all collected metrics.
    /// </summary>
    public void LogSummary()
    {
        s_logger.Information("[PERF] === Performance Metrics Summary ===");

        foreach (var (name, stats) in _stats.OrderByDescending(x => x.Value.TotalTime))
        {
            s_logger.Information(
                "[PERF] {Operation}: Count={Count}, Total={TotalMs:F2}ms, Avg={AvgMs:F2}ms, Min={MinMs:F2}ms, Max={MaxMs:F2}ms",
                name,
                stats.Count,
                stats.TotalTime.TotalMilliseconds,
                stats.AverageTime.TotalMilliseconds,
                stats.MinTime.TotalMilliseconds,
                stats.MaxTime.TotalMilliseconds);
        }
    }

    /// <summary>
    /// Clears all collected metrics.
    /// </summary>
    public void Clear()
    {
        _stats.Clear();
    }

    /// <summary>
    /// Statistics for a single operation type.
    /// </summary>
    public sealed class OperationStats
    {
        private readonly object _lock = new();
        private TimeSpan _totalTime;
        private TimeSpan _minTime;
        private TimeSpan _maxTime;
        private long _count;

        public long Count => Volatile.Read(ref _count);
        public TimeSpan TotalTime { get { lock (_lock) return _totalTime; } }
        public TimeSpan MinTime { get { lock (_lock) return _minTime; } }
        public TimeSpan MaxTime { get { lock (_lock) return _maxTime; } }
        public TimeSpan AverageTime => Count > 0 ? TotalTime / Count : TimeSpan.Zero;

        internal OperationStats(TimeSpan initialDuration)
        {
            _totalTime = initialDuration;
            _minTime = initialDuration;
            _maxTime = initialDuration;
            _count = 1;
        }

        internal OperationStats Add(TimeSpan duration)
        {
            lock (_lock)
            {
                _totalTime += duration;
                if (duration < _minTime) _minTime = duration;
                if (duration > _maxTime) _maxTime = duration;
                Interlocked.Increment(ref _count);
            }
            return this;
        }
    }
}
