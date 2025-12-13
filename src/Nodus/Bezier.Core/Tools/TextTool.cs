namespace Bezier.Core.Tools;

using Bezier.Core.Commands;
using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Models.Fills;

/// <summary>
/// Tool for creating and editing text elements.
/// </summary>
public class TextTool : ToolBase
{
    private SvgText? _activeText;
    private bool _isEditing;
    private string _editBuffer = string.Empty;
    private int _cursorPosition;
    private int _selectionStart = -1;
    private int _selectionEnd = -1;

    /// <inheritdoc/>
    public override string Name => "Text";

    /// <inheritdoc/>
    public override string Icon => "TextFont";

    /// <inheritdoc/>
    public override ToolCursor Cursor => ToolCursor.Text;

    /// <inheritdoc/>
    public override string? Shortcut => "T";

    /// <summary>
    /// Gets or sets the default font family.
    /// </summary>
    public string DefaultFontFamily { get; set; } = "Arial";

    /// <summary>
    /// Gets or sets the default font size.
    /// </summary>
    public double DefaultFontSize { get; set; } = 24;

    /// <summary>
    /// Gets or sets the default font weight (100-900).
    /// </summary>
    public int DefaultFontWeight { get; set; } = 400;

    /// <summary>
    /// Gets or sets whether text is italic by default.
    /// </summary>
    public bool DefaultItalic { get; set; } = false;

    /// <summary>
    /// Gets or sets the default text anchor.
    /// </summary>
    public TextAnchor DefaultTextAnchor { get; set; } = TextAnchor.Start;

    /// <summary>
    /// Gets or sets the default fill color for text.
    /// </summary>
    public uint DefaultFillColor { get; set; } = 0xFFCDD6F4;

    /// <summary>
    /// Gets the currently active text element being edited.
    /// </summary>
    public SvgText? ActiveText => _activeText;

    /// <summary>
    /// Gets whether text is currently being edited.
    /// </summary>
    public bool IsEditing => _isEditing;

    /// <summary>
    /// Event raised when editing state changes.
    /// </summary>
    public event EventHandler<bool>? EditingStateChanged;

    /// <summary>
    /// Event raised when the text content changes.
    /// </summary>
    public event EventHandler? TextChanged;

    /// <inheritdoc/>
    public override void OnActivate()
    {
        base.OnActivate();
        EndEditing(false);
    }

    /// <inheritdoc/>
    public override void OnDeactivate()
    {
        base.OnDeactivate();
        EndEditing(true);
    }

    /// <inheritdoc/>
    public override bool OnMouseDown(ToolPoint point, KeyModifiers modifiers)
    {
        base.OnMouseDown(point, modifiers);

        if (Document is null) return false;

        // If already editing, check if clicking on the same text or elsewhere
        if (_isEditing && _activeText != null)
        {
            // Check if clicking inside the active text bounds
            var bounds = _activeText.GetBoundingBox();
            if (point.X >= bounds.X && point.X <= bounds.X + bounds.Width &&
                point.Y >= bounds.Y && point.Y <= bounds.Y + bounds.Height)
            {
                // Clicked inside - update cursor position
                UpdateCursorFromClick(point);
                return true;
            }
            else
            {
                // Clicked outside - finish editing and create new text
                EndEditing(true);
            }
        }

        // Check if clicking on an existing text element
        var hitText = HitTestText(point.X, point.Y);
        if (hitText != null)
        {
            StartEditing(hitText);
            return true;
        }

        // Create new text at click position
        CreateNewText(point.X, point.Y);
        return true;
    }

