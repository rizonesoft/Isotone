namespace Bezier.Core.Services;

using System.Collections.ObjectModel;
using Bezier.Core.Models;

/// <summary>
/// Event args for layer events.
/// </summary>
public class LayerEventArgs : EventArgs
{
    public Layer Layer { get; }
    public LayerEventArgs(Layer layer) => Layer = layer;
}

/// <summary>
/// Manages layers in the document.
/// </summary>
public class LayerManager
{
    private Layer? _activeLayer;
    private Layer? _isolationLayer;

    /// <summary>
    /// Gets the root layers collection.
    /// </summary>
    public ObservableCollection<Layer> Layers { get; } = [];

    /// <summary>
    /// Gets or sets the currently active layer.
    /// </summary>
    public Layer? ActiveLayer
    {
        get => _activeLayer;
        set
        {
            if (_activeLayer != value)
            {
                _activeLayer = value;
                ActiveLayerChanged?.Invoke(this, value != null ? new LayerEventArgs(value) : EventArgs.Empty);
            }
        }
    }

    /// <summary>
    /// Gets or sets the isolation mode layer (when editing inside a group).
    /// </summary>
    public Layer? IsolationLayer
    {
        get => _isolationLayer;
        set
        {
            if (_isolationLayer != value)
            {
                _isolationLayer = value;
                IsolationModeChanged?.Invoke(this, EventArgs.Empty);
            }
        }
    }

    /// <summary>
    /// Gets whether isolation mode is active.
    /// </summary>
    public bool IsInIsolationMode => IsolationLayer != null;

    /// <summary>
    /// Event raised when the active layer changes.
    /// </summary>
    public event EventHandler? ActiveLayerChanged;

    /// <summary>
    /// Event raised when layers are modified.
    /// </summary>
    public event EventHandler? LayersChanged;

    /// <summary>
    /// Event raised when isolation mode changes.
    /// </summary>
    public event EventHandler? IsolationModeChanged;

    /// <summary>
    /// Creates a new layer and adds it to the document.
    /// </summary>
    public Layer CreateLayer(string? name = null)
    {
        var layer = new Layer
        {
            Name = name ?? $"Layer {Layers.Count + 1}"
        };

        Layers.Add(layer);
        ActiveLayer ??= layer;
        LayersChanged?.Invoke(this, EventArgs.Empty);

        return layer;
    }

    /// <summary>
    /// Creates a new layer at a specific index.
    /// </summary>
    public Layer CreateLayerAt(int index, string? name = null)
    {
        var layer = new Layer
        {
            Name = name ?? $"Layer {Layers.Count + 1}"
        };

        index = Math.Clamp(index, 0, Layers.Count);
        Layers.Insert(index, layer);
        ActiveLayer ??= layer;
        LayersChanged?.Invoke(this, EventArgs.Empty);

        return layer;
    }

    /// <summary>
    /// Removes a layer from the document.
    /// </summary>
    public bool RemoveLayer(Layer layer)
    {
        // Remove from parent if nested
        if (layer.Parent != null)
        {
            layer.Parent.RemoveChild(layer);
        }
        else
        {
            if (!Layers.Remove(layer))
                return false;
        }

        // Update active layer if needed
        if (ActiveLayer == layer)
        {
            ActiveLayer = Layers.FirstOrDefault();
        }

        LayersChanged?.Invoke(this, EventArgs.Empty);
        return true;
    }

    /// <summary>
    /// Duplicates a layer.
    /// </summary>
    public Layer DuplicateLayer(Layer layer)
    {
        var clone = layer.Clone();

        if (layer.Parent != null)
        {
            var index = layer.Parent.Children.IndexOf(layer);
            layer.Parent.Children.Insert(index + 1, clone);
            clone.Parent = layer.Parent;
        }
        else
        {
            var index = Layers.IndexOf(layer);
            Layers.Insert(index + 1, clone);
        }

        LayersChanged?.Invoke(this, EventArgs.Empty);
        return clone;
    }

