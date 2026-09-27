namespace Bezier.Tests;

using Bezier.Core.Interfaces;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;
using Bezier.Core.Tools;

public class TextToolTests
{
    private readonly TextTool _tool;
    private readonly VectorDocument _document;
    private readonly HistoryManager _history;

    public TextToolTests()
    {
        _tool = new TextTool();
        _document = new VectorDocument();
        _history = new HistoryManager();
        _tool.SetContext(_document, _history);
        _tool.OnActivate();
    }

    [Fact]
    public void Properties_AreCorrect()
    {
        Assert.Equal("Text", _tool.Name);
        Assert.Equal("TextFont", _tool.Icon);
        Assert.Equal("T", _tool.Shortcut);
        Assert.Equal(ToolCursor.Text, _tool.Cursor);
    }

    [Fact]
    public void DefaultProperties_AreSet()
    {
        Assert.Equal("Arial", _tool.DefaultFontFamily);
        Assert.Equal(24, _tool.DefaultFontSize);
        Assert.Equal(400, _tool.DefaultFontWeight);
        Assert.False(_tool.DefaultItalic);
        Assert.Equal(TextAnchor.Start, _tool.DefaultTextAnchor);
    }

    [Fact]
    public void Click_StartsEditing()
    {
        Assert.False(_tool.IsEditing);

        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.True(_tool.IsEditing);
        Assert.NotNull(_tool.ActiveText);
    }

    [Fact]
    public void Click_CreatesTextAtPosition()
    {
        _tool.OnMouseDown(new ToolPoint(150, 200), KeyModifiers.None);

        Assert.NotNull(_tool.ActiveText);
        Assert.Equal(150, _tool.ActiveText!.X);
        Assert.Equal(200, _tool.ActiveText!.Y);
    }

