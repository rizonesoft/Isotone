using Bezier.Core.Models;

namespace Bezier.Core.Services;

/// <summary>
/// Event args for debug info updates.
/// </summary>
public class DebugInfoUpdateEventArgs : EventArgs
{
    public DebugInfoSnapshot Snapshot { get; }
    
    public DebugInfoUpdateEventArgs(DebugInfoSnapshot snapshot)
    {
        Snapshot = snapshot;
    }
}

/// <summary>
/// Snapshot of debug information at a point in time.
/// </summary>
public record DebugInfoSnapshot
{
    // Mouse coordinates
    public double ScreenX { get; init; }
    public double ScreenY { get; init; }
    public double DocumentX { get; init; }
    public double DocumentY { get; init; }
    public double ArtboardX { get; init; }
    public double ArtboardY { get; init; }
    public string? ActiveArtboardName { get; init; }
    
    // Canvas state
    public double ZoomLevel { get; init; }
    public double PanOffsetX { get; init; }
    public double PanOffsetY { get; init; }
    public double ViewportWidth { get; init; }
    public double ViewportHeight { get; init; }
    
    // Selection info
    public int SelectionCount { get; init; }
    public VectorElement? PrimarySelection { get; init; }
    public (double X, double Y, double Width, double Height)? SelectionBounds { get; init; }
    
    public DateTime Timestamp { get; init; } = DateTime.Now;
}

/// <summary>
/// Service that publishes debug information for the Developer Tools window.
/// This acts as a bridge between the editor and the debug window.
/// </summary>
public sealed class DebugInfoService
{
    private static readonly Lazy<DebugInfoService> _instance = new(() => new DebugInfoService());
    
    /// <summary>
    /// Gets the singleton instance.
    /// </summary>
    public static DebugInfoService Instance => _instance.Value;
    
    private DebugInfoSnapshot _currentSnapshot = new();
    
    // Mouse coordinates
    private double _screenX;
    private double _screenY;
    private double _documentX;
    private double _documentY;
    private double _artboardX;
    private double _artboardY;
    private string? _activeArtboardName;
    
    // Canvas state
    private double _zoomLevel = 1.0;
    private double _panOffsetX;
    private double _panOffsetY;
    private double _viewportWidth;
    private double _viewportHeight;
    
    // Selection
    private int _selectionCount;
    private VectorElement? _primarySelection;
    private (double X, double Y, double Width, double Height)? _selectionBounds;
    
    /// <summary>
    /// Event raised when debug info is updated.
    /// </summary>
    public event EventHandler<DebugInfoUpdateEventArgs>? InfoUpdated;
    
    /// <summary>
    /// Event raised when mouse coordinates change.
    /// </summary>
    public event EventHandler? MousePositionChanged;
    
    /// <summary>
    /// Event raised when selection changes.
    /// </summary>
    public event EventHandler? SelectionChanged;
    
    /// <summary>
    /// Event raised when canvas state changes (zoom, pan).
    /// </summary>
    public event EventHandler? CanvasStateChanged;
    
    private DebugInfoService() { }
    
    /// <summary>
    /// Gets the current debug info snapshot.
    /// </summary>
    public DebugInfoSnapshot CurrentSnapshot => _currentSnapshot;
    
    /// <summary>
    /// Updates mouse position information.
    /// </summary>
    public void UpdateMousePosition(double screenX, double screenY, double documentX, double documentY,
        double artboardX = 0, double artboardY = 0, string? artboardName = null)
    {
        _screenX = screenX;
        _screenY = screenY;
        _documentX = documentX;
        _documentY = documentY;
        _artboardX = artboardX;
        _artboardY = artboardY;
        _activeArtboardName = artboardName;
        
        UpdateSnapshot();
        MousePositionChanged?.Invoke(this, EventArgs.Empty);
    }
    
    /// <summary>
    /// Updates canvas state information.
    /// </summary>
    public void UpdateCanvasState(double zoom, double panX, double panY, double viewportWidth, double viewportHeight)
    {
        _zoomLevel = zoom;
        _panOffsetX = panX;
        _panOffsetY = panY;
        _viewportWidth = viewportWidth;
        _viewportHeight = viewportHeight;
        
        UpdateSnapshot();
        CanvasStateChanged?.Invoke(this, EventArgs.Empty);
    }
    
