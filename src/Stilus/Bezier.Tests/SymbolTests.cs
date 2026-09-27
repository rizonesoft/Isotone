namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class SymbolTests
{
    [Fact]
    public void Symbol_DefaultProperties()
    {
        var symbol = new Symbol();

        Assert.Equal("Symbol", symbol.Name);
        Assert.Equal("Uncategorized", symbol.Category);
        Assert.Empty(symbol.Elements);
        Assert.NotEqual(Guid.Empty, symbol.Id);
    }

    [Fact]
    public void Symbol_GetBounds_ReturnsViewBox_WhenEmpty()
    {
        var symbol = new Symbol { ViewBox = (10, 20, 100, 50) };

        var bounds = symbol.GetBounds();

        Assert.Equal((10, 20, 100, 50), bounds);
    }

    [Fact]
    public void Symbol_GetBounds_CalculatesFromElements()
    {
        var symbol = new Symbol();
        symbol.Elements.Add(new SvgRect { X = 0, Y = 0, Width = 50, Height = 50 });
        symbol.Elements.Add(new SvgRect { X = 50, Y = 50, Width = 50, Height = 50 });

        var bounds = symbol.GetBounds();

        Assert.Equal(0, bounds.X);
        Assert.Equal(0, bounds.Y);
        Assert.Equal(100, bounds.Width);
        Assert.Equal(100, bounds.Height);
    }

    [Fact]
    public void Symbol_Clone_CreatesDeepCopy()
    {
        var original = new Symbol
        {
            Name = "Original",
            Category = "Test",
            Description = "Test symbol"
        };
        original.Elements.Add(new SvgRect { X = 10, Y = 10 });

        var clone = original.Clone();

        Assert.NotEqual(original.Id, clone.Id);
        Assert.Contains("Copy", clone.Name);
        Assert.Equal("Test", clone.Category);
        Assert.Single(clone.Elements);
        Assert.NotSame(original.Elements[0], clone.Elements[0]);
    }

    [Fact]
    public void Symbol_MarkModified_UpdatesTimestamp()
    {
        var symbol = new Symbol();
        var original = symbol.ModifiedAt;

        Thread.Sleep(10);
        symbol.MarkModified();

        Assert.True(symbol.ModifiedAt > original);
    }
}

public class SymbolInstanceTests
{
    [Fact]
    public void SymbolInstance_DefaultProperties()
    {
        var instance = new SymbolInstance();

        Assert.Equal(100, instance.Width);
        Assert.Equal(100, instance.Height);
        Assert.True(instance.MaintainAspectRatio);
        Assert.False(instance.IsDetached);
        Assert.Empty(instance.Overrides);
        Assert.False(instance.HasOverrides);
    }

    [Fact]
    public void SymbolInstance_GetBoundingBox_ReturnsCorrectBounds()
    {
        var instance = new SymbolInstance
        {
            X = 10,
            Y = 20,
            Width = 100,
            Height = 50
        };

        var bounds = instance.GetBoundingBox();

        Assert.Equal((10, 20, 100, 50), bounds);
    }

    [Fact]
    public void SymbolInstance_HitTest_ReturnsTrue_WhenInside()
    {
        var instance = new SymbolInstance
        {
            X = 0,
            Y = 0,
            Width = 100,
            Height = 100
        };

        Assert.True(instance.HitTest(50, 50));
        Assert.True(instance.HitTest(0, 0));
        Assert.True(instance.HitTest(100, 100));
    }

    [Fact]
    public void SymbolInstance_HitTest_ReturnsFalse_WhenOutside()
    {
        var instance = new SymbolInstance
        {
            X = 0,
            Y = 0,
            Width = 100,
            Height = 100
        };

        Assert.False(instance.HitTest(-20, -20));
        Assert.False(instance.HitTest(200, 200));
    }

    [Fact]
    public void SymbolInstance_SetOverride_AddsOverride()
    {
        var instance = new SymbolInstance();

        instance.SetOverride("fill", "#FF0000");

        Assert.True(instance.HasOverrides);
        Assert.Single(instance.Overrides);
    }

    [Fact]
    public void SymbolInstance_GetOverride_ReturnsValue()
    {
        var instance = new SymbolInstance();
        instance.SetOverride("opacity", 0.5);

        var value = instance.GetOverride<double>("opacity");

        Assert.Equal(0.5, value);
    }

