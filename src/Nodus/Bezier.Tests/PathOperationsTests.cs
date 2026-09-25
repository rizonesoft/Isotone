namespace Bezier.Tests;

using Bezier.Core.Services;

public class PathOperationsServiceTests
{
    private readonly PathOperationsService _service;

    public PathOperationsServiceTests()
    {
        _service = new PathOperationsService();
    }

    [Fact]
    public void BooleanOp_WithEmptyPath1_ReturnsFalse()
    {
        var result = _service.BooleanOp("", "M0,0 L10,10", BooleanOperation.Union);

        Assert.False(result.Success);
        Assert.Contains("First path", result.ErrorMessage);
    }

    [Fact]
    public void BooleanOp_WithEmptyPath2_ReturnsFalse()
    {
        var result = _service.BooleanOp("M0,0 L10,10", "", BooleanOperation.Union);

        Assert.False(result.Success);
        Assert.Contains("Second path", result.ErrorMessage);
    }

    [Fact]
    public void BooleanOp_WithValidPaths_ReturnsSuccess()
    {
        var result = _service.BooleanOp("M0,0 L10,10", "M5,5 L15,15", BooleanOperation.Union);

        Assert.True(result.Success);
        Assert.NotNull(result.PathData);
    }

    [Theory]
    [InlineData(BooleanOperation.Union)]
    [InlineData(BooleanOperation.Subtract)]
    [InlineData(BooleanOperation.Intersect)]
    [InlineData(BooleanOperation.Exclude)]
    public void BooleanOp_SupportsAllOperationTypes(BooleanOperation operation)
    {
        var result = _service.BooleanOp("M0,0 L10,10 Z", "M5,5 L15,15 Z", operation);

        Assert.True(result.Success);
    }

    [Fact]
    public void BooleanOpMultiple_WithNoPaths_ReturnsFalse()
    {
        var result = _service.BooleanOpMultiple([], BooleanOperation.Union);

        Assert.False(result.Success);
    }

    [Fact]
    public void BooleanOpMultiple_WithSinglePath_ReturnsThatPath()
    {
        var path = "M0,0 L10,10";
        var result = _service.BooleanOpMultiple([path], BooleanOperation.Union);

        Assert.True(result.Success);
        Assert.Equal(path, result.PathData);
    }

    [Fact]
    public void BooleanOpMultiple_WithMultiplePaths_CombinesThem()
    {
        var paths = new[] { "M0,0 L10,10", "M5,5 L15,15", "M10,10 L20,20" };
        var result = _service.BooleanOpMultiple(paths, BooleanOperation.Union);

        Assert.True(result.Success);
        Assert.NotNull(result.PathData);
    }

    [Fact]
    public void Simplify_WithEmptyPath_ReturnsFalse()
    {
        var result = _service.Simplify("");

        Assert.False(result.Success);
    }

    [Fact]
    public void Simplify_WithValidPath_ReturnsSuccess()
    {
        var result = _service.Simplify("M0,0 L10,10 L20,0 Z");

        Assert.True(result.Success);
        Assert.NotNull(result.PathData);
    }

    [Fact]
    public void Offset_WithEmptyPath_ReturnsFalse()
    {
        var result = _service.Offset("", 5);

        Assert.False(result.Success);
    }

    [Fact]
    public void Offset_WithZeroDistance_ReturnsSamePath()
    {
        var path = "M0,0 L10,10 Z";
        var result = _service.Offset(path, 0);

        Assert.True(result.Success);
        Assert.Equal(path, result.PathData);
    }

    [Theory]
    [InlineData(PathJoinType.Miter)]
    [InlineData(PathJoinType.Round)]
    [InlineData(PathJoinType.Bevel)]
    public void Offset_SupportsAllJoinTypes(PathJoinType joinType)
    {
        var result = _service.Offset("M0,0 L10,10 Z", 5, joinType);

        Assert.True(result.Success);
    }

    [Fact]
    public void StrokeToPath_WithEmptyPath_ReturnsFalse()
    {
        var result = _service.StrokeToPath("", 2);

        Assert.False(result.Success);
    }

    [Fact]
    public void StrokeToPath_WithZeroWidth_ReturnsFalse()
    {
        var result = _service.StrokeToPath("M0,0 L10,10", 0);

        Assert.False(result.Success);
        Assert.Contains("Stroke width", result.ErrorMessage);
    }

    [Fact]
    public void StrokeToPath_WithValidParams_ReturnsSuccess()
    {
        var result = _service.StrokeToPath("M0,0 L10,10", 2);

        Assert.True(result.Success);
        Assert.NotNull(result.PathData);
    }

    [Fact]
    public void TextToPath_WithEmptyText_ReturnsFalse()
    {
        var result = _service.TextToPath("");

        Assert.False(result.Success);
    }