    /// <summary>
    /// Updates selection information.
    /// </summary>
    public void UpdateSelection(int count, VectorElement? primarySelection, 
        (double X, double Y, double Width, double Height)? bounds)
    {
        _selectionCount = count;
        _primarySelection = primarySelection;
        _selectionBounds = bounds;
        
        UpdateSnapshot();
        SelectionChanged?.Invoke(this, EventArgs.Empty);
    }
    
    private void UpdateSnapshot()
    {
        _currentSnapshot = new DebugInfoSnapshot
        {
            ScreenX = _screenX,
            ScreenY = _screenY,
            DocumentX = _documentX,
            DocumentY = _documentY,
            ArtboardX = _artboardX,
            ArtboardY = _artboardY,
            ActiveArtboardName = _activeArtboardName,
            ZoomLevel = _zoomLevel,
            PanOffsetX = _panOffsetX,
            PanOffsetY = _panOffsetY,
            ViewportWidth = _viewportWidth,
            ViewportHeight = _viewportHeight,
            SelectionCount = _selectionCount,
            PrimarySelection = _primarySelection,
            SelectionBounds = _selectionBounds,
            Timestamp = DateTime.Now
        };
        
        InfoUpdated?.Invoke(this, new DebugInfoUpdateEventArgs(_currentSnapshot));
    }
    
    /// <summary>
    /// Formats all current debug info as text for copying.
    /// </summary>
    public string FormatAllInfo()
    {
        var sb = new System.Text.StringBuilder();
        var s = _currentSnapshot;
        
        sb.AppendLine("=== Bezier Debug Info ===");
        sb.AppendLine($"Timestamp: {s.Timestamp:yyyy-MM-dd HH:mm:ss.fff}");
        sb.AppendLine();
        
        sb.AppendLine("--- Mouse Coordinates ---");
        sb.AppendLine($"Screen (WPF):     ({s.ScreenX:F1}, {s.ScreenY:F1})");
        sb.AppendLine($"Document:         ({s.DocumentX:F1}, {s.DocumentY:F1})");
        if (!string.IsNullOrEmpty(s.ActiveArtboardName))
        {
            sb.AppendLine($"Artboard [{s.ActiveArtboardName}]: ({s.ArtboardX:F1}, {s.ArtboardY:F1})");
        }
        sb.AppendLine();
        
        sb.AppendLine("--- Canvas State ---");
        sb.AppendLine($"Zoom:      {s.ZoomLevel * 100:F0}%");
        sb.AppendLine($"Pan:       ({s.PanOffsetX:F1}, {s.PanOffsetY:F1})");
        sb.AppendLine($"Viewport:  {s.ViewportWidth:F0} × {s.ViewportHeight:F0}");
        sb.AppendLine();
        
        sb.AppendLine("--- Selection ---");
        sb.AppendLine($"Count: {s.SelectionCount}");
        
        if (s.PrimarySelection is not null)
        {
            var elem = s.PrimarySelection;
            sb.AppendLine($"Element:   {elem.GetType().Name}");
            sb.AppendLine($"Name:      {elem.Name ?? "(unnamed)"}");
            sb.AppendLine($"ID:        {elem.Id}");
            
            var bounds = elem.GetBoundingBox();
            sb.AppendLine($"Position:  ({bounds.X:F1}, {bounds.Y:F1})");
            sb.AppendLine($"Size:      {bounds.Width:F1} × {bounds.Height:F1}");
            
            var transform = elem.Transform;
            // Calculate rotation from matrix (atan2 of skewY and scaleX)
            var rotationDeg = Math.Atan2(transform.SkewY, transform.ScaleX) * 180.0 / Math.PI;
            sb.AppendLine($"Transform: translate({transform.TranslateX:F1}, {transform.TranslateY:F1}) " +
                          $"scale({transform.ScaleX:F2}, {transform.ScaleY:F2}) " +
                          $"rotate({rotationDeg:F1}°)");
            
            if (elem.Fill is not null)
            {
                sb.AppendLine($"Fill:      {elem.Fill.GetType().Name}");
            }
            if (elem.Stroke is not null)
            {
                sb.AppendLine($"Stroke:    {elem.Stroke.Width}px");
            }
        }
        
        if (s.SelectionBounds is not null)
        {
            var b = s.SelectionBounds.Value;
            sb.AppendLine($"Bounds:    ({b.X:F1}, {b.Y:F1}) - ({b.X + b.Width:F1}, {b.Y + b.Height:F1})");
            sb.AppendLine($"           {b.Width:F1} × {b.Height:F1}");
        }
        
        return sb.ToString();
    }
}