    [Fact]
    public void SymbolInstance_GetOverride_ReturnsDefault_WhenNotSet()
    {
        var instance = new SymbolInstance();

        var value = instance.GetOverride("missing", "default");

        Assert.Equal("default", value);
    }

    [Fact]
    public void SymbolInstance_RemoveOverride_RemovesIt()
    {
        var instance = new SymbolInstance();
        instance.SetOverride("fill", "#FF0000");

        instance.RemoveOverride("fill");

        Assert.False(instance.HasOverrides);
    }

    [Fact]
    public void SymbolInstance_ClearOverrides_RemovesAll()
    {
        var instance = new SymbolInstance();
        instance.SetOverride("fill", "#FF0000");
        instance.SetOverride("stroke", "#0000FF");

        instance.ClearOverrides();

        Assert.False(instance.HasOverrides);
        Assert.Empty(instance.Overrides);
    }

    [Fact]
    public void SymbolInstance_Clone_CopiesOverrides()
    {
        var original = new SymbolInstance
        {
            X = 10,
            Y = 20,
            Width = 100,
            Height = 50
        };
        original.SetOverride("fill", "#FF0000");

        var clone = (SymbolInstance)original.Clone();

        Assert.Equal(10, clone.X);
        Assert.Equal(20, clone.Y);
        Assert.True(clone.HasOverrides);
        Assert.Equal("#FF0000", clone.Overrides["fill"]);
    }

    [Fact]
    public void SymbolInstance_ToSvgString_GeneratesUseElement()
    {
        var instance = new SymbolInstance
        {
            SymbolId = Guid.Parse("12345678-1234-1234-1234-123456789012"),
            X = 10,
            Y = 20,
            Width = 100,
            Height = 50
        };

        var svg = instance.ToSvgString();

        Assert.Contains("<use", svg);
        Assert.Contains("href=\"#12345678-1234-1234-1234-123456789012\"", svg);
        Assert.Contains("x=\"10\"", svg);
        Assert.Contains("y=\"20\"", svg);
    }
}

public class SymbolLibraryServiceTests
{
    private readonly SymbolLibraryService _library;

    public SymbolLibraryServiceTests()
    {
        _library = new SymbolLibraryService();
    }

    [Fact]
    public void CreateSymbol_AddsToLibrary()
    {
        var elements = new[] { new SvgRect { Width = 50, Height = 50 } };

        var symbol = _library.CreateSymbol("Test", elements);

        Assert.Single(_library.Symbols);
        Assert.Equal("Test", symbol.Name);
        Assert.Single(symbol.Elements);
    }

    [Fact]
    public void AddSymbol_RaisesEvent()
    {
        var raised = false;
        _library.SymbolAdded += (_, _) => raised = true;

        _library.AddSymbol(new Symbol());

        Assert.True(raised);
    }

    [Fact]
    public void RemoveSymbol_RemovesFromLibrary()
    {
        var symbol = _library.CreateSymbol("Test", []);

        var removed = _library.RemoveSymbol(symbol.Id);

        Assert.True(removed);
        Assert.Empty(_library.Symbols);
    }

    [Fact]
    public void RemoveSymbol_RaisesEvent()
    {
        var symbol = _library.CreateSymbol("Test", []);
        var raised = false;
        _library.SymbolRemoved += (_, _) => raised = true;

        _library.RemoveSymbol(symbol.Id);

        Assert.True(raised);
    }

    [Fact]
    public void GetSymbol_ReturnsSymbol()
    {
        var symbol = _library.CreateSymbol("Test", []);

        var found = _library.GetSymbol(symbol.Id);

        Assert.Same(symbol, found);
    }

    [Fact]
    public void GetSymbol_ReturnsNull_WhenNotFound()
    {
        var found = _library.GetSymbol(Guid.NewGuid());

        Assert.Null(found);
    }

    [Fact]
    public void GetSymbolsByCategory_ReturnsMatching()
    {
        _library.CreateSymbol("S1", [], "Category1");
        _library.CreateSymbol("S2", [], "Category2");
        _library.CreateSymbol("S3", [], "Category1");

        var symbols = _library.GetSymbolsByCategory("Category1").ToList();

        Assert.Equal(2, symbols.Count);
    }

