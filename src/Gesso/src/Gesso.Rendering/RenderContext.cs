namespace Gesso.Rendering;

/// <summary>
/// Provides context for rendering operations.
/// </summary>
public sealed class RenderContext : IDisposable
{
    private bool _disposed;

    public int Width { get; }
    public int Height { get; }
    public float Zoom { get; set; } = 1.0f;
    public float PanX { get; set; }
    public float PanY { get; set; }

    public RenderContext(int width, int height)
    {
        Width = width;
        Height = height;
    }

    public (float X, float Y) ScreenToCanvas(float screenX, float screenY)
    {
        var canvasX = (screenX - PanX) / Zoom;
        var canvasY = (screenY - PanY) / Zoom;
        return (canvasX, canvasY);
    }

    public (float X, float Y) CanvasToScreen(float canvasX, float canvasY)
    {
        var screenX = (canvasX * Zoom) + PanX;
        var screenY = (canvasY * Zoom) + PanY;
        return (screenX, screenY);
    }

    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        _disposed = true;
    }
}
