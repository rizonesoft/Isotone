namespace Bezier.Tests;

using Bezier.Core.Services;

public class CodeEditorServiceTests
{
    private readonly CodeEditorService _service;

    public CodeEditorServiceTests()
    {
        _service = new CodeEditorService();
    }

    [Fact]
    public void CodeEditorService_DefaultValues()
    {
        Assert.Equal(string.Empty, _service.Content);
        Assert.False(_service.IsDirty);
        Assert.False(_service.IsSyncLocked);
        Assert.Empty(_service.Markers);
    }

    [Fact]
    public void Content_SetterMarksDirty()
    {
        _service.Content = "<svg></svg>";

        Assert.True(_service.IsDirty);
    }

    [Fact]
    public void SetContent_UpdatesContent()
    {
        _service.SetContent("<svg></svg>");

        Assert.Equal("<svg></svg>", _service.Content);
    }

    [Fact]
    public void SetContent_WhenSyncLocked_DoesNotUpdate()
    {
        _service.SetContent("<svg></svg>");
        _service.IsSyncLocked = true;

        _service.SetContent("<svg><rect/></svg>");

        Assert.Equal("<svg></svg>", _service.Content);
    }

    [Fact]
    public void GetContent_ReturnsContent()
    {
        _service.SetContent("<svg></svg>");

        Assert.Equal("<svg></svg>", _service.GetContent());
    }

    [Fact]
    public void NotifyUserContentChanged_RaisesEvent()
    {
        string? changedContent = null;
        bool? isUserChange = null;
        _service.ContentChanged += (_, e) =>
        {
            changedContent = e.Content;
            isUserChange = e.IsUserChange;
        };

        _service.NotifyUserContentChanged("<svg></svg>");

        Assert.Equal("<svg></svg>", changedContent);
        Assert.True(isUserChange);
    }

    [Fact]
    public void NotifyUserContentChanged_MarksDirty()
    {
        _service.NotifyUserContentChanged("<svg></svg>");

        Assert.True(_service.IsDirty);
    }

    [Fact]
    public void MarkAsSaved_ClearsDirty()
    {
        _service.Content = "<svg></svg>";

        _service.MarkAsSaved();

        Assert.False(_service.IsDirty);
    }

    [Fact]
    public void ValidateContent_ValidXml_NoMarkers()
    {
        _service.SetContent("<svg><rect/></svg>");

        Assert.Empty(_service.Markers);
    }

    [Fact]
    public void ValidateContent_InvalidXml_AddsMarker()
    {
        _service.SetContent("<svg><rect></svg>");

        Assert.Single(_service.Markers);
        Assert.Equal(CodeMarkerSeverity.Error, _service.Markers[0].Severity);
    }

    [Fact]
    public void ValidateContent_EmptyContent_NoMarkers()
    {
        _service.SetContent("");

        Assert.Empty(_service.Markers);
    }

    [Fact]
    public void ValidateContent_RaisesMarkersChanged()
    {
        IReadOnlyList<CodeMarker>? changedMarkers = null;
        _service.MarkersChanged += (_, markers) => changedMarkers = markers;

        _service.SetContent("<svg></svg>");

        Assert.NotNull(changedMarkers);
    }

    [Fact]
    public void FormatContent_FormatsValidXml()
    {
        _service.SetContent("<svg><rect/></svg>");

        var formatted = _service.FormatContent();

        Assert.Contains("\n", formatted);
    }

    [Fact]
    public void FormatContent_InvalidXml_ReturnsOriginal()
    {
        var original = "<svg><rect></svg>";
        _service.SetContent(original);

        var formatted = _service.FormatContent();

        Assert.Equal(original, formatted);
    }

    [Fact]
    public void GetLineForElementId_FindsElement()
    {
        _service.SetContent("""
            <svg>
              <rect id="myRect"/>
            </svg>
            """);

        var line = _service.GetLineForElementId("myRect");

        Assert.NotNull(line);
        Assert.Equal(2, line);
    }

    [Fact]
    public void GetLineForElementId_NotFound_ReturnsNull()
    {
        _service.SetContent("<svg></svg>");

        var line = _service.GetLineForElementId("nonexistent");

        Assert.Null(line);
    }

    [Fact]
    public void GetElementIdAtLine_FindsElement()
    {
        _service.SetContent("""
            <svg>
              <rect id="myRect" x="10"/>
            </svg>
            """);

        var id = _service.GetElementIdAtLine(2);

        Assert.Equal("myRect", id);
    }

    [Fact]
    public void GetElementIdAtLine_NotFound_ReturnsNull()
    {
        _service.SetContent("<svg></svg>");

        var id = _service.GetElementIdAtLine(1);

        Assert.Null(id);
    }

    [Fact]
    public void ShouldSync_WhenNotLocked_ReturnsTrue()
    {
        _service.Config.DebounceDurationMs = 0;
        _service.Content = "<svg></svg>";

        Assert.True(_service.ShouldSync());
    }

    [Fact]
    public void ShouldSync_WhenLocked_ReturnsFalse()
    {
        _service.IsSyncLocked = true;

        Assert.False(_service.ShouldSync());
    }

    [Fact]
    public void NotifyCursorPositionChanged_RaisesEvent()
    {
        int? line = null;
        int? column = null;
        _service.CursorPositionChanged += (_, e) =>
        {
            line = e.Line;
            column = e.Column;
        };

        _service.NotifyCursorPositionChanged(10, 5);

        Assert.Equal(10, line);
        Assert.Equal(5, column);
    }