    /// <inheritdoc/>
    public override bool OnKeyDown(string key, KeyModifiers modifiers)
    {
        if (!_isEditing || _activeText is null) return false;

        switch (key)
        {
            case "Escape":
                EndEditing(false);
                return true;

            case "Enter":
                if (modifiers.HasFlag(KeyModifiers.Shift))
                {
                    // Shift+Enter: Insert newline
                    InsertText("\n");
                }
                else
                {
                    // Enter: Finish editing
                    EndEditing(true);
                }
                return true;

            case "Back":
            case "Backspace":
                if (HasSelection())
                {
                    DeleteSelection();
                }
                else if (_cursorPosition > 0)
                {
                    _editBuffer = _editBuffer.Remove(_cursorPosition - 1, 1);
                    _cursorPosition--;
                    UpdateTextContent();
                }
                return true;

            case "Delete":
                if (HasSelection())
                {
                    DeleteSelection();
                }
                else if (_cursorPosition < _editBuffer.Length)
                {
                    _editBuffer = _editBuffer.Remove(_cursorPosition, 1);
                    UpdateTextContent();
                }
                return true;

            case "Left":
                if (_cursorPosition > 0)
                {
                    _cursorPosition--;
                    if (!modifiers.HasFlag(KeyModifiers.Shift))
                    {
                        ClearSelection();
                    }
                }
                return true;

            case "Right":
                if (_cursorPosition < _editBuffer.Length)
                {
                    _cursorPosition++;
                    if (!modifiers.HasFlag(KeyModifiers.Shift))
                    {
                        ClearSelection();
                    }
                }
                return true;

            case "Home":
                _cursorPosition = 0;
                if (!modifiers.HasFlag(KeyModifiers.Shift))
                {
                    ClearSelection();
                }
                return true;

            case "End":
                _cursorPosition = _editBuffer.Length;
                if (!modifiers.HasFlag(KeyModifiers.Shift))
                {
                    ClearSelection();
                }
                return true;

            case "A":
                if (modifiers.HasFlag(KeyModifiers.Control))
                {
                    // Select all
                    _selectionStart = 0;
                    _selectionEnd = _editBuffer.Length;
                    _cursorPosition = _editBuffer.Length;
                    return true;
                }
                break;

            case "C":
                if (modifiers.HasFlag(KeyModifiers.Control) && HasSelection())
                {
                    // Copy - would need clipboard integration
                    return true;
                }
                break;

            case "V":
                if (modifiers.HasFlag(KeyModifiers.Control))
                {
                    // Paste - would need clipboard integration
                    return true;
                }
                break;

            case "X":
                if (modifiers.HasFlag(KeyModifiers.Control) && HasSelection())
                {
                    // Cut - would need clipboard integration
                    DeleteSelection();
                    return true;
                }
                break;
        }

        // Handle regular character input
        if (key.Length == 1 && !modifiers.HasFlag(KeyModifiers.Control))
        {
            if (HasSelection())
            {
                DeleteSelection();
            }
            InsertText(key);
            return true;
        }

        return false;
    }

    /// <inheritdoc/>
    public override void RenderOverlay(IToolRenderContext context)
    {
        if (!_isEditing || _activeText is null) return;

        const uint cursorColor = 0xFFFFFFFF;
        const uint selectionColor = 0x4089B4FA;

        var bounds = _activeText.GetBoundingBox();
        var x = bounds.X;
        var y = bounds.Y;
        var lineHeight = _activeText.FontSize * 1.2;

        // Draw selection highlight
        if (HasSelection())
        {
            var selStart = Math.Min(_selectionStart, _selectionEnd);
            var selEnd = Math.Max(_selectionStart, _selectionEnd);
            
            // Simplified selection rendering - just highlight the text area
            var charWidth = _activeText.FontSize * 0.6; // Approximate
            var selX = x + selStart * charWidth;
            var selWidth = (selEnd - selStart) * charWidth;
            
            context.DrawRect(selX, y, selWidth, lineHeight, selectionColor, 1f, true);
        }

        // Draw cursor
        var cursorX = x + _cursorPosition * (_activeText.FontSize * 0.6);
        context.DrawLine(cursorX, y, cursorX, y + lineHeight, cursorColor, 2f);

        // Draw text bounds
        context.DrawRect(bounds.X - 2, bounds.Y - 2, bounds.Width + 4, bounds.Height + 4, 0x4089B4FA, 1f, false);
    }

