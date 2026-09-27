namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Services;

public class ArtboardTests
{
    [Fact]
    public void Artboard_DefaultProperties()
    {
        var artboard = new Artboard();

        Assert.Equal("Artboard", artboard.Name);
        Assert.Equal(0, artboard.X);
        Assert.Equal(0, artboard.Y);
        Assert.Equal(800, artboard.Width);
        Assert.Equal(600, artboard.Height);
        Assert.Equal(0xFFFFFFFFu, artboard.BackgroundColor);
        Assert.True(artboard.ShowBackground);
        Assert.False(artboard.IsSelected);
    }

    [Fact]
    public void Artboard_Bounds_ReturnsCorrectValue()
    {
        var artboard = new Artboard { X = 10, Y = 20, Width = 100, Height = 50 };

        Assert.Equal((10, 20, 100, 50), artboard.Bounds);
    }

    [Fact]
    public void Artboard_Center_ReturnsCorrectValue()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 50 };

        Assert.Equal((50, 25), artboard.Center);
    }

    [Fact]
    public void Artboard_ContainsPoint_ReturnsTrue_WhenInside()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };

        Assert.True(artboard.ContainsPoint(50, 50));
        Assert.True(artboard.ContainsPoint(0, 0));
        Assert.True(artboard.ContainsPoint(100, 100));
    }

    [Fact]
    public void Artboard_ContainsPoint_ReturnsFalse_WhenOutside()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };

        Assert.False(artboard.ContainsPoint(-10, 50));
        Assert.False(artboard.ContainsPoint(50, -10));
        Assert.False(artboard.ContainsPoint(110, 50));
        Assert.False(artboard.ContainsPoint(50, 110));
    }

    [Fact]
    public void Artboard_HitTestBorder_ReturnsTrueOnEdge()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };

        Assert.True(artboard.HitTestBorder(2, 50)); // Left edge
        Assert.True(artboard.HitTestBorder(98, 50)); // Right edge
        Assert.True(artboard.HitTestBorder(50, 2)); // Top edge
        Assert.True(artboard.HitTestBorder(50, 98)); // Bottom edge
    }

    [Fact]
    public void Artboard_HitTestBorder_ReturnsFalseInCenter()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };

        Assert.False(artboard.HitTestBorder(50, 50));
    }

    [Fact]
    public void Artboard_HitTestTitle_ReturnsTrueAboveArtboard()
    {
        var artboard = new Artboard { X = 0, Y = 100, Width = 100, Height = 100 };

        Assert.True(artboard.HitTestTitle(50, 90));
        Assert.False(artboard.HitTestTitle(50, 150));
    }

    [Fact]
    public void Artboard_GetResizeHandle_ReturnsCornerHandles()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };

        Assert.Equal(ResizeHandle.TopLeft, artboard.GetResizeHandle(0, 0));
        Assert.Equal(ResizeHandle.TopRight, artboard.GetResizeHandle(100, 0));
        Assert.Equal(ResizeHandle.BottomLeft, artboard.GetResizeHandle(0, 100));
        Assert.Equal(ResizeHandle.BottomRight, artboard.GetResizeHandle(100, 100));
    }

    [Fact]
    public void Artboard_GetResizeHandle_ReturnsEdgeHandles()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };

        Assert.Equal(ResizeHandle.Top, artboard.GetResizeHandle(50, 0));
        Assert.Equal(ResizeHandle.Bottom, artboard.GetResizeHandle(50, 100));
        Assert.Equal(ResizeHandle.Left, artboard.GetResizeHandle(0, 50));
        Assert.Equal(ResizeHandle.Right, artboard.GetResizeHandle(100, 50));
    }

    [Fact]
    public void Artboard_GetResizeHandle_ReturnsNull_WhenNoHandle()
    {
        var artboard = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };

        Assert.Null(artboard.GetResizeHandle(50, 50));
    }

    [Fact]
    public void Artboard_ApplyPreset_SetsSize()
    {
        var artboard = new Artboard();

        artboard.ApplyPreset("Instagram Post");

        Assert.Equal(1080, artboard.Width);
        Assert.Equal(1080, artboard.Height);
    }

    [Fact]
    public void Artboard_Clone_CreatesDeepCopy()
    {
        var original = new Artboard
        {
            Name = "Original",
            X = 10,
            Y = 20,
            Width = 300,
            Height = 200,
            BackgroundColor = 0xFF0000FF
        };

        var clone = original.Clone();

        Assert.NotEqual(original.Id, clone.Id);
        Assert.Contains("Copy", clone.Name);
        Assert.Equal(60, clone.X); // Offset by 50
        Assert.Equal(70, clone.Y);
        Assert.Equal(300, clone.Width);
        Assert.Equal(200, clone.Height);
    }

    [Fact]
    public void Artboard_Intersects_ReturnsTrue_WhenOverlapping()
    {
        var a = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };
        var b = new Artboard { X = 50, Y = 50, Width = 100, Height = 100 };

        Assert.True(a.Intersects(b));
        Assert.True(b.Intersects(a));
    }

    [Fact]
    public void Artboard_Intersects_ReturnsFalse_WhenNotOverlapping()
    {
        var a = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };
        var b = new Artboard { X = 200, Y = 200, Width = 100, Height = 100 };

        Assert.False(a.Intersects(b));
    }

    [Fact]
    public void Artboard_GetIntersection_ReturnsOverlapArea()
    {
        var a = new Artboard { X = 0, Y = 0, Width = 100, Height = 100 };
        var b = new Artboard { X = 50, Y = 50, Width = 100, Height = 100 };

        var intersection = a.GetIntersection(b);

        Assert.NotNull(intersection);
        Assert.Equal(50, intersection.Value.X);
        Assert.Equal(50, intersection.Value.Y);
        Assert.Equal(50, intersection.Value.Width);
        Assert.Equal(50, intersection.Value.Height);
    }
}

