namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class AlignmentServiceTests
{
    private readonly List<VectorElement> _elements;

    public AlignmentServiceTests()
    {
        // Create test elements at different positions
        _elements =
        [
            new SvgRect { X = 10, Y = 10, Width = 20, Height = 20 },   // Left-top
            new SvgRect { X = 50, Y = 30, Width = 30, Height = 30 },   // Middle
            new SvgRect { X = 100, Y = 60, Width = 40, Height = 40 }   // Right-bottom
        ];
    }

    [Fact]
    public void AlignHorizontal_Left_AlignsToLeftmostEdge()
    {
        var offsets = AlignmentService.AlignHorizontal(
            _elements,
            HorizontalAlignment.Left,
            AlignmentReference.Selection);

        // First element is at X=10, which is the leftmost
        // Second element should move from X=50 to X=10 (offset = -40)
        // Third element should move from X=100 to X=10 (offset = -90)
        Assert.False(offsets.ContainsKey(_elements[0].Id)); // No offset needed
        Assert.Equal(-40, offsets[_elements[1].Id], 0.001);
        Assert.Equal(-90, offsets[_elements[2].Id], 0.001);
    }

    [Fact]
    public void AlignHorizontal_Right_AlignsToRightmostEdge()
    {
        var offsets = AlignmentService.AlignHorizontal(
            _elements,
            HorizontalAlignment.Right,
            AlignmentReference.Selection);

        // Third element right edge is at X=140 (100+40)
        // First element right edge at 30, needs to move +110
        // Second element right edge at 80, needs to move +60
        Assert.Equal(110, offsets[_elements[0].Id], 0.001);
        Assert.Equal(60, offsets[_elements[1].Id], 0.001);
        Assert.False(offsets.ContainsKey(_elements[2].Id)); // No offset needed
    }

    [Fact]
    public void AlignHorizontal_Center_AlignsToCenter()
    {
        var offsets = AlignmentService.AlignHorizontal(
            _elements,
            HorizontalAlignment.Center,
            AlignmentReference.Selection);

        // Combined bounds: X=10 to X=140, center = 75
        // First element center at 20, needs +55
        // Second element center at 65, needs +10
        // Third element center at 120, needs -45
        Assert.Equal(55, offsets[_elements[0].Id], 0.001);
        Assert.Equal(10, offsets[_elements[1].Id], 0.001);
        Assert.Equal(-45, offsets[_elements[2].Id], 0.001);
    }

    [Fact]
    public void AlignVertical_Top_AlignsToTopmostEdge()
    {
        var offsets = AlignmentService.AlignVertical(
            _elements,
            VerticalAlignment.Top,
            AlignmentReference.Selection);

        // First element is at Y=10, which is the topmost
        Assert.False(offsets.ContainsKey(_elements[0].Id));
        Assert.Equal(-20, offsets[_elements[1].Id], 0.001);
        Assert.Equal(-50, offsets[_elements[2].Id], 0.001);
    }

    [Fact]
    public void AlignVertical_Bottom_AlignsToBottommostEdge()
    {
        var offsets = AlignmentService.AlignVertical(
            _elements,
            VerticalAlignment.Bottom,
            AlignmentReference.Selection);

        // Third element bottom at 100 (60+40)
        Assert.Equal(70, offsets[_elements[0].Id], 0.001);
        Assert.Equal(40, offsets[_elements[1].Id], 0.001);
        Assert.False(offsets.ContainsKey(_elements[2].Id));
    }

    [Fact]
    public void AlignVertical_Middle_AlignsToMiddle()
    {
        var offsets = AlignmentService.AlignVertical(
            _elements,
            VerticalAlignment.Middle,
            AlignmentReference.Selection);

        // Combined bounds: Y=10 to Y=100, middle = 55
        // First element middle at 20, needs +35
        // Second element middle at 45, needs +10
        // Third element middle at 80, needs -25
        Assert.Equal(35, offsets[_elements[0].Id], 0.001);
        Assert.Equal(10, offsets[_elements[1].Id], 0.001);
        Assert.Equal(-25, offsets[_elements[2].Id], 0.001);
    }

    [Fact]
    public void AlignHorizontal_ToCanvas_AlignsToCanvasEdge()
    {
        var offsets = AlignmentService.AlignHorizontal(
            _elements,
            HorizontalAlignment.Left,
            AlignmentReference.Canvas,
            canvasWidth: 800);

        // All elements should align to X=0
        Assert.Equal(-10, offsets[_elements[0].Id], 0.001);
        Assert.Equal(-50, offsets[_elements[1].Id], 0.001);
        Assert.Equal(-100, offsets[_elements[2].Id], 0.001);
    }

    [Fact]
    public void AlignHorizontal_ToCanvas_Center()
    {
        var offsets = AlignmentService.AlignHorizontal(
            _elements,
            HorizontalAlignment.Center,
            AlignmentReference.Canvas,
            canvasWidth: 800);

        // All elements should align centers to X=400
        Assert.Equal(380, offsets[_elements[0].Id], 0.001);  // 400 - 20 = 380
        Assert.Equal(335, offsets[_elements[1].Id], 0.001);  // 400 - 65 = 335
        Assert.Equal(280, offsets[_elements[2].Id], 0.001);  // 400 - 120 = 280
    }

    [Fact]
    public void AlignHorizontal_ToKeyObject_AlignsToFirstElement()
    {
        var offsets = AlignmentService.AlignHorizontal(
            _elements,
            HorizontalAlignment.Left,
            AlignmentReference.KeyObject);

        // Align to first element (X=10)
        Assert.False(offsets.ContainsKey(_elements[0].Id));
        Assert.Equal(-40, offsets[_elements[1].Id], 0.001);
        Assert.Equal(-90, offsets[_elements[2].Id], 0.001);
    }

    [Fact]
    public void DistributeHorizontal_DistributesEvenly()
    {
        var offsets = AlignmentService.DistributeHorizontal(_elements);

        // First and last elements don't move
        // Centers: 20, 65, 120 -> span = 100, spacing = 50
        // Middle element center should be at 70 (20 + 50)
        // Current center is 65, so offset = 5
        Assert.False(offsets.ContainsKey(_elements[0].Id));
        Assert.Equal(5, offsets[_elements[1].Id], 0.001);
        Assert.False(offsets.ContainsKey(_elements[2].Id));
    }

    [Fact]
    public void DistributeVertical_DistributesEvenly()
    {
        var offsets = AlignmentService.DistributeVertical(_elements);

        // Centers Y: 20, 45, 80 -> span = 60, spacing = 30
        // Middle element center should be at 50 (20 + 30)
        // Current center is 45, so offset = 5
        Assert.False(offsets.ContainsKey(_elements[0].Id));
        Assert.Equal(5, offsets[_elements[1].Id], 0.001);
        Assert.False(offsets.ContainsKey(_elements[2].Id));
    }

    [Fact]
    public void DistributeHorizontal_WithTwoElements_ReturnsEmpty()
    {
        var twoElements = _elements.Take(2).ToList();

        var offsets = AlignmentService.DistributeHorizontal(twoElements);

        Assert.Empty(offsets);
    }

    [Fact]
    public void DistributeVertical_WithTwoElements_ReturnsEmpty()
    {
        var twoElements = _elements.Take(2).ToList();

        var offsets = AlignmentService.DistributeVertical(twoElements);

        Assert.Empty(offsets);
    }

    [Fact]
    public void GetCombinedBounds_ReturnsCorrectBounds()
    {
        var bounds = AlignmentService.GetCombinedBounds(_elements);

        Assert.Equal(10, bounds.X);
        Assert.Equal(10, bounds.Y);
        Assert.Equal(130, bounds.Width);  // 140 - 10
        Assert.Equal(90, bounds.Height);  // 100 - 10
    }

    [Fact]
    public void GetCombinedBounds_EmptyList_ReturnsZero()
    {
        var bounds = AlignmentService.GetCombinedBounds([]);

        Assert.Equal(0, bounds.X);
        Assert.Equal(0, bounds.Y);
        Assert.Equal(0, bounds.Width);
        Assert.Equal(0, bounds.Height);
    }

    [Fact]
    public void AlignHorizontal_EmptyList_ReturnsEmpty()
    {
        var offsets = AlignmentService.AlignHorizontal(
            [],
            HorizontalAlignment.Left);

        Assert.Empty(offsets);
    }

    [Fact]
    public void AlignVertical_EmptyList_ReturnsEmpty()
    {
        var offsets = AlignmentService.AlignVertical(
            [],
            VerticalAlignment.Top);

        Assert.Empty(offsets);
    }

    [Fact]
    public void DistributeHorizontalGaps_DistributesWithEqualGaps()
    {
        // Create elements with different widths
        var elements = new List<VectorElement>
        {
            new SvgRect { X = 0, Y = 0, Width = 20, Height = 20 },
            new SvgRect { X = 40, Y = 0, Width = 30, Height = 20 },
            new SvgRect { X = 100, Y = 0, Width = 40, Height = 20 }
        };

        var offsets = AlignmentService.DistributeHorizontalGaps(elements);

        // Total span: 0 to 140 = 140
        // Total element width: 20 + 30 + 40 = 90
        // Total gap: 140 - 90 = 50, gap size = 25
        // First element: 0-20
        // Second element should start at: 20 + 25 = 45
        // Current start: 40, offset = 5
        Assert.False(offsets.ContainsKey(elements[0].Id));
        Assert.Equal(5, offsets[elements[1].Id], 0.001);
        Assert.False(offsets.ContainsKey(elements[2].Id));
    }

    [Fact]
    public void DistributeVerticalGaps_DistributesWithEqualGaps()
    {
        var elements = new List<VectorElement>
        {
            new SvgRect { X = 0, Y = 0, Width = 20, Height = 20 },
            new SvgRect { X = 0, Y = 40, Width = 20, Height = 30 },
            new SvgRect { X = 0, Y = 100, Width = 20, Height = 40 }
        };

        var offsets = AlignmentService.DistributeVerticalGaps(elements);

        // Total span: 0 to 140 = 140
        // Total element height: 20 + 30 + 40 = 90
        // Total gap: 140 - 90 = 50, gap size = 25
        // Second element should start at: 20 + 25 = 45
        // Current start: 40, offset = 5
        Assert.False(offsets.ContainsKey(elements[0].Id));
        Assert.Equal(5, offsets[elements[1].Id], 0.001);
        Assert.False(offsets.ContainsKey(elements[2].Id));
    }

    [Fact]
    public void ApplyHorizontalOffsets_MovesElements()
    {
        var elements = new List<VectorElement>
        {
            new SvgRect { X = 10, Y = 10, Width = 20, Height = 20 }
        };
        var offsets = new Dictionary<Guid, double>
        {
            { elements[0].Id, 50 }
        };

        AlignmentService.ApplyHorizontalOffsets(elements, offsets);

        // Check that transform was applied
        Assert.Equal(50, elements[0].Transform.TranslateX);
    }

    [Fact]
    public void ApplyVerticalOffsets_MovesElements()
    {
        var elements = new List<VectorElement>
        {
            new SvgRect { X = 10, Y = 10, Width = 20, Height = 20 }
        };
        var offsets = new Dictionary<Guid, double>
        {
            { elements[0].Id, 30 }
        };

        AlignmentService.ApplyVerticalOffsets(elements, offsets);

        // Check that transform was applied
        Assert.Equal(30, elements[0].Transform.TranslateY);
    }
}
