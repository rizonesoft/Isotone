using System.Diagnostics;

namespace Bezier.Core.Services;

/// <summary>
/// Snapshot of performance metrics at a point in time.
/// </summary>
public record PerformanceSnapshot
{
    /// <summary>Current frames per second.</summary>
    public double Fps { get; init; }
    
    /// <summary>Average FPS over the sample period.</summary>
    public double AverageFps { get; init; }
    
    /// <summary>Minimum FPS recorded.</summary>
    public double MinFps { get; init; }
    
    /// <summary>Maximum FPS recorded.</summary>
    public double MaxFps { get; init; }
    
    /// <summary>Last frame render time in milliseconds.</summary>
    public double LastRenderTimeMs { get; init; }
    
    /// <summary>Average render time in milliseconds.</summary>
    public double AverageRenderTimeMs { get; init; }
    
    /// <summary>Maximum render time in milliseconds.</summary>
    public double MaxRenderTimeMs { get; init; }
    
    /// <summary>Total frames rendered.</summary>
    public long TotalFrames { get; init; }
    
    /// <summary>Memory used by the process in bytes.</summary>
    public long MemoryUsedBytes { get; init; }
    
    /// <summary>GC memory in bytes.</summary>
    public long GcMemoryBytes { get; init; }
    
    /// <summary>Number of elements in the document.</summary>
    public int ElementCount { get; init; }
    
    /// <summary>Number of commands in the undo stack.</summary>
    public int UndoStackSize { get; init; }
    
    /// <summary>Number of commands in the redo stack.</summary>
    public int RedoStackSize { get; init; }
    
    /// <summary>Timestamp of this snapshot.</summary>
    public DateTime Timestamp { get; init; } = DateTime.Now;
}

/// <summary>
/// Service that collects and publishes performance metrics.
/// </summary>
public sealed class PerformanceMetricsService
{
    private static readonly Lazy<PerformanceMetricsService> _instance = new(() => new PerformanceMetricsService());
    
    /// <summary>Gets the singleton instance.</summary>
    public static PerformanceMetricsService Instance => _instance.Value;
    
    private readonly Stopwatch _frameTimer = new();
    private readonly Queue<double> _frameTimes = new();
    private readonly Queue<double> _renderTimes = new();
    private const int SampleSize = 60; // Keep last 60 frames for averaging
    
    private long _totalFrames;
    private double _lastRenderTimeMs;
    private double _maxRenderTimeMs;
    private double _minFps = double.MaxValue;
    private double _maxFps;
    private int _elementCount;
    private int _undoStackSize;
    private int _redoStackSize;
    
    private PerformanceSnapshot _currentSnapshot = new();
    
    /// <summary>Event raised when metrics are updated.</summary>
    public event EventHandler<PerformanceSnapshot>? MetricsUpdated;
    
    private PerformanceMetricsService()
    {
        _frameTimer.Start();
    }
    
    /// <summary>Gets the current performance snapshot.</summary>
    public PerformanceSnapshot CurrentSnapshot => _currentSnapshot;
    
    /// <summary>
    /// Call this at the start of each render frame.
    /// </summary>
    public void BeginFrame()
    {
        _frameTimer.Restart();
    }
    
    /// <summary>
    /// Call this at the end of each render frame.
    /// </summary>
    public void EndFrame()
    {
        var frameTime = _frameTimer.Elapsed.TotalMilliseconds;
        _lastRenderTimeMs = frameTime;
        _totalFrames++;
        
        // Track render times
        _renderTimes.Enqueue(frameTime);
        if (_renderTimes.Count > SampleSize)
            _renderTimes.Dequeue();
        
        if (frameTime > _maxRenderTimeMs)
            _maxRenderTimeMs = frameTime;
        
        // Calculate FPS from frame time
        var fps = frameTime > 0 ? 1000.0 / frameTime : 0;
        _frameTimes.Enqueue(fps);
        if (_frameTimes.Count > SampleSize)
            _frameTimes.Dequeue();
        
        if (fps < _minFps && fps > 0)
            _minFps = fps;
        if (fps > _maxFps)
            _maxFps = fps;
        
        UpdateSnapshot();
    }
    
    /// <summary>
    /// Records the render time for a frame (alternative to Begin/EndFrame).
    /// </summary>
    public void RecordRenderTime(double milliseconds)
    {
        _lastRenderTimeMs = milliseconds;
        _totalFrames++;
        
        _renderTimes.Enqueue(milliseconds);
        if (_renderTimes.Count > SampleSize)
            _renderTimes.Dequeue();
        
        if (milliseconds > _maxRenderTimeMs)
            _maxRenderTimeMs = milliseconds;
        
        var fps = milliseconds > 0 ? 1000.0 / milliseconds : 0;
        _frameTimes.Enqueue(fps);
        if (_frameTimes.Count > SampleSize)
            _frameTimes.Dequeue();
        
        if (fps < _minFps && fps > 0)
            _minFps = fps;
        if (fps > _maxFps)
            _maxFps = fps;
        
        UpdateSnapshot();
    }
    