public class ArtboardPresetsTests
{
    [Fact]
    public void ArtboardPresets_ContainsExpectedPresets()
    {
        Assert.True(ArtboardPresets.Presets.Length > 0);
        Assert.Contains(ArtboardPresets.Presets, p => p.Name == "Desktop HD");
        Assert.Contains(ArtboardPresets.Presets, p => p.Name == "Instagram Post");
        Assert.Contains(ArtboardPresets.Presets, p => p.Name == "A4 Portrait");
    }

    [Fact]
    public void ArtboardPresets_FindPreset_ReturnsPreset()
    {
        var preset = ArtboardPresets.FindPreset("Instagram Post");

        Assert.NotNull(preset);
        Assert.Equal(1080, preset.Value.Width);
        Assert.Equal(1080, preset.Value.Height);
    }

    [Fact]
    public void ArtboardPresets_FindPreset_ReturnsNull_WhenNotFound()
    {
        var preset = ArtboardPresets.FindPreset("NonExistent");

        Assert.Null(preset);
    }
}

public class ArtboardManagerTests
{
    private readonly ArtboardManager _manager;

    public ArtboardManagerTests()
    {
        _manager = new ArtboardManager();
    }

    [Fact]
    public void CreateArtboard_AddsToCollection()
    {
        var artboard = _manager.CreateArtboard(0, 0, 800, 600);

        Assert.Single(_manager.Artboards);
        Assert.Same(artboard, _manager.ActiveArtboard);
    }

    [Fact]
    public void CreateArtboard_AssignsUniqueName()
    {
        var a1 = _manager.CreateArtboard();
        var a2 = _manager.CreateArtboard();

        Assert.NotEqual(a1.Name, a2.Name);
    }

    [Fact]
    public void CreateFromPreset_UsesPresetSize()
    {
        var artboard = _manager.CreateFromPreset("Instagram Post");

        Assert.Equal(1080, artboard.Width);
        Assert.Equal(1080, artboard.Height);
    }

    [Fact]
    public void CreateFromPreset_ThrowsForInvalidPreset()
    {
        Assert.Throws<ArgumentException>(() => _manager.CreateFromPreset("Invalid"));
    }

    [Fact]
    public void RemoveArtboard_RemovesFromCollection()
    {
        var artboard = _manager.CreateArtboard();

        var removed = _manager.RemoveArtboard(artboard);

        Assert.True(removed);
        Assert.Empty(_manager.Artboards);
    }

    [Fact]
    public void RemoveArtboard_UpdatesActiveArtboard()
    {
        var a1 = _manager.CreateArtboard();
        var a2 = _manager.CreateArtboard();
        _manager.ActiveArtboard = a1;

        _manager.RemoveArtboard(a1);

        Assert.Same(a2, _manager.ActiveArtboard);
    }

    [Fact]
    public void GetArtboard_FindsById()
    {
        var artboard = _manager.CreateArtboard();

        var found = _manager.GetArtboard(artboard.Id);

        Assert.Same(artboard, found);
    }

    [Fact]
    public void GetArtboardByName_FindsByName()
    {
        var artboard = _manager.CreateArtboard();
        artboard.Name = "TestBoard";

        var found = _manager.GetArtboardByName("TestBoard");

        Assert.Same(artboard, found);
    }

