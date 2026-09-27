using System.ComponentModel;
using System.Text;
using System.Xml;

namespace Bezier.Core.Services;

/// <summary>
/// Editor theme options.
/// </summary>
public enum CodeEditorTheme
{
    Light,
    Dark,
    HighContrast
}

/// <summary>
/// Represents a code editor error/warning marker.
/// </summary>
public class CodeMarker
{
    public int StartLine { get; init; }
    public int StartColumn { get; init; }
    public int EndLine { get; init; }
    public int EndColumn { get; init; }
    public string Message { get; init; } = string.Empty;
    public CodeMarkerSeverity Severity { get; init; }
}

/// <summary>
/// Severity of a code marker.
/// </summary>
public enum CodeMarkerSeverity
{
    Hint,
    Info,
    Warning,
    Error
}

/// <summary>
/// Configuration for the code editor.
/// </summary>
public class CodeEditorConfig
{
    public CodeEditorTheme Theme { get; set; } = CodeEditorTheme.Dark;
    public bool ShowLineNumbers { get; set; } = true;
    public bool ShowMinimap { get; set; } = true;
    public bool EnableFolding { get; set; } = true;
    public bool WordWrap { get; set; } = false;
    public int TabSize { get; set; } = 2;
    public bool InsertSpaces { get; set; } = true;
    public string FontFamily { get; set; } = "Cascadia Code, Consolas, monospace";
    public int FontSize { get; set; } = 14;
    public bool ReadOnly { get; set; } = false;
    public int DebounceDurationMs { get; set; } = 300;
}

/// <summary>
/// Event args for content changed events.
/// </summary>
public class ContentChangedEventArgs : EventArgs
{
    public string Content { get; }
    public bool IsUserChange { get; }

    public ContentChangedEventArgs(string content, bool isUserChange = true)
    {
        Content = content;
        IsUserChange = isUserChange;
    }
}

/// <summary>
/// Event args for cursor position changed events.
/// </summary>
public class CursorPositionChangedEventArgs : EventArgs
{
    public int Line { get; }
    public int Column { get; }

    public CursorPositionChangedEventArgs(int line, int column)
    {
        Line = line;
        Column = column;
    }
}

/// <summary>
/// Event args for element hover events.
/// </summary>
public class ElementHoverEventArgs : EventArgs
{
    public string? ElementId { get; }
    public int Line { get; }
    public int Column { get; }

    public ElementHoverEventArgs(string? elementId, int line, int column)
    {
        ElementId = elementId;
        Line = line;
        Column = column;
    }
}

/// <summary>
/// Service for managing code editor functionality.
/// </summary>
public class CodeEditorService : INotifyPropertyChanged
{
    private string _content = string.Empty;
    private bool _isDirty;
    private bool _isSyncLocked;
    private readonly List<CodeMarker> _markers = [];
    private DateTime _lastChangeTime = DateTime.MinValue;
    private readonly CodeEditorConfig _config = new();

    public event PropertyChangedEventHandler? PropertyChanged;
    public event EventHandler<ContentChangedEventArgs>? ContentChanged;
    public event EventHandler<CursorPositionChangedEventArgs>? CursorPositionChanged;
    public event EventHandler<ElementHoverEventArgs>? ElementHovered;
    public event EventHandler<IReadOnlyList<CodeMarker>>? MarkersChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets the editor configuration.
    /// </summary>
    public CodeEditorConfig Config => _config;

    /// <summary>
    /// Gets or sets the content.
    /// </summary>
    public string Content
    {
        get => _content;
        set
        {
            if (_content != value)
            {
                _content = value;
                _isDirty = true;
                _lastChangeTime = DateTime.UtcNow;
                OnPropertyChanged(nameof(Content));
                OnPropertyChanged(nameof(IsDirty));
            }
        }
    }

    /// <summary>
    /// Gets whether the content has unsaved changes.
    /// </summary>
    public bool IsDirty
    {
        get => _isDirty;
        private set { _isDirty = value; OnPropertyChanged(nameof(IsDirty)); }
    }

