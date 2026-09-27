namespace Bezier.Tests;

using Bezier.Core.Commands;
using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class TransformHandleTests
{
    [Fact]
    public void GenerateHandles_Returns9Handles_WithRotation()
    {
        var handles = TransformHandleGenerator.GenerateHandles(0, 0, 100, 100, includeRotation: true);
        
        Assert.Equal(9, handles.Count);
    }

    [Fact]
    public void GenerateHandles_Returns8Handles_WithoutRotation()
    {
        var handles = TransformHandleGenerator.GenerateHandles(0, 0, 100, 100, includeRotation: false);
        
        Assert.Equal(8, handles.Count);
    }

    [Fact]
    public void GenerateHandles_CornerHandles_AtCorrectPositions()
    {
        var handles = TransformHandleGenerator.GenerateHandles(10, 20, 100, 50);
        
        var topLeft = handles.First(h => h.Type == HandleType.TopLeft);
        var topRight = handles.First(h => h.Type == HandleType.TopRight);
        var bottomLeft = handles.First(h => h.Type == HandleType.BottomLeft);
        var bottomRight = handles.First(h => h.Type == HandleType.BottomRight);

        Assert.Equal(10, topLeft.X);
        Assert.Equal(20, topLeft.Y);
        Assert.Equal(110, topRight.X);
        Assert.Equal(20, topRight.Y);
        Assert.Equal(10, bottomLeft.X);
        Assert.Equal(70, bottomLeft.Y);
        Assert.Equal(110, bottomRight.X);
        Assert.Equal(70, bottomRight.Y);
    }

    [Fact]
    public void GenerateHandles_EdgeHandles_AtMidpoints()
    {
        var handles = TransformHandleGenerator.GenerateHandles(0, 0, 100, 100);
        
        var topCenter = handles.First(h => h.Type == HandleType.TopCenter);
        var bottomCenter = handles.First(h => h.Type == HandleType.BottomCenter);
        var leftCenter = handles.First(h => h.Type == HandleType.LeftCenter);
        var rightCenter = handles.First(h => h.Type == HandleType.RightCenter);

        Assert.Equal(50, topCenter.X);
        Assert.Equal(0, topCenter.Y);
        Assert.Equal(50, bottomCenter.X);
        Assert.Equal(100, bottomCenter.Y);
        Assert.Equal(0, leftCenter.X);
        Assert.Equal(50, leftCenter.Y);
        Assert.Equal(100, rightCenter.X);
        Assert.Equal(50, rightCenter.Y);
    }

    [Fact]
    public void GenerateHandles_RotationHandle_AboveTopCenter()
    {
        var handles = TransformHandleGenerator.GenerateHandles(0, 0, 100, 100);
        
        var rotation = handles.First(h => h.Type == HandleType.Rotation);

        Assert.Equal(50, rotation.X);
        Assert.True(rotation.Y < 0); // Above the bounding box
    }

    [Fact]
    public void TransformHandle_HitTest_ReturnsTrue_WhenPointInside()
    {
        var handle = new TransformHandle(HandleType.TopLeft, 50, 50, 8);

        Assert.True(handle.HitTest(50, 50));
        Assert.True(handle.HitTest(52, 52));
        Assert.True(handle.HitTest(48, 48));
    }

    [Fact]
    public void TransformHandle_HitTest_ReturnsFalse_WhenPointOutside()
    {
        var handle = new TransformHandle(HandleType.TopLeft, 50, 50, 8);

        Assert.False(handle.HitTest(60, 60));
        Assert.False(handle.HitTest(40, 40));
    }

    [Fact]
    public void TransformHandle_GetCursor_ReturnsCorrectCursor()
    {
        Assert.Equal(HandleCursor.SizeNWSE, new TransformHandle(HandleType.TopLeft, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.SizeNWSE, new TransformHandle(HandleType.BottomRight, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.SizeNESW, new TransformHandle(HandleType.TopRight, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.SizeNESW, new TransformHandle(HandleType.BottomLeft, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.SizeWE, new TransformHandle(HandleType.LeftCenter, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.SizeWE, new TransformHandle(HandleType.RightCenter, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.SizeNS, new TransformHandle(HandleType.TopCenter, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.SizeNS, new TransformHandle(HandleType.BottomCenter, 0, 0).GetCursor());
        Assert.Equal(HandleCursor.Rotate, new TransformHandle(HandleType.Rotation, 0, 0).GetCursor());
    }

    [Fact]
    public void TransformHandle_GetOpposite_ReturnsCorrectHandle()
    {
        Assert.Equal(HandleType.BottomRight, new TransformHandle(HandleType.TopLeft, 0, 0).GetOpposite());
        Assert.Equal(HandleType.BottomLeft, new TransformHandle(HandleType.TopRight, 0, 0).GetOpposite());
        Assert.Equal(HandleType.TopRight, new TransformHandle(HandleType.BottomLeft, 0, 0).GetOpposite());
        Assert.Equal(HandleType.TopLeft, new TransformHandle(HandleType.BottomRight, 0, 0).GetOpposite());
    }

    [Fact]
    public void GetAnchorPoint_ReturnsOppositeCorner()
    {
        var (ax, ay) = TransformHandleGenerator.GetAnchorPoint(HandleType.TopLeft, 0, 0, 100, 100);
        Assert.Equal(100, ax);
        Assert.Equal(100, ay);

        (ax, ay) = TransformHandleGenerator.GetAnchorPoint(HandleType.BottomRight, 0, 0, 100, 100);
        Assert.Equal(0, ax);
        Assert.Equal(0, ay);
    }
}

public class TransformServiceTests
{
    [Fact]
    public void CalculateResize_BottomRight_IncreasesSize()
    {
        var (x, y, w, h) = TransformService.CalculateResize(0, 0, 100, 100, HandleType.BottomRight, 50, 50);

        Assert.Equal(0, x);
        Assert.Equal(0, y);
        Assert.Equal(150, w);
        Assert.Equal(150, h);
    }

    [Fact]
    public void CalculateResize_TopLeft_MovesOriginAndChangesSize()
    {
        var (x, y, w, h) = TransformService.CalculateResize(0, 0, 100, 100, HandleType.TopLeft, 20, 20);

        Assert.Equal(20, x);
        Assert.Equal(20, y);
        Assert.Equal(80, w);
        Assert.Equal(80, h);
    }

    [Fact]
    public void CalculateResize_EdgeHandle_OnlyChangesOneDirection()
    {
        var (x, y, w, h) = TransformService.CalculateResize(0, 0, 100, 100, HandleType.RightCenter, 50, 0);

        Assert.Equal(0, x);
        Assert.Equal(0, y);
        Assert.Equal(150, w);
        Assert.Equal(100, h); // Height unchanged
    }

    [Fact]
    public void CalculateResize_MinimumSize_EnforcedAt1()
    {
        var (x, y, w, h) = TransformService.CalculateResize(0, 0, 100, 100, HandleType.BottomRight, -200, -200);

        Assert.Equal(1, w);
        Assert.Equal(1, h);
    }

    [Fact]
    public void CalculateRotationAngle_FromTopCenter()
    {
        // Point directly above center should be 0 degrees
        var angle = TransformService.CalculateRotationAngle(50, 50, 50, 0);
        Assert.Equal(0, angle);
    }

    [Fact]
    public void CalculateRotationAngle_FromRightCenter()
    {
        // Point directly to the right should be 90 degrees
        var angle = TransformService.CalculateRotationAngle(50, 50, 100, 50);
        Assert.Equal(90, angle);
    }

    [Fact]
    public void SnapAngle_SnapsTo15DegreeIncrements()
    {
        Assert.Equal(0, TransformService.SnapAngle(7));
        Assert.Equal(15, TransformService.SnapAngle(8));
        Assert.Equal(15, TransformService.SnapAngle(15));
        Assert.Equal(15, TransformService.SnapAngle(22));
        Assert.Equal(30, TransformService.SnapAngle(23));
        Assert.Equal(45, TransformService.SnapAngle(45));
        Assert.Equal(90, TransformService.SnapAngle(90));
    }

    [Fact]
    public void NormalizeAngle_KeepsAngleIn0To360Range()
    {
        Assert.Equal(0, TransformService.NormalizeAngle(0));
        Assert.Equal(45, TransformService.NormalizeAngle(45));
        Assert.Equal(0, TransformService.NormalizeAngle(360));
        Assert.Equal(90, TransformService.NormalizeAngle(450));
        Assert.Equal(270, TransformService.NormalizeAngle(-90));
    }

    [Fact]
    public void CalculateScale_ReturnsCorrectFactors()
    {
        var (scaleX, scaleY) = TransformService.CalculateScale(100, 50, 200, 100);

        Assert.Equal(2, scaleX);
        Assert.Equal(2, scaleY);
    }

    [Fact]
    public void TransformPoint_NoTransform_ReturnsOriginalPoint()
    {
        var (x, y) = TransformService.TransformPoint(100, 100, 50, 50, 0, 1, 1);

        Assert.Equal(100, x);
        Assert.Equal(100, y);
    }

    [Fact]
    public void TransformPoint_Scale_DoublesDistance()
    {
        var (x, y) = TransformService.TransformPoint(100, 50, 50, 50, 0, 2, 1);

        Assert.Equal(150, x); // (100 - 50) * 2 + 50
        Assert.Equal(50, y);
    }

    [Fact]
    public void TransformPoint_Rotation90_RotatesCorrectly()
    {
        var (x, y) = TransformService.TransformPoint(100, 50, 50, 50, 90, 1, 1);

        Assert.Equal(50, x, 5); // Precision tolerance
        Assert.Equal(100, y, 5);
    }
}

public class ResizeCommandTests
{
    [Fact]
    public void Execute_ScalesElement()
    {
        var rect = new SvgRect { X = 0, Y = 0, Width = 100, Height = 100 };
        var command = new ResizeCommand(rect, 2, 2, 0, 0);

        command.Execute();

        // Transform scale should be doubled
        Assert.Equal(2, rect.Transform.ScaleX);
        Assert.Equal(2, rect.Transform.ScaleY);
    }

    [Fact]
    public void Undo_RestoresOriginalScale()
    {
        var rect = new SvgRect { X = 0, Y = 0, Width = 100, Height = 100 };
        var originalTransform = rect.Transform;
        var command = new ResizeCommand(rect, 2, 2, 0, 0);

        command.Execute();
        command.Undo();

        Assert.Equal(originalTransform.ScaleX, rect.Transform.ScaleX, 5);
        Assert.Equal(originalTransform.ScaleY, rect.Transform.ScaleY, 5);
    }

    [Fact]
    public void Description_SingleElement_IncludesName()
    {
        var rect = new SvgRect { Name = "MyRect" };
        var command = new ResizeCommand(rect, 2, 2, 0, 0);

        Assert.Contains("MyRect", command.Description);
    }

    [Fact]
    public void Description_MultipleElements_IncludesCount()
    {
        var rect1 = new SvgRect();
        var rect2 = new SvgRect();
        var command = new ResizeCommand([rect1, rect2], 2, 2, 0, 0);

        Assert.Contains("2 elements", command.Description);
    }

    [Fact]
    public void IsUndoable_ReturnsTrue()
    {
        var rect = new SvgRect();
        var command = new ResizeCommand(rect, 2, 2, 0, 0);

        Assert.True(command.IsUndoable);
    }
}