    /// <summary>
    /// Moves a layer to a new index.
    /// </summary>
    public void MoveLayer(Layer layer, int newIndex)
    {
        var collection = layer.Parent?.Children ?? Layers;
        var currentIndex = collection.IndexOf(layer);

        if (currentIndex < 0) return;

        newIndex = Math.Clamp(newIndex, 0, collection.Count - 1);
        if (currentIndex == newIndex) return;

        collection.RemoveAt(currentIndex);
        collection.Insert(newIndex, layer);
        LayersChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Moves a layer into a group.
    /// </summary>
    public void MoveLayerIntoGroup(Layer layer, Layer group)
    {
        if (layer == group) return;

        // Remove from current location
        if (layer.Parent != null)
        {
            layer.Parent.RemoveChild(layer);
        }
        else
        {
            Layers.Remove(layer);
        }

        // Add to group
        group.AddChild(layer);
        LayersChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Groups selected layers into a new group.
    /// </summary>
    public Layer GroupLayers(IEnumerable<Layer> layers)
    {
        var layerList = layers.ToList();
        if (layerList.Count == 0) return CreateLayer("Group");

        var group = new Layer { Name = "Group" };

        // Find insertion point (position of first layer)
        var firstLayer = layerList[0];
        var collection = firstLayer.Parent?.Children ?? Layers;
        var insertIndex = collection.IndexOf(firstLayer);

        // Remove layers from their current locations
        foreach (var layer in layerList)
        {
            if (layer.Parent != null)
            {
                layer.Parent.RemoveChild(layer);
            }
            else
            {
                Layers.Remove(layer);
            }

            group.AddChild(layer);
        }

        // Insert group at original position
        collection.Insert(Math.Max(0, insertIndex), group);
        if (firstLayer.Parent != null)
        {
            group.Parent = firstLayer.Parent;
        }

        LayersChanged?.Invoke(this, EventArgs.Empty);
        return group;
    }

    /// <summary>
    /// Ungroups a layer, moving its children to its parent.
    /// </summary>
    public void UngroupLayer(Layer group)
    {
        if (!group.IsGroup) return;

        var collection = group.Parent?.Children ?? Layers;
        var index = collection.IndexOf(group);
        if (index < 0) return;

        // Remove group first
        collection.RemoveAt(index);

        // Move children to group's former position
        var children = group.Children.ToList();
        var insertIndex = index;
        foreach (var child in children)
        {
            child.Parent = group.Parent;
            collection.Insert(insertIndex++, child);
        }

        // Clear children from group
        group.Children.Clear();
        LayersChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Toggles visibility of a layer.
    /// </summary>
    public void ToggleVisibility(Layer layer)
    {
        layer.IsVisible = !layer.IsVisible;
        LayersChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Solos a layer (hides all others).
    /// </summary>
    public void SoloLayer(Layer targetLayer)
    {
        foreach (var layer in GetAllLayers())
        {
            layer.IsVisible = layer == targetLayer || IsAncestorOf(layer, targetLayer);
        }
        LayersChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Toggles lock state of a layer.
    /// </summary>
    public void ToggleLock(Layer layer)
    {
        layer.IsLocked = !layer.IsLocked;
        LayersChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Enters isolation mode for a group.
    /// </summary>
    public void EnterIsolationMode(Layer group)
    {
        if (!group.IsGroup) return;
        IsolationLayer = group;
    }

    /// <summary>
    /// Exits isolation mode.
    /// </summary>
    public void ExitIsolationMode()
    {
        IsolationLayer = null;
    }

    /// <summary>
    /// Gets the breadcrumb path for isolation mode.
    /// </summary>
    public IEnumerable<Layer> GetIsolationBreadcrumb()
    {
        var path = new List<Layer>();
        var current = IsolationLayer;

        while (current != null)
        {
            path.Insert(0, current);
            current = current.Parent;
        }

        return path;
    }

    /// <summary>
    /// Merges multiple layers into one.
    /// </summary>
    public Layer MergeLayers(IEnumerable<Layer> layers)
    {
        var layerList = layers.ToList();
        if (layerList.Count == 0) return CreateLayer("Merged");

        var merged = new Layer { Name = "Merged" };

        // Collect all elements
        foreach (var layer in layerList)
        {
            foreach (var element in layer.GetAllElements())
            {
                merged.AddElement(element.Clone());
            }
        }

        // Insert at first layer's position
        var firstLayer = layerList[0];
        var collection = firstLayer.Parent?.Children ?? Layers;
        var insertIndex = collection.IndexOf(firstLayer);

        // Remove original layers
        foreach (var layer in layerList)
        {
            RemoveLayer(layer);
        }

        collection.Insert(Math.Max(0, insertIndex), merged);
        LayersChanged?.Invoke(this, EventArgs.Empty);

        return merged;
    }

    /// <summary>
    /// Gets all layers recursively.
    /// </summary>
    public IEnumerable<Layer> GetAllLayers()
    {
        foreach (var layer in Layers)
        {
            yield return layer;
            foreach (var child in GetAllLayersRecursive(layer))
            {
                yield return child;
            }
        }
    }

    /// <summary>
    /// Finds a layer by ID.
    /// </summary>
    public Layer? FindLayer(Guid id)
    {
        return GetAllLayers().FirstOrDefault(l => l.Id == id);
    }

    /// <summary>
    /// Finds which layer contains an element.
    /// </summary>
    public Layer? FindLayerContaining(VectorElement element)
    {
        return GetAllLayers().FirstOrDefault(l => l.Elements.Contains(element));
    }

    /// <summary>
    /// Gets all visible elements from all layers.
    /// </summary>
    public IEnumerable<VectorElement> GetAllVisibleElements()
    {
        foreach (var layer in Layers)
        {
            foreach (var element in layer.GetVisibleElements())
            {
                yield return element;
            }
        }
    }

    /// <summary>
    /// Renames a layer.
    /// </summary>
    public void RenameLayer(Layer layer, string newName)
    {
        layer.Name = newName;
        LayersChanged?.Invoke(this, EventArgs.Empty);
    }

    private IEnumerable<Layer> GetAllLayersRecursive(Layer parent)
    {
        foreach (var child in parent.Children)
        {
            yield return child;
            foreach (var grandchild in GetAllLayersRecursive(child))
            {
                yield return grandchild;
            }
        }
    }

    private bool IsAncestorOf(Layer ancestor, Layer descendant)
    {
        var current = descendant.Parent;
        while (current != null)
        {
            if (current == ancestor) return true;
            current = current.Parent;
        }
        return false;
    }
}