    [Fact]
    public void TextToPath_WithValidText_ReturnsSuccess()
    {
        var result = _service.TextToPath("Hello", "Arial", 24);

        Assert.True(result.Success);
        Assert.NotNull(result.PathData);
    }

    [Fact]
    public void ReversePath_WithEmptyPath_ReturnsFalse()
    {
        var result = _service.ReversePath("");

        Assert.False(result.Success);
    }

    [Fact]
    public void ReversePath_WithValidPath_ReturnsSuccess()
    {
        var result = _service.ReversePath("M0,0 L10,10 Z");

        Assert.True(result.Success);
    }

    [Fact]
    public void ClosePath_WithEmptyPath_ReturnsFalse()
    {
        var result = _service.ClosePath("");

        Assert.False(result.Success);
    }

    [Fact]
    public void ClosePath_WithOpenPath_AddsZ()
    {
        var result = _service.ClosePath("M0,0 L10,10");

        Assert.True(result.Success);
        Assert.EndsWith("Z", result.PathData);
    }

    [Fact]
    public void ClosePath_WithClosedPath_DoesNotDuplicateZ()
    {
        var path = "M0,0 L10,10 Z";
        var result = _service.ClosePath(path);

        Assert.True(result.Success);
        Assert.Equal(path, result.PathData);
    }

    [Fact]
    public void GetPathBounds_WithEmptyPath_ReturnsNull()
    {
        var bounds = _service.GetPathBounds("");

        Assert.Null(bounds);
    }

    [Fact]
    public void GetPathBounds_WithValidPath_ReturnsBounds()
    {
        var bounds = _service.GetPathBounds("M0,0 L10,10 Z");

        Assert.NotNull(bounds);
    }

    [Fact]
    public void ContainsPoint_WithEmptyPath_ReturnsFalse()
    {
        var contains = _service.ContainsPoint("", 5, 5);

        Assert.False(contains);
    }

    [Fact]
    public void SplitPath_WithEmptyPath_ReturnsFalse()
    {
        var (first, second) = _service.SplitPath("", 0.5);

        Assert.False(first.Success);
        Assert.False(second.Success);
    }

    [Fact]
    public void SplitPath_WithValidPath_ReturnsTwoPaths()
    {
        var (first, second) = _service.SplitPath("M0,0 L10,10", 0.5);

        Assert.True(first.Success);
        Assert.True(second.Success);
    }

    [Fact]
    public void FlattenPath_WithEmptyPath_ReturnsFalse()
    {
        var result = _service.FlattenPath("");

        Assert.False(result.Success);
    }

    [Fact]
    public void FlattenPath_WithValidPath_ReturnsSuccess()
    {
        var result = _service.FlattenPath("M0,0 C10,0 10,10 0,10");

        Assert.True(result.Success);
    }

    [Fact]
    public void RectToPath_CreatesValidPath()
    {
        var path = _service.RectToPath(10, 20, 100, 50);

        Assert.Contains("M 10 20", path);
        Assert.EndsWith("Z", path);
    }

    [Fact]
    public void RectToPath_WithRadius_CreatesRoundedPath()
    {
        var path = _service.RectToPath(0, 0, 100, 50, 10, 10);

        Assert.Contains("A", path); // Contains arc commands
        Assert.EndsWith("Z", path);
    }

    [Fact]
    public void EllipseToPath_CreatesValidPath()
    {
        var path = _service.EllipseToPath(50, 50, 30, 20);

        Assert.Contains("A", path);
        Assert.EndsWith("Z", path);
    }

    [Fact]
    public void CircleToPath_CreatesValidPath()
    {
        var path = _service.CircleToPath(50, 50, 25);

        Assert.Contains("A", path);
        Assert.EndsWith("Z", path);
    }

    [Fact]
    public void LineToPath_CreatesValidPath()
    {
        var path = _service.LineToPath(0, 0, 100, 100);

        Assert.Equal("M 0 0 L 100 100", path);
    }

    [Fact]
    public void PolygonToPath_WithEmptyPoints_ReturnsEmpty()
    {
        var path = _service.PolygonToPath("");

        Assert.Empty(path);
    }

    [Fact]
    public void PolygonToPath_CreatesClosedPath()
    {
        var path = _service.PolygonToPath("0,0 100,0 100,100 0,100");

        Assert.StartsWith("M", path);
        Assert.EndsWith("Z", path);
    }

    [Fact]
    public void PolylineToPath_WithEmptyPoints_ReturnsEmpty()
    {
        var path = _service.PolylineToPath("");

        Assert.Empty(path);
    }

    [Fact]
    public void PolylineToPath_CreatesOpenPath()
    {
        var path = _service.PolylineToPath("0,0 100,0 100,100");

        Assert.StartsWith("M", path);
        Assert.DoesNotContain("Z", path);
    }
}