    /// <summary>
    /// Gets or sets whether sync is locked (e.g., during drag operations).
    /// </summary>
    public bool IsSyncLocked
    {
        get => _isSyncLocked;
        set { _isSyncLocked = value; OnPropertyChanged(nameof(IsSyncLocked)); }
    }

    /// <summary>
    /// Gets the current markers.
    /// </summary>
    public IReadOnlyList<CodeMarker> Markers => _markers;

    /// <summary>
    /// Sets the content from an external source (e.g., canvas sync).
    /// </summary>
    public void SetContent(string content, bool notifyChange = true)
    {
        if (_isSyncLocked) return;

        _content = content;
        OnPropertyChanged(nameof(Content));

        if (notifyChange)
        {
            ContentChanged?.Invoke(this, new ContentChangedEventArgs(content, false));
        }

        ValidateContent();
    }

    /// <summary>
    /// Gets the current content.
    /// </summary>
    public string GetContent() => _content;

    /// <summary>
    /// Notifies that content was changed by user.
    /// </summary>
    public void NotifyUserContentChanged(string content)
    {
        _content = content;
        _isDirty = true;
        _lastChangeTime = DateTime.UtcNow;
        OnPropertyChanged(nameof(Content));
        OnPropertyChanged(nameof(IsDirty));
        ContentChanged?.Invoke(this, new ContentChangedEventArgs(content, true));
        ValidateContent();
    }

    /// <summary>
    /// Notifies cursor position changed.
    /// </summary>
    public void NotifyCursorPositionChanged(int line, int column)
    {
        CursorPositionChanged?.Invoke(this, new CursorPositionChangedEventArgs(line, column));
    }

    /// <summary>
    /// Notifies element hover.
    /// </summary>
    public void NotifyElementHovered(string? elementId, int line, int column)
    {
        ElementHovered?.Invoke(this, new ElementHoverEventArgs(elementId, line, column));
    }

    /// <summary>
    /// Marks content as saved.
    /// </summary>
    public void MarkAsSaved()
    {
        IsDirty = false;
    }

    /// <summary>
    /// Validates the content and updates markers.
    /// </summary>
    public void ValidateContent()
    {
        _markers.Clear();

        if (string.IsNullOrWhiteSpace(_content))
        {
            MarkersChanged?.Invoke(this, _markers);
            return;
        }

        try
        {
            var settings = new XmlReaderSettings
            {
                ValidationType = ValidationType.None,
                DtdProcessing = DtdProcessing.Ignore
            };

            using var reader = XmlReader.Create(new StringReader(_content), settings);
            while (reader.Read()) { }
        }
        catch (XmlException ex)
        {
            _markers.Add(new CodeMarker
            {
                StartLine = ex.LineNumber,
                StartColumn = ex.LinePosition,
                EndLine = ex.LineNumber,
                EndColumn = ex.LinePosition + 1,
                Message = ex.Message,
                Severity = CodeMarkerSeverity.Error
            });
        }

        MarkersChanged?.Invoke(this, _markers);
    }

    /// <summary>
    /// Formats/prettifies the SVG content.
    /// </summary>
    public string FormatContent()
    {
        if (string.IsNullOrWhiteSpace(_content))
            return _content;

        try
        {
            var doc = new XmlDocument();
            doc.LoadXml(_content);

            var sb = new StringBuilder();
            var settings = new XmlWriterSettings
            {
                Indent = true,
                IndentChars = _config.InsertSpaces ? new string(' ', _config.TabSize) : "\t",
                NewLineChars = "\n",
                NewLineHandling = NewLineHandling.Replace,
                OmitXmlDeclaration = !_content.TrimStart().StartsWith("<?xml")
            };

            using var writer = XmlWriter.Create(sb, settings);
            doc.Save(writer);

            var formatted = sb.ToString();
            SetContent(formatted);
            return formatted;
        }
        catch
        {
            return _content;
        }
    }