    [Fact]
    public void GetCategories_ReturnsUnique()
    {
        _library.CreateSymbol("S1", [], "A");
        _library.CreateSymbol("S2", [], "B");
        _library.CreateSymbol("S3", [], "A");

        var categories = _library.GetCategories().ToList();

        Assert.Equal(2, categories.Count);
        Assert.Contains("A", categories);
        Assert.Contains("B", categories);
    }

    [Fact]
    public void Search_FindsByName()
    {
        _library.CreateSymbol("Arrow", []);
        _library.CreateSymbol("Button", []);
        _library.CreateSymbol("Arrow Icon", []);

        var results = _library.Search("arrow").ToList();

        Assert.Equal(2, results.Count);
    }

    [Fact]
    public void CreateInstance_CreatesLinkedInstance()
    {
        var symbol = _library.CreateSymbol("Test", [], "Test");
        symbol.ViewBox = (0, 0, 100, 50);

        var instance = _library.CreateInstance(symbol.Id, 10, 20);

        Assert.Equal(symbol.Id, instance.SymbolId);
        Assert.Equal(10, instance.X);
        Assert.Equal(20, instance.Y);
        Assert.Equal(100, instance.Width);
        Assert.Equal(50, instance.Height);
    }

    [Fact]
    public void GetInstances_ReturnsRegistered()
    {
        var symbol = _library.CreateSymbol("Test", []);
        _library.CreateInstance(symbol.Id, 0, 0);
        _library.CreateInstance(symbol.Id, 100, 100);

        var instances = _library.GetInstances(symbol.Id);

        Assert.Equal(2, instances.Count);
    }

    [Fact]
    public void GetInstanceCount_ReturnsCount()
    {
        var symbol = _library.CreateSymbol("Test", []);
        _library.CreateInstance(symbol.Id, 0, 0);
        _library.CreateInstance(symbol.Id, 100, 100);

        var count = _library.GetInstanceCount(symbol.Id);

        Assert.Equal(2, count);
    }

    [Fact]
    public void BeginEdit_EntersEditMode()
    {
        var symbol = _library.CreateSymbol("Test", []);

        _library.BeginEdit(symbol.Id);

        Assert.True(_library.IsEditing);
        Assert.Same(symbol, _library.EditingSymbol);
    }

    [Fact]
    public void EndEdit_ExitsEditMode()
    {
        var symbol = _library.CreateSymbol("Test", []);
        _library.BeginEdit(symbol.Id);

        _library.EndEdit();

        Assert.False(_library.IsEditing);
        Assert.Null(_library.EditingSymbol);
    }

    [Fact]
    public void EndEdit_RaisesModifiedEvent()
    {
        var symbol = _library.CreateSymbol("Test", []);
        _library.BeginEdit(symbol.Id);
        var raised = false;
        _library.SymbolModified += (_, _) => raised = true;

        _library.EndEdit();

        Assert.True(raised);
    }

    [Fact]
    public void RenameSymbol_ChangesName()
    {
        var symbol = _library.CreateSymbol("Old Name", []);

        _library.RenameSymbol(symbol.Id, "New Name");

        Assert.Equal("New Name", symbol.Name);
    }

    [Fact]
    public void DuplicateSymbol_CreatesClone()
    {
        var original = _library.CreateSymbol("Original", []);

        var clone = _library.DuplicateSymbol(original.Id);

        Assert.Equal(2, _library.Count);
        Assert.NotEqual(original.Id, clone.Id);
        Assert.Contains("Copy", clone.Name);
    }

    [Fact]
    public void DetachInstance_ReturnsElements()
    {
        var symbol = _library.CreateSymbol("Test", [new SvgRect { Width = 50, Height = 50 }]);
        var instance = _library.CreateInstance(symbol.Id, 100, 100);

        var elements = _library.DetachInstance(instance).ToList();

        Assert.Single(elements);
        Assert.True(instance.IsDetached);
    }

    [Fact]
    public void Clear_RemovesAllSymbols()
    {
        _library.CreateSymbol("S1", []);
        _library.CreateSymbol("S2", []);

        _library.Clear();

        Assert.Equal(0, _library.Count);
    }
}
