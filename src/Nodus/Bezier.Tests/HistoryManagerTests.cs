namespace Bezier.Tests;

using Bezier.Core.Commands;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class HistoryManagerTests
{
    private readonly HistoryManager _history = new();

    [Fact]
    public void ExecuteCommand_AddsToUndoStack()
    {
        var element = new SvgRect { X = 0, Y = 0 };
        var command = new MoveCommand(element, 10, 20);

        _history.ExecuteCommand(command);

        Assert.True(_history.CanUndo);
        Assert.Equal(1, _history.UndoCount);
        Assert.Equal(10, element.Transform.TranslateX);
        Assert.Equal(20, element.Transform.TranslateY);
    }

    [Fact]
    public void ExecuteCommand_ClearsRedoStack()
    {
        var element = new SvgRect();
        var command1 = new MoveCommand(element, 10, 0);
        var command2 = new MoveCommand(element, 0, 10);

        _history.ExecuteCommand(command1);
        _history.Undo();
        Assert.True(_history.CanRedo);

        _history.ExecuteCommand(command2);
        Assert.False(_history.CanRedo);
    }

    [Fact]
    public void Undo_RevertsCommand()
    {
        var element = new SvgRect { X = 0, Y = 0 };
        var command = new MoveCommand(element, 50, 100);

        _history.ExecuteCommand(command);
        Assert.Equal(50, element.Transform.TranslateX);

        _history.Undo();
        Assert.Equal(0, element.Transform.TranslateX);
        Assert.Equal(0, element.Transform.TranslateY);
    }

    [Fact]
    public void Undo_MovesToRedoStack()
    {
        var element = new SvgRect();
        var command = new MoveCommand(element, 10, 10);

        _history.ExecuteCommand(command);
        _history.Undo();

        Assert.False(_history.CanUndo);
        Assert.True(_history.CanRedo);
        Assert.Equal(1, _history.RedoCount);
    }

    [Fact]
    public void Redo_ReappliesCommand()
    {
        var element = new SvgRect();
        var command = new MoveCommand(element, 25, 50);

        _history.ExecuteCommand(command);
        _history.Undo();
        Assert.Equal(0, element.Transform.TranslateX);

        _history.Redo();
        Assert.Equal(25, element.Transform.TranslateX);
        Assert.Equal(50, element.Transform.TranslateY);
    }

    [Fact]
    public void Undo_ReturnsFalse_WhenEmpty()
    {
        var result = _history.Undo();
        Assert.False(result);
    }

    [Fact]
    public void Redo_ReturnsFalse_WhenEmpty()
    {
        var result = _history.Redo();
        Assert.False(result);
    }

    [Fact]
    public void Clear_RemovesAllHistory()
    {
        var element = new SvgRect();
        _history.ExecuteCommand(new MoveCommand(element, 10, 10));
        _history.ExecuteCommand(new MoveCommand(element, 20, 20));
        _history.Undo();

        _history.Clear();

        Assert.False(_history.CanUndo);
        Assert.False(_history.CanRedo);
        Assert.Equal(0, _history.UndoCount);
        Assert.Equal(0, _history.RedoCount);
    }

    [Fact]
    public void NextUndoDescription_ReturnsCorrectDescription()
    {
        var element = new SvgRect { Name = "TestRect" };
        var command = new MoveCommand(element, 10, 10);

        _history.ExecuteCommand(command);

        Assert.Equal("Move TestRect", _history.NextUndoDescription);
    }

    [Fact]
    public void NextRedoDescription_ReturnsCorrectDescription()
    {
        var element = new SvgRect { Name = "TestRect" };
        var command = new MoveCommand(element, 10, 10);

        _history.ExecuteCommand(command);
        _history.Undo();

        Assert.Equal("Move TestRect", _history.NextRedoDescription);
    }

    [Fact]
    public void HistoryChanged_RaisedOnExecute()
    {
        var eventRaised = false;
        _history.HistoryChanged += (_, _) => eventRaised = true;

        var element = new SvgRect();
        _history.ExecuteCommand(new MoveCommand(element, 10, 10));

        Assert.True(eventRaised);
    }

    [Fact]
    public void HistoryChanged_RaisedOnUndo()
    {
        var element = new SvgRect();
        _history.ExecuteCommand(new MoveCommand(element, 10, 10));

        var eventRaised = false;
        _history.HistoryChanged += (_, _) => eventRaised = true;

        _history.Undo();

        Assert.True(eventRaised);
    }

    [Fact]
    public void MaxHistorySize_LimitsUndoStack()
    {
        _history.MaxHistorySize = 3;
        var element = new SvgRect();

        for (var i = 0; i < 10; i++)
        {
            _history.ExecuteCommand(new MoveCommand(element, i, i));
        }

        Assert.Equal(3, _history.UndoCount);
    }
}

