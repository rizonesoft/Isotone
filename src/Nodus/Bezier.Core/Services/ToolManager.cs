namespace Bezier.Core.Services;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Tools;

/// <summary>
/// Manages the active tool and tool switching.
/// </summary>
public class ToolManager
{
    private readonly List<ITool> _tools = [];
    private ITool? _activeTool;
    private ITool? _previousTool;
    private VectorDocument? _document;
    private HistoryManager? _history;

    /// <summary>
    /// Gets the currently active tool.
    /// </summary>
    public ITool? ActiveTool => _activeTool;

    /// <summary>
    /// Gets the collection of registered tools.
    /// </summary>
    public IReadOnlyList<ITool> Tools => _tools;

    /// <summary>
    /// Event raised when the active tool changes.
    /// </summary>
    public event EventHandler<ITool?>? ActiveToolChanged;

    /// <summary>
    /// Event raised when the cursor should change.
    /// </summary>
    public event EventHandler<ToolCursor>? CursorChanged;

    /// <summary>
    /// Event raised when the canvas should be redrawn.
    /// </summary>
    public event EventHandler? RedrawRequested;

    /// <summary>
    /// Sets the document context for all tools.
    /// </summary>
    public void SetContext(VectorDocument? document, HistoryManager? history)
    {
        _document = document;
        _history = history;

        foreach (var tool in _tools.OfType<ToolBase>())
        {
            tool.SetContext(document, history);
        }
    }

    /// <summary>
    /// Registers a tool with the manager.
    /// </summary>
    public void RegisterTool(ITool tool)
    {
        if (!_tools.Contains(tool))
        {
            _tools.Add(tool);
            
            if (tool is ToolBase toolBase)
            {
                toolBase.SetContext(_document, _history);
            }
        }
    }

    /// <summary>
    /// Sets the active tool.
    /// </summary>
    public void SetTool(ITool? tool)
    {
        if (_activeTool == tool) return;

        _activeTool?.OnDeactivate();
        _previousTool = _activeTool;
        _activeTool = tool;
        _activeTool?.OnActivate();

        CursorChanged?.Invoke(this, _activeTool?.Cursor ?? ToolCursor.Arrow);
        ActiveToolChanged?.Invoke(this, _activeTool);
        RequestRedraw();
    }

    /// <summary>
    /// Sets the active tool by name.
    /// </summary>
    public void SetTool(string name)
    {
        var tool = _tools.FirstOrDefault(t => t.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
        if (tool is not null)
        {
            SetTool(tool);
        }
    }

    /// <summary>
    /// Temporarily switches to a tool and returns to the previous tool on release.
    /// </summary>
    public void PushTool(ITool tool)
    {
        if (_activeTool == tool) return;
        
        _previousTool = _activeTool;
        _activeTool?.OnDeactivate();
        _activeTool = tool;
        _activeTool?.OnActivate();

        CursorChanged?.Invoke(this, _activeTool.Cursor);
        ActiveToolChanged?.Invoke(this, _activeTool);
    }

    /// <summary>
    /// Returns to the previous tool.
    /// </summary>
    public void PopTool()
    {
        if (_previousTool is not null)
        {
            SetTool(_previousTool);
            _previousTool = null;
        }
    }

    /// <summary>
    /// Gets a tool by name.
    /// </summary>
    public ITool? GetTool(string name)
    {
        return _tools.FirstOrDefault(t => t.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Gets a tool by type.
    /// </summary>
    public T? GetTool<T>() where T : class, ITool
    {
        return _tools.OfType<T>().FirstOrDefault();
    }

    /// <summary>
    /// Handles keyboard shortcuts for tool switching.
    /// </summary>
    public bool HandleShortcut(string key)
    {
        var tool = _tools.FirstOrDefault(t => 
            t.Shortcut?.Equals(key, StringComparison.OrdinalIgnoreCase) == true);
        
        if (tool is not null)
        {
            SetTool(tool);
            return true;
        }
        return false;
    }

    /// <summary>
    /// Requests a canvas redraw.
    /// </summary>
    public void RequestRedraw()
    {
        RedrawRequested?.Invoke(this, EventArgs.Empty);
    }

    #region Input Forwarding

    public bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        var handled = _activeTool?.OnMouseDown(point, modifiers) ?? false;
        if (handled) RequestRedraw();
        return handled;
    }

    public bool OnMouseMove(ToolPoint point, KeyModifiers modifiers)
    {
        var handled = _activeTool?.OnMouseMove(point, modifiers) ?? false;
        if (handled) RequestRedraw();
        return handled;
    }

    public bool OnMouseUp(ToolPoint point, KeyModifiers modifiers)
    {
        var handled = _activeTool?.OnMouseUp(point, modifiers) ?? false;
        if (handled) RequestRedraw();
        return handled;
    }

    public bool OnKeyDown(string key, KeyModifiers modifiers)
    {
        return _activeTool?.OnKeyDown(key, modifiers) ?? false;
    }

    public bool OnKeyUp(string key, KeyModifiers modifiers)
    {
        return _activeTool?.OnKeyUp(key, modifiers) ?? false;
    }

    public void RenderOverlay(IToolRenderContext context)
    {
        _activeTool?.RenderOverlay(context);
    }

    #endregion
}