    [Fact]
    public void NotifyElementHovered_RaisesEvent()
    {
        string? elementId = null;
        _service.ElementHovered += (_, e) => elementId = e.ElementId;

        _service.NotifyElementHovered("rect1", 5, 10);

        Assert.Equal("rect1", elementId);
    }
}

public class CodeEditorConfigTests
{
    [Fact]
    public void CodeEditorConfig_DefaultValues()
    {
        var config = new CodeEditorConfig();

        Assert.Equal(CodeEditorTheme.Dark, config.Theme);
        Assert.True(config.ShowLineNumbers);
        Assert.True(config.ShowMinimap);
        Assert.True(config.EnableFolding);
        Assert.False(config.WordWrap);
        Assert.Equal(2, config.TabSize);
        Assert.True(config.InsertSpaces);
        Assert.Equal(14, config.FontSize);
        Assert.False(config.ReadOnly);
        Assert.Equal(300, config.DebounceDurationMs);
    }

    [Fact]
    public void CodeEditorConfig_AllowsCustomization()
    {
        var config = new CodeEditorConfig
        {
            Theme = CodeEditorTheme.Light,
            ShowLineNumbers = false,
            TabSize = 4,
            FontSize = 16
        };

        Assert.Equal(CodeEditorTheme.Light, config.Theme);
        Assert.False(config.ShowLineNumbers);
        Assert.Equal(4, config.TabSize);
        Assert.Equal(16, config.FontSize);
    }
}

public class CodeMarkerTests
{
    [Fact]
    public void CodeMarker_StoresAllProperties()
    {
        var marker = new CodeMarker
        {
            StartLine = 1,
            StartColumn = 5,
            EndLine = 1,
            EndColumn = 10,
            Message = "Test error",
            Severity = CodeMarkerSeverity.Error
        };

        Assert.Equal(1, marker.StartLine);
        Assert.Equal(5, marker.StartColumn);
        Assert.Equal(1, marker.EndLine);
        Assert.Equal(10, marker.EndColumn);
        Assert.Equal("Test error", marker.Message);
        Assert.Equal(CodeMarkerSeverity.Error, marker.Severity);
    }
}

public class MonacoConfigTests
{
    private readonly CodeEditorService _service;

    public MonacoConfigTests()
    {
        _service = new CodeEditorService();
    }

    [Fact]
    public void GetMonacoConfigJson_ContainsTheme()
    {
        _service.Config.Theme = CodeEditorTheme.Dark;

        var json = _service.GetMonacoConfigJson();

        Assert.Contains("vs-dark", json);
    }

    [Fact]
    public void GetMonacoConfigJson_LightTheme()
    {
        _service.Config.Theme = CodeEditorTheme.Light;

        var json = _service.GetMonacoConfigJson();

        Assert.Contains("\"vs\"", json);
    }

    [Fact]
    public void GetMonacoConfigJson_HighContrastTheme()
    {
        _service.Config.Theme = CodeEditorTheme.HighContrast;

        var json = _service.GetMonacoConfigJson();

        Assert.Contains("hc-black", json);
    }

    [Fact]
    public void GetMonacoConfigJson_ContainsLanguage()
    {
        var json = _service.GetMonacoConfigJson();

        Assert.Contains("\"language\": \"xml\"", json);
    }

    [Fact]
    public void GetMonacoConfigJson_ContainsLineNumbers()
    {
        _service.Config.ShowLineNumbers = true;

        var json = _service.GetMonacoConfigJson();

        Assert.Contains("\"lineNumbers\": true", json);
    }

    [Fact]
    public void GetMarkersJson_EmptyMarkers_ReturnsEmptyArray()
    {
        var json = _service.GetMarkersJson();

        Assert.Equal("[]", json);
    }

    [Fact]
    public void GetMarkersJson_WithMarkers_ReturnsArray()
    {
        _service.SetContent("<svg><rect></svg>"); // Invalid XML

        var json = _service.GetMarkersJson();

        Assert.StartsWith("[", json);
        Assert.EndsWith("]", json);
        Assert.Contains("severity", json);
    }
}

public class ContentChangedEventArgsTests
{
    [Fact]
    public void ContentChangedEventArgs_StoresValues()
    {
        var args = new ContentChangedEventArgs("<svg></svg>", true);

        Assert.Equal("<svg></svg>", args.Content);
        Assert.True(args.IsUserChange);
    }

    [Fact]
    public void ContentChangedEventArgs_DefaultIsUserChange()
    {
        var args = new ContentChangedEventArgs("<svg></svg>");

        Assert.True(args.IsUserChange);
    }
}

public class CursorPositionChangedEventArgsTests
{
    [Fact]
    public void CursorPositionChangedEventArgs_StoresValues()
    {
        var args = new CursorPositionChangedEventArgs(10, 5);

        Assert.Equal(10, args.Line);
        Assert.Equal(5, args.Column);
    }
}

public class ElementHoverEventArgsTests
{
    [Fact]
    public void ElementHoverEventArgs_StoresValues()
    {
        var args = new ElementHoverEventArgs("rect1", 5, 10);

        Assert.Equal("rect1", args.ElementId);
        Assert.Equal(5, args.Line);
        Assert.Equal(10, args.Column);
    }

    [Fact]
    public void ElementHoverEventArgs_AllowsNullElementId()
    {
        var args = new ElementHoverEventArgs(null, 5, 10);

        Assert.Null(args.ElementId);
    }
}