    /// <summary>
    /// Updates element count.
    /// </summary>
    public void UpdateElementCount(int count)
    {
        _elementCount = count;
        UpdateSnapshot();
    }
    
    /// <summary>
    /// Updates undo/redo stack sizes.
    /// </summary>
    public void UpdateHistoryInfo(int undoCount, int redoCount)
    {
        _undoStackSize = undoCount;
        _redoStackSize = redoCount;
        UpdateSnapshot();
    }
    
    /// <summary>
    /// Resets all metrics.
    /// </summary>
    public void Reset()
    {
        _totalFrames = 0;
        _lastRenderTimeMs = 0;
        _maxRenderTimeMs = 0;
        _minFps = double.MaxValue;
        _maxFps = 0;
        _frameTimes.Clear();
        _renderTimes.Clear();
        UpdateSnapshot();
    }
    
    private void UpdateSnapshot()
    {
        var avgFps = _frameTimes.Count > 0 ? _frameTimes.Average() : 0;
        var avgRenderTime = _renderTimes.Count > 0 ? _renderTimes.Average() : 0;
        var currentFps = _frameTimes.Count > 0 ? _frameTimes.LastOrDefault() : 0;
        
        // Get memory info
        var process = Process.GetCurrentProcess();
        var memoryUsed = process.WorkingSet64;
        var gcMemory = GC.GetTotalMemory(false);
        
        _currentSnapshot = new PerformanceSnapshot
        {
            Fps = currentFps,
            AverageFps = avgFps,
            MinFps = _minFps == double.MaxValue ? 0 : _minFps,
            MaxFps = _maxFps,
            LastRenderTimeMs = _lastRenderTimeMs,
            AverageRenderTimeMs = avgRenderTime,
            MaxRenderTimeMs = _maxRenderTimeMs,
            TotalFrames = _totalFrames,
            MemoryUsedBytes = memoryUsed,
            GcMemoryBytes = gcMemory,
            ElementCount = _elementCount,
            UndoStackSize = _undoStackSize,
            RedoStackSize = _redoStackSize,
            Timestamp = DateTime.Now
        };
        
        MetricsUpdated?.Invoke(this, _currentSnapshot);
    }
    
    /// <summary>
    /// Formats a byte count as a human-readable string.
    /// </summary>
    public static string FormatBytes(long bytes)
    {
        const long KB = 1024;
        const long MB = KB * 1024;
        const long GB = MB * 1024;
        
        return bytes switch
        {
            >= GB => $"{bytes / (double)GB:F2} GB",
            >= MB => $"{bytes / (double)MB:F1} MB",
            >= KB => $"{bytes / (double)KB:F1} KB",
            _ => $"{bytes} B"
        };
    }
    
    /// <summary>
    /// Formats all performance info as text for copying.
    /// </summary>
    public string FormatAllInfo()
    {
        var s = _currentSnapshot;
        var sb = new System.Text.StringBuilder();
        
        sb.AppendLine("=== Bezier Performance Metrics ===");
        sb.AppendLine($"Timestamp: {s.Timestamp:yyyy-MM-dd HH:mm:ss.fff}");
        sb.AppendLine();
        
        sb.AppendLine("--- Frame Rate ---");
        sb.AppendLine($"Current FPS:  {s.Fps:F1}");
        sb.AppendLine($"Average FPS:  {s.AverageFps:F1}");
        sb.AppendLine($"Min FPS:      {s.MinFps:F1}");
        sb.AppendLine($"Max FPS:      {s.MaxFps:F1}");
        sb.AppendLine($"Total Frames: {s.TotalFrames:N0}");
        sb.AppendLine();
        
        sb.AppendLine("--- Render Time ---");
        sb.AppendLine($"Last:    {s.LastRenderTimeMs:F2} ms");
        sb.AppendLine($"Average: {s.AverageRenderTimeMs:F2} ms");
        sb.AppendLine($"Max:     {s.MaxRenderTimeMs:F2} ms");
        sb.AppendLine();
        
        sb.AppendLine("--- Memory ---");
        sb.AppendLine($"Process:    {FormatBytes(s.MemoryUsedBytes)}");
        sb.AppendLine($"GC Managed: {FormatBytes(s.GcMemoryBytes)}");
        sb.AppendLine();
        
        sb.AppendLine("--- Document ---");
        sb.AppendLine($"Elements:   {s.ElementCount}");
        sb.AppendLine($"Undo Stack: {s.UndoStackSize}");
        sb.AppendLine($"Redo Stack: {s.RedoStackSize}");
        
        return sb.ToString();
    }
}

