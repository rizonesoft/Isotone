namespace Bezier.Tests;

using Bezier.Core.Models;
using Bezier.Core.Models.Elements;
using Bezier.Core.Services;

public class LayerTests
{
    [Fact]
    public void Layer_DefaultProperties()
    {
        var layer = new Layer();

        Assert.Equal("Layer", layer.Name);
        Assert.True(layer.IsVisible);
        Assert.False(layer.IsLocked);
        Assert.True(layer.IsExpanded);
        Assert.Equal(1.0, layer.Opacity);
        Assert.Equal(BlendMode.Normal, layer.BlendMode);
        Assert.Null(layer.Parent);
        Assert.Empty(layer.Elements);
        Assert.Empty(layer.Children);
        Assert.False(layer.IsGroup);
    }

    [Fact]
    public void AddElement_AddsToElements()
    {
        var layer = new Layer();
        var rect = new SvgRect();

        layer.AddElement(rect);

        Assert.Single(layer.Elements);
        Assert.Contains(rect, layer.Elements);
    }

    [Fact]
    public void RemoveElement_RemovesFromElements()
    {
        var layer = new Layer();
        var rect = new SvgRect();
        layer.AddElement(rect);

        var removed = layer.RemoveElement(rect);

        Assert.True(removed);
        Assert.Empty(layer.Elements);
    }

    [Fact]
    public void AddChild_SetsParent()
    {
        var parent = new Layer { Name = "Parent" };
        var child = new Layer { Name = "Child" };

        parent.AddChild(child);

        Assert.Single(parent.Children);
        Assert.Same(parent, child.Parent);
        Assert.True(parent.IsGroup);
    }

    [Fact]
    public void RemoveChild_ClearsParent()
    {
        var parent = new Layer { Name = "Parent" };
        var child = new Layer { Name = "Child" };
        parent.AddChild(child);

        var removed = parent.RemoveChild(child);

        Assert.True(removed);
        Assert.Empty(parent.Children);
        Assert.Null(child.Parent);
    }

    [Fact]
    public void Depth_ReturnsCorrectValue()
    {
        var root = new Layer { Name = "Root" };
        var child = new Layer { Name = "Child" };
        var grandchild = new Layer { Name = "Grandchild" };

        root.AddChild(child);
        child.AddChild(grandchild);

        Assert.Equal(0, root.Depth);
        Assert.Equal(1, child.Depth);
        Assert.Equal(2, grandchild.Depth);
    }

    [Fact]
    public void IsEffectivelyVisible_ConsidersParent()
    {
        var parent = new Layer { Name = "Parent", IsVisible = false };
        var child = new Layer { Name = "Child", IsVisible = true };
        parent.AddChild(child);

        Assert.False(child.IsEffectivelyVisible);
    }

    [Fact]
    public void IsEffectivelyLocked_ConsidersParent()
    {
        var parent = new Layer { Name = "Parent", IsLocked = true };
        var child = new Layer { Name = "Child", IsLocked = false };
        parent.AddChild(child);

        Assert.True(child.IsEffectivelyLocked);
    }

    [Fact]
    public void GetAllElements_ReturnsNestedElements()
    {
        var parent = new Layer { Name = "Parent" };
        var child = new Layer { Name = "Child" };
        parent.AddChild(child);

        parent.AddElement(new SvgRect { Name = "Rect1" });
        child.AddElement(new SvgRect { Name = "Rect2" });

        var elements = parent.GetAllElements().ToList();

        Assert.Equal(2, elements.Count);
    }

    [Fact]
    public void GetVisibleElements_FiltersHidden()
    {
        var layer = new Layer();
        layer.AddElement(new SvgRect { Name = "Visible", IsVisible = true });
        layer.AddElement(new SvgRect { Name = "Hidden", IsVisible = false });

        var visible = layer.GetVisibleElements().ToList();

        Assert.Single(visible);
        Assert.Equal("Visible", visible[0].Name);
    }

    [Fact]
    public void Clone_CreatesDeepCopy()
    {
        var original = new Layer { Name = "Original", Opacity = 0.5 };
        original.AddElement(new SvgRect { Name = "Rect" });

        var clone = original.Clone();

        Assert.NotEqual(original.Id, clone.Id);
        Assert.Contains("Copy", clone.Name);
        Assert.Equal(0.5, clone.Opacity);
        Assert.Single(clone.Elements);
    }
}

public class LayerManagerTests
{
    private readonly LayerManager _manager;

    public LayerManagerTests()
    {
        _manager = new LayerManager();
    }

    [Fact]
    public void CreateLayer_AddsToLayers()
    {
        var layer = _manager.CreateLayer("Test");

        Assert.Single(_manager.Layers);
        Assert.Equal("Test", layer.Name);
        Assert.Same(layer, _manager.ActiveLayer);
    }

    [Fact]
    public void CreateLayerAt_InsertsAtIndex()
    {
        _manager.CreateLayer("First");
        _manager.CreateLayer("Third");
        _manager.CreateLayerAt(1, "Second");

        Assert.Equal(3, _manager.Layers.Count);
        Assert.Equal("Second", _manager.Layers[1].Name);
    }

    [Fact]
    public void RemoveLayer_RemovesFromLayers()
    {
        var layer = _manager.CreateLayer("Test");

        var removed = _manager.RemoveLayer(layer);

        Assert.True(removed);
        Assert.Empty(_manager.Layers);
    }

    [Fact]
    public void RemoveLayer_UpdatesActiveLayer()
    {
        var layer1 = _manager.CreateLayer("Layer 1");
        var layer2 = _manager.CreateLayer("Layer 2");
        _manager.ActiveLayer = layer1;

        _manager.RemoveLayer(layer1);

        Assert.Same(layer2, _manager.ActiveLayer);
    }