    private void CreateNewText(double x, double y)
    {
        _activeText = new SvgText
        {
            X = x,
            Y = y,
            Text = "",
            FontFamily = DefaultFontFamily,
            FontSize = DefaultFontSize,
            FontWeight = DefaultFontWeight,
            Italic = DefaultItalic,
            TextAnchor = DefaultTextAnchor,
            Fill = new SolidFill { Color = DefaultFillColor },
            Name = GenerateName()
        };

        _editBuffer = string.Empty;
        _cursorPosition = 0;
        _isEditing = true;
        ClearSelection();

        EditingStateChanged?.Invoke(this, true);
    }

    private void StartEditing(SvgText text)
    {
        _activeText = text;
        _editBuffer = text.Text ?? string.Empty;
        _cursorPosition = _editBuffer.Length;
        _isEditing = true;
        ClearSelection();

        EditingStateChanged?.Invoke(this, true);
    }

    private void EndEditing(bool save)
    {
        if (!_isEditing) return;

        if (save && _activeText != null && Document != null)
        {
            if (!string.IsNullOrEmpty(_editBuffer))
            {
                _activeText.Text = _editBuffer;
                
                // If this is a new text element, add it to the document
                if (!Document.Elements.Contains(_activeText))
                {
                    var command = new AddElementCommand(Document, _activeText);
                    History?.ExecuteCommand(command);
                }
            }
        }

        _activeText = null;
        _editBuffer = string.Empty;
        _cursorPosition = 0;
        _isEditing = false;
        ClearSelection();

        EditingStateChanged?.Invoke(this, false);
    }

    private void InsertText(string text)
    {
        _editBuffer = _editBuffer.Insert(_cursorPosition, text);
        _cursorPosition += text.Length;
        UpdateTextContent();
    }

    private void UpdateTextContent()
    {
        if (_activeText != null)
        {
            _activeText.Text = _editBuffer;
            TextChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    private void DeleteSelection()
    {
        if (!HasSelection()) return;

        var start = Math.Min(_selectionStart, _selectionEnd);
        var length = Math.Abs(_selectionEnd - _selectionStart);
        
        _editBuffer = _editBuffer.Remove(start, length);
        _cursorPosition = start;
        ClearSelection();
        UpdateTextContent();
    }

    private bool HasSelection()
    {
        return _selectionStart >= 0 && _selectionEnd >= 0 && _selectionStart != _selectionEnd;
    }

    private void ClearSelection()
    {
        _selectionStart = -1;
        _selectionEnd = -1;
    }

    private void UpdateCursorFromClick(ToolPoint point)
    {
        if (_activeText is null) return;

        var bounds = _activeText.GetBoundingBox();
        var charWidth = _activeText.FontSize * 0.6; // Approximate character width
        var relativeX = point.X - bounds.X;
        
        _cursorPosition = Math.Max(0, Math.Min(_editBuffer.Length, (int)(relativeX / charWidth)));
        ClearSelection();
    }

    private SvgText? HitTestText(double x, double y)
    {
        if (Document is null) return null;

        foreach (var element in Document.Elements)
        {
            if (element is SvgText text)
            {
                var bounds = text.GetBoundingBox();
                // Add some padding for easier clicking
                if (x >= bounds.X - 5 && x <= bounds.X + bounds.Width + 5 &&
                    y >= bounds.Y - 5 && y <= bounds.Y + bounds.Height + 5)
                {
                    return text;
                }
            }
        }

        return null;
    }

    private string GenerateName()
    {
        return $"Text {DateTime.Now:HHmmss}";
    }

    /// <summary>
    /// Gets the current cursor position.
    /// </summary>
    public int CursorPosition => _cursorPosition;

    /// <summary>
    /// Gets the current edit buffer content.
    /// </summary>
    public string EditBuffer => _editBuffer;
}
