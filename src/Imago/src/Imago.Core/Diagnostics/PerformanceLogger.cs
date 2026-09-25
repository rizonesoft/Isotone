namespace Imago.Core.Diagnostics;

using System.Diagnostics;
using System.Runtime.CompilerServices;
using Serilog;
using Serilog.Events;

/// <summary>
/// Provides performance logging utilities for measuring operation durations.
/// </summary>
public static class PerformanceLogger
{
    private static readonly ILogger s_logger = Log.ForContext(typeof(PerformanceLogger));

    /// <summary>
    /// Creates a timed operation scope that logs duration on disposal.
    /// </summary>
    /// <param name="operationName">Name of the operation being measured.</param>
    /// <param name="warningThresholdMs">Log as warning if duration exceeds this threshold.</param>
    /// <param name="caller">Auto-populated caller member name.</param>
    /// <returns>A disposable timing scope.</returns>
    public static TimingScope BeginOperation(
        string operationName,
        long warningThresholdMs = 1000,
        [CallerMemberName] string caller = "")
    {
        return new TimingScope(operationName, caller, warningThresholdMs);
    }

    /// <summary>
    /// Creates a timed operation scope with custom logger context.
    /// </summary>
    public static TimingScope BeginOperation<TContext>(
        string operationName,
        long warningThresholdMs = 1000,
        [CallerMemberName] string caller = "")
    {
        return new TimingScope(operationName, caller, warningThresholdMs, typeof(TContext).Name);
    }

    /// <summary>
    /// Measures and logs a synchronous action.
    /// </summary>
    public static void Measure(
        string operationName,
        Action action,
        long warningThresholdMs = 1000,
        [CallerMemberName] string caller = "")
    {
        using var scope = BeginOperation(operationName, warningThresholdMs, caller);
        action();
    }

    /// <summary>
    /// Measures and logs a synchronous function.
    /// </summary>
    public static T Measure<T>(
        string operationName,
        Func<T> func,
        long warningThresholdMs = 1000,
        [CallerMemberName] string caller = "")
    {
        using var scope = BeginOperation(operationName, warningThresholdMs, caller);
        return func();
    }

    /// <summary>
    /// Measures and logs an async operation.
    /// </summary>
    public static async Task MeasureAsync(
        string operationName,
        Func<Task> asyncAction,
        long warningThresholdMs = 1000,
        [CallerMemberName] string caller = "")
    {
        using var scope = BeginOperation(operationName, warningThresholdMs, caller);
        await asyncAction().ConfigureAwait(false);
    }

    /// <summary>
    /// Measures and logs an async function.
    /// </summary>
    public static async Task<T> MeasureAsync<T>(
        string operationName,
        Func<Task<T>> asyncFunc,
        long warningThresholdMs = 1000,
        [CallerMemberName] string caller = "")
    {
        using var scope = BeginOperation(operationName, warningThresholdMs, caller);
        return await asyncFunc().ConfigureAwait(false);
    }

    /// <summary>
    /// A disposable scope that measures and logs operation duration.
    /// </summary>
    public readonly struct TimingScope : IDisposable
    {
        private readonly string _operationName;
        private readonly string _caller;
        private readonly string? _context;
        private readonly long _warningThresholdMs;
        private readonly long _startTimestamp;

        internal TimingScope(string operationName, string caller, long warningThresholdMs, string? context = null)
        {
            _operationName = operationName;
            _caller = caller;
            _context = context;
            _warningThresholdMs = warningThresholdMs;
            _startTimestamp = Stopwatch.GetTimestamp();

            if (s_logger.IsEnabled(LogEventLevel.Debug))
            {
                s_logger.Debug(
                    "[PERF] Starting {Operation} in {Caller}{Context}",
                    _operationName,
                    _caller,
                    _context is not null ? $" ({_context})" : "");
            }
        }

        public void Dispose()
        {
            var elapsed = Stopwatch.GetElapsedTime(_startTimestamp);
            var elapsedMs = elapsed.TotalMilliseconds;

            if (elapsedMs >= _warningThresholdMs)
            {
                s_logger.Warning(
                    "[PERF] {Operation} completed in {ElapsedMs:F2}ms (exceeded threshold of {ThresholdMs}ms) in {Caller}{Context}",
                    _operationName,
                    elapsedMs,
                    _warningThresholdMs,
                    _caller,
                    _context is not null ? $" ({_context})" : "");
            }
            else if (s_logger.IsEnabled(LogEventLevel.Debug))
            {
                s_logger.Debug(
                    "[PERF] {Operation} completed in {ElapsedMs:F2}ms in {Caller}{Context}",
                    _operationName,
                    elapsedMs,
                    _caller,
                    _context is not null ? $" ({_context})" : "");
            }
        }
    }
}