public class MoveCommandTests
{
    [Fact]
    public void Execute_MovesElement()
    {
        var element = new SvgRect { X = 10, Y = 20 };
        var command = new MoveCommand(element, 5, 10);

        command.Execute();

        Assert.Equal(5, element.Transform.TranslateX);
        Assert.Equal(10, element.Transform.TranslateY);
    }

    [Fact]
    public void Undo_ReversesMove()
    {
        var element = new SvgRect();
        var command = new MoveCommand(element, 100, 200);

        command.Execute();
        command.Undo();

        Assert.Equal(0, element.Transform.TranslateX);
        Assert.Equal(0, element.Transform.TranslateY);
    }

    [Fact]
    public void Execute_MovesMultipleElements()
    {
        var elements = new VectorElement[]
        {
            new SvgRect(),
            new SvgCircle(),
            new SvgEllipse()
        };
        var command = new MoveCommand(elements, 50, 75);

        command.Execute();

        foreach (var element in elements)
        {
            Assert.Equal(50, element.Transform.TranslateX);
            Assert.Equal(75, element.Transform.TranslateY);
        }
    }

    [Fact]
    public void Description_SingleElement()
    {
        var element = new SvgRect { Name = "MyRect" };
        var command = new MoveCommand(element, 10, 10);

        Assert.Equal("Move MyRect", command.Description);
    }

    [Fact]
    public void Description_MultipleElements()
    {
        var elements = new VectorElement[] { new SvgRect(), new SvgCircle() };
        var command = new MoveCommand(elements, 10, 10);

        Assert.Equal("Move 2 elements", command.Description);
    }
}

public class RotateCommandTests
{
    [Fact]
    public void Execute_RotatesElement()
    {
        var element = new SvgRect();
        var originalTransform = element.Transform;
        var command = new RotateCommand(element, 45);

        command.Execute();

        // Transform should have changed after rotation
        Assert.NotEqual(originalTransform, element.Transform);
    }

    [Fact]
    public void Undo_ReversesRotation()
    {
        var element = new SvgRect();
        var originalTransform = element.Transform;
        var command = new RotateCommand(element, 90);

        command.Execute();
        command.Undo();

        // Transform should be back to identity after undo
        Assert.True(element.Transform.IsIdentity);
    }
}

public class ScaleCommandTests
{
    [Fact]
    public void Execute_ScalesElement()
    {
        var element = new SvgRect();
        var command = new ScaleCommand(element, 2.0, 1.5);

        command.Execute();

        Assert.Equal(2.0, element.Transform.ScaleX);
        Assert.Equal(1.5, element.Transform.ScaleY);
    }

    [Fact]
    public void Undo_ReversesScale()
    {
        var element = new SvgRect();
        var command = new ScaleCommand(element, 2.0, 2.0);

        command.Execute();
        command.Undo();

        Assert.Equal(1.0, element.Transform.ScaleX);
        Assert.Equal(1.0, element.Transform.ScaleY);
    }
}

public class AddDeleteElementCommandTests
{
    [Fact]
    public void AddElement_AddsToDocument()
    {
        var document = new VectorDocument();
        var element = new SvgRect();
        var command = new AddElementCommand(document, element);

        command.Execute();

        Assert.Single(document.Elements);
        Assert.Same(element, document.Elements[0]);
    }

    [Fact]
    public void AddElement_Undo_RemovesElement()
    {
        var document = new VectorDocument();
        var element = new SvgRect();
        var command = new AddElementCommand(document, element);

        command.Execute();
        command.Undo();

        Assert.Empty(document.Elements);
    }

    [Fact]
    public void DeleteElement_RemovesFromDocument()
    {
        var document = new VectorDocument();
        var element = new SvgRect();
        document.Elements.Add(element);

        var command = new DeleteElementCommand(document, element);
        command.Execute();

        Assert.Empty(document.Elements);
    }

    [Fact]
    public void DeleteElement_Undo_RestoresElement()
    {
        var document = new VectorDocument();
        var element = new SvgRect();
        document.Elements.Add(element);

        var command = new DeleteElementCommand(document, element);
        command.Execute();
        command.Undo();

        Assert.Single(document.Elements);
        Assert.Same(element, document.Elements[0]);
    }