    /// <summary>
    /// Gets the line number for an element by ID.
    /// </summary>
    public int? GetLineForElementId(string elementId)
    {
        if (string.IsNullOrWhiteSpace(_content) || string.IsNullOrWhiteSpace(elementId))
            return null;

        var searchPattern = $"id=\"{elementId}\"";
        var lines = _content.Split('\n');

        for (var i = 0; i < lines.Length; i++)
        {
            if (lines[i].Contains(searchPattern, StringComparison.OrdinalIgnoreCase))
                return i + 1;
        }

        return null;
    }

    /// <summary>
    /// Gets the element ID at a specific line.
    /// </summary>
    public string? GetElementIdAtLine(int line)
    {
        if (string.IsNullOrWhiteSpace(_content) || line < 1)
            return null;

        var lines = _content.Split('\n');
        if (line > lines.Length)
            return null;

        // Search backwards from line to find enclosing element with id
        for (var i = line - 1; i >= 0; i--)
        {
            var currentLine = lines[i];
            var idIndex = currentLine.IndexOf("id=\"", StringComparison.OrdinalIgnoreCase);
            if (idIndex >= 0)
            {
                var startQuote = idIndex + 4;
                var endQuote = currentLine.IndexOf('"', startQuote);
                if (endQuote > startQuote)
                {
                    return currentLine[startQuote..endQuote];
                }
            }
        }

        return null;
    }

    /// <summary>
    /// Checks if sync should be performed based on debounce timing.
    /// </summary>
    public bool ShouldSync()
    {
        if (_isSyncLocked) return false;
        var elapsed = (DateTime.UtcNow - _lastChangeTime).TotalMilliseconds;
        return elapsed >= _config.DebounceDurationMs;
    }

    /// <summary>
    /// Gets configuration as JSON for Monaco editor.
    /// </summary>
    public string GetMonacoConfigJson()
    {
        var theme = _config.Theme switch
        {
            CodeEditorTheme.Light => "vs",
            CodeEditorTheme.Dark => "vs-dark",
            CodeEditorTheme.HighContrast => "hc-black",
            _ => "vs-dark"
        };

        return $$"""
        {
            "theme": "{{theme}}",
            "language": "xml",
            "lineNumbers": {{(_config.ShowLineNumbers ? "true" : "false")}},
            "minimap": { "enabled": {{(_config.ShowMinimap ? "true" : "false")}} },
            "folding": {{(_config.EnableFolding ? "true" : "false")}},
            "wordWrap": "{{(_config.WordWrap ? "on" : "off")}}",
            "tabSize": {{_config.TabSize}},
            "insertSpaces": {{(_config.InsertSpaces ? "true" : "false")}},
            "fontFamily": "{{_config.FontFamily}}",
            "fontSize": {{_config.FontSize}},
            "readOnly": {{(_config.ReadOnly ? "true" : "false")}},
            "automaticLayout": true,
            "scrollBeyondLastLine": false
        }
        """;
    }

    /// <summary>
    /// Creates markers JSON for Monaco editor.
    /// </summary>
    public string GetMarkersJson()
    {
        if (_markers.Count == 0)
            return "[]";

        var items = _markers.Select(m =>
        {
            var severity = m.Severity switch
            {
                CodeMarkerSeverity.Hint => 1,
                CodeMarkerSeverity.Info => 2,
                CodeMarkerSeverity.Warning => 4,
                CodeMarkerSeverity.Error => 8,
                _ => 8
            };

            return $$"""
            {
                "startLineNumber": {{m.StartLine}},
                "startColumn": {{m.StartColumn}},
                "endLineNumber": {{m.EndLine}},
                "endColumn": {{m.EndColumn}},
                "message": "{{EscapeJson(m.Message)}}",
                "severity": {{severity}}
            }
            """;
        });

        return $"[{string.Join(",", items)}]";
    }

    private static string EscapeJson(string s)
    {
        return s.Replace("\\", "\\\\")
                .Replace("\"", "\\\"")
                .Replace("\n", "\\n")
                .Replace("\r", "\\r")
                .Replace("\t", "\\t");
    }
}