    [Fact]
    public void DuplicateLayer_CreatesClone()
    {
        var original = _manager.CreateLayer("Original");
        original.AddElement(new SvgRect());

        var duplicate = _manager.DuplicateLayer(original);

        Assert.Equal(2, _manager.Layers.Count);
        Assert.Contains("Copy", duplicate.Name);
        Assert.Single(duplicate.Elements);
    }

    [Fact]
    public void MoveLayer_ChangesOrder()
    {
        var layer1 = _manager.CreateLayer("Layer 1");
        var layer2 = _manager.CreateLayer("Layer 2");
        var layer3 = _manager.CreateLayer("Layer 3");

        _manager.MoveLayer(layer3, 0);

        Assert.Same(layer3, _manager.Layers[0]);
        Assert.Same(layer1, _manager.Layers[1]);
    }

    [Fact]
    public void GroupLayers_CreatesGroup()
    {
        var layer1 = _manager.CreateLayer("Layer 1");
        var layer2 = _manager.CreateLayer("Layer 2");

        var group = _manager.GroupLayers([layer1, layer2]);

        Assert.Single(_manager.Layers);
        Assert.Equal("Group", group.Name);
        Assert.Equal(2, group.Children.Count);
    }

    [Fact]
    public void UngroupLayer_MovesChildrenOut()
    {
        // Create a group with children directly
        var group = _manager.CreateLayer("Group");
        var child1 = new Layer { Name = "Child 1" };
        var child2 = new Layer { Name = "Child 2" };
        group.AddChild(child1);
        group.AddChild(child2);

        Assert.Single(_manager.Layers);
        Assert.Equal(2, group.Children.Count);

        _manager.UngroupLayer(group);

        Assert.Equal(2, _manager.Layers.Count);
        Assert.DoesNotContain(group, _manager.Layers);
    }

    [Fact]
    public void ToggleVisibility_TogglesState()
    {
        var layer = _manager.CreateLayer("Test");
        Assert.True(layer.IsVisible);

        _manager.ToggleVisibility(layer);

        Assert.False(layer.IsVisible);
    }

    [Fact]
    public void ToggleLock_TogglesState()
    {
        var layer = _manager.CreateLayer("Test");
        Assert.False(layer.IsLocked);

        _manager.ToggleLock(layer);

        Assert.True(layer.IsLocked);
    }

    [Fact]
    public void SoloLayer_HidesOthers()
    {
        var layer1 = _manager.CreateLayer("Layer 1");
        var layer2 = _manager.CreateLayer("Layer 2");
        var layer3 = _manager.CreateLayer("Layer 3");

        _manager.SoloLayer(layer2);

        Assert.False(layer1.IsVisible);
        Assert.True(layer2.IsVisible);
        Assert.False(layer3.IsVisible);
    }

    [Fact]
    public void EnterIsolationMode_SetsIsolationLayer()
    {
        var layer = _manager.CreateLayer("Group");
        layer.AddChild(new Layer { Name = "Child" });

        _manager.EnterIsolationMode(layer);

        Assert.Same(layer, _manager.IsolationLayer);
        Assert.True(_manager.IsInIsolationMode);
    }

    [Fact]
    public void ExitIsolationMode_ClearsIsolationLayer()
    {
        var layer = _manager.CreateLayer("Group");
        layer.AddChild(new Layer { Name = "Child" });
        _manager.EnterIsolationMode(layer);

        _manager.ExitIsolationMode();

        Assert.Null(_manager.IsolationLayer);
        Assert.False(_manager.IsInIsolationMode);
    }

    [Fact]
    public void GetAllLayers_ReturnsNested()
    {
        var parent = _manager.CreateLayer("Parent");
        var child = new Layer { Name = "Child" };
        parent.AddChild(child);

        var all = _manager.GetAllLayers().ToList();

        Assert.Equal(2, all.Count);
        Assert.Contains(parent, all);
        Assert.Contains(child, all);
    }

    [Fact]
    public void FindLayer_FindsById()
    {
        var layer = _manager.CreateLayer("Test");

        var found = _manager.FindLayer(layer.Id);

        Assert.Same(layer, found);
    }

    [Fact]
    public void FindLayerContaining_FindsElement()
    {
        var layer = _manager.CreateLayer("Test");
        var rect = new SvgRect();
        layer.AddElement(rect);

        var found = _manager.FindLayerContaining(rect);

        Assert.Same(layer, found);
    }

    [Fact]
    public void MergeLayers_CombinesElements()
    {
        var layer1 = _manager.CreateLayer("Layer 1");
        layer1.AddElement(new SvgRect { Name = "Rect1" });
        var layer2 = _manager.CreateLayer("Layer 2");
        layer2.AddElement(new SvgRect { Name = "Rect2" });

        var merged = _manager.MergeLayers([layer1, layer2]);

        Assert.Single(_manager.Layers);
        Assert.Equal("Merged", merged.Name);
        Assert.Equal(2, merged.Elements.Count);
    }

    [Fact]
    public void RenameLayer_ChangesName()
    {
        var layer = _manager.CreateLayer("Old Name");

        _manager.RenameLayer(layer, "New Name");

        Assert.Equal("New Name", layer.Name);
    }

    [Fact]
    public void ActiveLayerChanged_EventRaised()
    {
        var raised = false;
        _manager.ActiveLayerChanged += (_, _) => raised = true;

        _manager.CreateLayer("Test");

        Assert.True(raised);
    }

    [Fact]
    public void LayersChanged_EventRaised()
    {
        var raised = false;
        _manager.LayersChanged += (_, _) => raised = true;

        _manager.CreateLayer("Test");

        Assert.True(raised);
    }
}