    [Fact]
    public void GetArtboardAtPoint_ReturnsTopmost()
    {
        var a1 = _manager.CreateArtboard(0, 0, 100, 100);
        var a2 = _manager.CreateArtboard(50, 50, 100, 100);

        var found = _manager.GetArtboardAtPoint(75, 75);

        Assert.Same(a2, found);
    }

    [Fact]
    public void DuplicateArtboard_CreatesClone()
    {
        var original = _manager.CreateArtboard(0, 0, 100, 100);
        original.Name = "Original";

        var clone = _manager.DuplicateArtboard(original);

        Assert.Equal(2, _manager.Count);
        Assert.NotEqual(original.Id, clone.Id);
    }

    [Fact]
    public void NavigateNext_CyclesToNextArtboard()
    {
        var a1 = _manager.CreateArtboard();
        var a2 = _manager.CreateArtboard();
        var a3 = _manager.CreateArtboard();
        _manager.ActiveArtboard = a1;

        var next = _manager.NavigateNext();

        Assert.Same(a2, next);
    }

    [Fact]
    public void NavigatePrevious_CyclesToPreviousArtboard()
    {
        var a1 = _manager.CreateArtboard();
        var a2 = _manager.CreateArtboard();
        var a3 = _manager.CreateArtboard();
        _manager.ActiveArtboard = a3;

        var prev = _manager.NavigatePrevious();

        Assert.Same(a2, prev);
    }

    [Fact]
    public void GetCombinedBounds_ReturnsAllArtboardsBounds()
    {
        _manager.CreateArtboard(0, 0, 100, 100);
        _manager.CreateArtboard(200, 200, 100, 100);

        var bounds = _manager.GetCombinedBounds();

        Assert.NotNull(bounds);
        Assert.Equal(0, bounds.Value.X);
        Assert.Equal(0, bounds.Value.Y);
        Assert.Equal(300, bounds.Value.Width);
        Assert.Equal(300, bounds.Value.Height);
    }

    [Fact]
    public void ArrangeHorizontally_PositionsArtboards()
    {
        var a1 = _manager.CreateArtboard(0, 0, 100, 100);
        var a2 = _manager.CreateArtboard(0, 0, 100, 100);
        var a3 = _manager.CreateArtboard(0, 0, 100, 100);

        _manager.ArrangeHorizontally(50);

        Assert.Equal(0, a1.X);
        Assert.Equal(150, a2.X);
        Assert.Equal(300, a3.X);
    }

    [Fact]
    public void ArrangeVertically_PositionsArtboards()
    {
        var a1 = _manager.CreateArtboard(0, 0, 100, 100);
        var a2 = _manager.CreateArtboard(0, 0, 100, 100);

        _manager.ArrangeVertically(50);

        Assert.Equal(0, a1.Y);
        Assert.Equal(150, a2.Y);
    }

    [Fact]
    public void BringToFront_MovesToEnd()
    {
        var a1 = _manager.CreateArtboard();
        var a2 = _manager.CreateArtboard();
        var a3 = _manager.CreateArtboard();

        _manager.BringToFront(a1);

        Assert.Same(a1, _manager.Artboards[^1]);
    }

    [Fact]
    public void SendToBack_MovesToStart()
    {
        var a1 = _manager.CreateArtboard();
        var a2 = _manager.CreateArtboard();
        var a3 = _manager.CreateArtboard();

        _manager.SendToBack(a3);

        Assert.Same(a3, _manager.Artboards[0]);
    }

    [Fact]
    public void Clear_RemovesAllArtboards()
    {
        _manager.CreateArtboard();
        _manager.CreateArtboard();

        _manager.Clear();

        Assert.Equal(0, _manager.Count);
        Assert.Null(_manager.ActiveArtboard);
    }

    [Fact]
    public void ActiveArtboardChanged_EventRaised()
    {
        var raised = false;
        _manager.ActiveArtboardChanged += (_, _) => raised = true;

        _manager.CreateArtboard();

        Assert.True(raised);
    }

    [Fact]
    public void ArtboardAdded_EventRaised()
    {
        Artboard? addedArtboard = null;
        _manager.ArtboardAdded += (_, e) => addedArtboard = e.Artboard;

        var artboard = _manager.CreateArtboard();

        Assert.Same(artboard, addedArtboard);
    }

    [Fact]
    public void ArtboardRemoved_EventRaised()
    {
        var artboard = _manager.CreateArtboard();
        Artboard? removedArtboard = null;
        _manager.ArtboardRemoved += (_, e) => removedArtboard = e.Artboard;

        _manager.RemoveArtboard(artboard);

        Assert.Same(artboard, removedArtboard);
    }
}