    [Fact]
    public void TypeCharacter_AddsToBuffer()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);

        _tool.OnKeyDown("H", KeyModifiers.None);
        _tool.OnKeyDown("i", KeyModifiers.None);

        Assert.Equal("Hi", _tool.EditBuffer);
        Assert.Equal(2, _tool.CursorPosition);
    }

    [Fact]
    public void Backspace_DeletesCharacter()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("H", KeyModifiers.None);
        _tool.OnKeyDown("i", KeyModifiers.None);

        _tool.OnKeyDown("Backspace", KeyModifiers.None);

        Assert.Equal("H", _tool.EditBuffer);
        Assert.Equal(1, _tool.CursorPosition);
    }

    [Fact]
    public void Delete_DeletesNextCharacter()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("H", KeyModifiers.None);
        _tool.OnKeyDown("i", KeyModifiers.None);
        _tool.OnKeyDown("Left", KeyModifiers.None);
        _tool.OnKeyDown("Left", KeyModifiers.None);

        _tool.OnKeyDown("Delete", KeyModifiers.None);

        Assert.Equal("i", _tool.EditBuffer);
    }

    [Fact]
    public void LeftArrow_MovesCursor()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("A", KeyModifiers.None);
        _tool.OnKeyDown("B", KeyModifiers.None);

        Assert.Equal(2, _tool.CursorPosition);

        _tool.OnKeyDown("Left", KeyModifiers.None);

        Assert.Equal(1, _tool.CursorPosition);
    }

    [Fact]
    public void RightArrow_MovesCursor()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("A", KeyModifiers.None);
        _tool.OnKeyDown("B", KeyModifiers.None);
        _tool.OnKeyDown("Left", KeyModifiers.None);
        _tool.OnKeyDown("Left", KeyModifiers.None);

        _tool.OnKeyDown("Right", KeyModifiers.None);

        Assert.Equal(1, _tool.CursorPosition);
    }

    [Fact]
    public void Home_MovesCursorToStart()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("A", KeyModifiers.None);
        _tool.OnKeyDown("B", KeyModifiers.None);
        _tool.OnKeyDown("C", KeyModifiers.None);

        _tool.OnKeyDown("Home", KeyModifiers.None);

        Assert.Equal(0, _tool.CursorPosition);
    }

    [Fact]
    public void End_MovesCursorToEnd()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("A", KeyModifiers.None);
        _tool.OnKeyDown("B", KeyModifiers.None);
        _tool.OnKeyDown("Home", KeyModifiers.None);

        _tool.OnKeyDown("End", KeyModifiers.None);

        Assert.Equal(2, _tool.CursorPosition);
    }

    [Fact]
    public void Escape_CancelsEditing()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("H", KeyModifiers.None);
        _tool.OnKeyDown("i", KeyModifiers.None);

        _tool.OnKeyDown("Escape", KeyModifiers.None);

        Assert.False(_tool.IsEditing);
        Assert.Null(_tool.ActiveText);
        Assert.Empty(_document.Elements); // Text not saved
    }

    [Fact]
    public void Enter_FinishesEditingAndSaves()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("H", KeyModifiers.None);
        _tool.OnKeyDown("i", KeyModifiers.None);

        _tool.OnKeyDown("Enter", KeyModifiers.None);

        Assert.False(_tool.IsEditing);
        Assert.Single(_document.Elements);
        var text = _document.Elements[0] as SvgText;
        Assert.NotNull(text);
        Assert.Equal("Hi", text!.Text);
    }

    [Fact]
    public void ShiftEnter_InsertsNewline()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("A", KeyModifiers.None);

        _tool.OnKeyDown("Enter", KeyModifiers.Shift);
        _tool.OnKeyDown("B", KeyModifiers.None);

        Assert.Equal("A\nB", _tool.EditBuffer);
        Assert.True(_tool.IsEditing);
    }

    [Fact]
    public void EmptyText_NotSaved()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);

        _tool.OnKeyDown("Enter", KeyModifiers.None);

        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void SavedText_IsUndoable()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("T", KeyModifiers.None);
        _tool.OnKeyDown("e", KeyModifiers.None);
        _tool.OnKeyDown("s", KeyModifiers.None);
        _tool.OnKeyDown("t", KeyModifiers.None);
        _tool.OnKeyDown("Enter", KeyModifiers.None);

        Assert.Single(_document.Elements);

        _history.Undo();

        Assert.Empty(_document.Elements);
    }

    [Fact]
    public void ClickOnExistingText_StartsEditing()
    {
        // First, create a text element with a large enough area to hit
        var text = new SvgText
        {
            X = 100,
            Y = 130,  // Text Y is baseline, so content is above this
            Text = "HelloWorld",
            FontSize = 24
        };
        _document.Elements.Add(text);

        // The bounding box is from (X, Y - height) to (X + width, Y)
        // With FontSize=24, height ≈ 28.8, so bounds are roughly (100, 101) to (244, 130)
        _tool.OnMouseDown(new ToolPoint(120, 115), KeyModifiers.None);

        Assert.True(_tool.IsEditing);
        Assert.Equal("HelloWorld", _tool.EditBuffer);
    }

    [Fact]
    public void EditingStateChanged_EventRaised()
    {
        var stateChanges = new List<bool>();
        _tool.EditingStateChanged += (_, state) => stateChanges.Add(state);

        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("A", KeyModifiers.None);
        _tool.OnKeyDown("Enter", KeyModifiers.None);

        Assert.Equal(2, stateChanges.Count);
        Assert.True(stateChanges[0]); // Started editing
        Assert.False(stateChanges[1]); // Finished editing
    }

    [Fact]
    public void TextChanged_EventRaised()
    {
        var changeCount = 0;
        _tool.TextChanged += (_, _) => changeCount++;

        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("A", KeyModifiers.None);
        _tool.OnKeyDown("B", KeyModifiers.None);

        Assert.Equal(2, changeCount);
    }

    [Fact]
    public void CtrlA_SelectsAll()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("H", KeyModifiers.None);
        _tool.OnKeyDown("e", KeyModifiers.None);
        _tool.OnKeyDown("l", KeyModifiers.None);
        _tool.OnKeyDown("l", KeyModifiers.None);
        _tool.OnKeyDown("o", KeyModifiers.None);

        var result = _tool.OnKeyDown("A", KeyModifiers.Control);

        Assert.True(result);
        Assert.Equal(5, _tool.CursorPosition); // Cursor at end
    }

    [Fact]
    public void OnDeactivate_SavesText()
    {
        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);
        _tool.OnKeyDown("T", KeyModifiers.None);
        _tool.OnKeyDown("e", KeyModifiers.None);
        _tool.OnKeyDown("s", KeyModifiers.None);
        _tool.OnKeyDown("t", KeyModifiers.None);

        _tool.OnDeactivate();

        Assert.Single(_document.Elements);
        Assert.False(_tool.IsEditing);
    }

    [Fact]
    public void NewText_UsesDefaultProperties()
    {
        _tool.DefaultFontFamily = "Verdana";
        _tool.DefaultFontSize = 32;
        _tool.DefaultFontWeight = 700;
        _tool.DefaultTextAnchor = TextAnchor.Middle;

        _tool.OnMouseDown(new ToolPoint(100, 100), KeyModifiers.None);

        Assert.Equal("Verdana", _tool.ActiveText?.FontFamily);
        Assert.Equal(32, _tool.ActiveText?.FontSize);
        Assert.Equal(700, _tool.ActiveText?.FontWeight);
        Assert.Equal(TextAnchor.Middle, _tool.ActiveText?.TextAnchor);
    }
}