    [Fact]
    public void DeleteMultiple_Undo_RestoresAtOriginalPositions()
    {
        var document = new VectorDocument();
        var rect = new SvgRect { Name = "Rect" };
        var circle = new SvgCircle { Name = "Circle" };
        var ellipse = new SvgEllipse { Name = "Ellipse" };
        document.Elements.Add(rect);
        document.Elements.Add(circle);
        document.Elements.Add(ellipse);

        var command = new DeleteElementCommand(document, [rect, ellipse]);
        command.Execute();

        Assert.Single(document.Elements);
        Assert.Same(circle, document.Elements[0]);

        command.Undo();

        Assert.Equal(3, document.Elements.Count);
        Assert.Same(rect, document.Elements[0]);
        Assert.Same(circle, document.Elements[1]);
        Assert.Same(ellipse, document.Elements[2]);
    }
}

public class ReorderCommandTests
{
    [Fact]
    public void BringToFront_MovesToEnd()
    {
        var document = new VectorDocument();
        var rect1 = new SvgRect { Name = "Rect1" };
        var rect2 = new SvgRect { Name = "Rect2" };
        var rect3 = new SvgRect { Name = "Rect3" };
        document.Elements.Add(rect1);
        document.Elements.Add(rect2);
        document.Elements.Add(rect3);

        var command = new ReorderCommand(document, rect1, ReorderType.BringToFront);
        command.Execute();

        Assert.Same(rect1, document.Elements[2]);
    }

    [Fact]
    public void SendToBack_MovesToStart()
    {
        var document = new VectorDocument();
        var rect1 = new SvgRect { Name = "Rect1" };
        var rect2 = new SvgRect { Name = "Rect2" };
        var rect3 = new SvgRect { Name = "Rect3" };
        document.Elements.Add(rect1);
        document.Elements.Add(rect2);
        document.Elements.Add(rect3);

        var command = new ReorderCommand(document, rect3, ReorderType.SendToBack);
        command.Execute();

        Assert.Same(rect3, document.Elements[0]);
    }

    [Fact]
    public void Undo_RestoresOriginalPosition()
    {
        var document = new VectorDocument();
        var rect1 = new SvgRect { Name = "Rect1" };
        var rect2 = new SvgRect { Name = "Rect2" };
        document.Elements.Add(rect1);
        document.Elements.Add(rect2);

        var command = new ReorderCommand(document, rect1, ReorderType.BringToFront);
        command.Execute();
        command.Undo();

        Assert.Same(rect1, document.Elements[0]);
        Assert.Same(rect2, document.Elements[1]);
    }
}

public class GroupUngroupCommandTests
{
    [Fact]
    public void GroupCommand_CreatesGroup()
    {
        var document = new VectorDocument();
        var rect = new SvgRect { Name = "Rect" };
        var circle = new SvgCircle { Name = "Circle" };
        document.Elements.Add(rect);
        document.Elements.Add(circle);

        var command = new GroupCommand(document, new VectorElement[] { rect, circle });
        command.Execute();

        Assert.Single(document.Elements);
        Assert.IsType<SvgGroup>(document.Elements[0]);
        var group = (SvgGroup)document.Elements[0];
        Assert.Equal(2, group.Children.Count);
    }

    [Fact]
    public void GroupCommand_Undo_RestoresElements()
    {
        var document = new VectorDocument();
        var rect = new SvgRect { Name = "Rect" };
        var circle = new SvgCircle { Name = "Circle" };
        document.Elements.Add(rect);
        document.Elements.Add(circle);

        var command = new GroupCommand(document, new VectorElement[] { rect, circle });
        command.Execute();
        command.Undo();

        Assert.Equal(2, document.Elements.Count);
        Assert.Same(rect, document.Elements[0]);
        Assert.Same(circle, document.Elements[1]);
    }

    [Fact]
    public void UngroupCommand_ExtractsChildren()
    {
        var document = new VectorDocument();
        var group = new SvgGroup { Name = "Group" };
        var rect = new SvgRect { Name = "Rect" };
        var circle = new SvgCircle { Name = "Circle" };
        group.Children.Add(rect);
        group.Children.Add(circle);
        document.Elements.Add(group);

        var command = new UngroupCommand(document, group);
        command.Execute();

        Assert.Equal(2, document.Elements.Count);
        Assert.Same(rect, document.Elements[0]);
        Assert.Same(circle, document.Elements[1]);
    }

    [Fact]
    public void UngroupCommand_Undo_RestoresGroup()
    {
        var document = new VectorDocument();
        var group = new SvgGroup { Name = "Group" };
        var rect = new SvgRect { Name = "Rect" };
        var circle = new SvgCircle { Name = "Circle" };
        group.Children.Add(rect);
        group.Children.Add(circle);
        document.Elements.Add(group);

        var command = new UngroupCommand(document, group);
        command.Execute();
        command.Undo();

        Assert.Single(document.Elements);
        Assert.Same(group, document.Elements[0]);
        Assert.Equal(2, group.Children.Count);
    }
}
