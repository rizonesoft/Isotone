namespace Bezier.Core.Interfaces;

/// <summary>
/// Represents keyboard modifiers for tool input.
/// </summary>
[Flags]
public enum KeyModifiers
{
    None = 0,
    Shift = 1,
    Control = 2,
    Alt = 4
}

/// <summary>
/// Represents a point in document coordinates.
/// </summary>
public readonly record struct ToolPoint(double X, double Y);

/// <summary>
/// Context provided to tools for rendering overlays.
/// </summary>
public interface IToolRenderContext
{
    void DrawLine(double x1, double y1, double x2, double y2, uint color, float strokeWidth = 1f);
    void DrawRect(double x, double y, double width, double height, uint color, float strokeWidth = 1f, bool fill = false);
    void DrawEllipse(double cx, double cy, double rx, double ry, uint color, float strokeWidth = 1f, bool fill = false);
    void DrawPath(string pathData, uint color, float strokeWidth = 1f, bool fill = false);
    void DrawText(string text, double x, double y, uint color, float fontSize = 12f);
    
    /// <summary>
    /// Renders an element preview with an offset (for drag operations).
    /// </summary>
    /// <param name="element">The element to render.</param>
    /// <param name="offsetX">X offset to apply.</param>
    /// <param name="offsetY">Y offset to apply.</param>
    /// <param name="opacity">Opacity for the preview (0.0 to 1.0).</param>
    void DrawElementPreview(object element, double offsetX, double offsetY, double opacity = 0.5);
}

/// <summary>
/// Represents an editor tool that handles user input and rendering.
/// </summary>
public interface ITool
{
    /// <summary>
    /// Gets the display name of the tool.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets the icon identifier for the tool.
    /// </summary>
    string Icon { get; }

    /// <summary>
    /// Gets the cursor type when this tool is active.
    /// </summary>
    ToolCursor Cursor { get; }

    /// <summary>
    /// Gets the keyboard shortcut for this tool.
    /// </summary>
    string? Shortcut { get; }

    /// <summary>
    /// Called when the tool becomes active.
    /// </summary>
    void OnActivate();

    /// <summary>
    /// Called when the tool is deactivated.
    /// </summary>
    void OnDeactivate();

    /// <summary>
    /// Called when the mouse button is pressed.
    /// </summary>
    /// <param name="point">Position in document coordinates.</param>
    /// <param name="modifiers">Active keyboard modifiers.</param>
    /// <returns>True if the event was handled.</returns>
    bool OnMouseDown(ToolPoint point, KeyModifiers modifiers);

    /// <summary>
    /// Called when the mouse is moved.
    /// </summary>
    /// <param name="point">Position in document coordinates.</param>
    /// <param name="modifiers">Active keyboard modifiers.</param>
    /// <returns>True if the event was handled.</returns>
    bool OnMouseMove(ToolPoint point, KeyModifiers modifiers);

    /// <summary>
    /// Called when the mouse button is released.
    /// </summary>
    /// <param name="point">Position in document coordinates.</param>
    /// <param name="modifiers">Active keyboard modifiers.</param>
    /// <returns>True if the event was handled.</returns>
    bool OnMouseUp(ToolPoint point, KeyModifiers modifiers);

    /// <summary>
    /// Called when a key is pressed.
    /// </summary>
    /// <param name="key">The key that was pressed.</param>
    /// <param name="modifiers">Active keyboard modifiers.</param>
    /// <returns>True if the event was handled.</returns>
    bool OnKeyDown(string key, KeyModifiers modifiers);

    /// <summary>
    /// Called when a key is released.
    /// </summary>
    /// <param name="key">The key that was released.</param>
    /// <param name="modifiers">Active keyboard modifiers.</param>
    /// <returns>True if the event was handled.</returns>
    bool OnKeyUp(string key, KeyModifiers modifiers);

    /// <summary>
    /// Renders tool-specific overlay graphics (guides, handles, selection box, etc.).
    /// </summary>
    /// <param name="context">The render context for drawing.</param>
    void RenderOverlay(IToolRenderContext context);
}

/// <summary>
/// Cursor types for tools.
/// </summary>
public enum ToolCursor
{
    Arrow,
    Cross,
    Hand,
    Move,
    SizeNWSE,
    SizeNESW,
    SizeWE,
    SizeNS,
    Text,
    Pen,
    Eyedropper,
    ZoomIn,
    ZoomOut,
    None
}
