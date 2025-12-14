namespace Imago.Core.Layers;

using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// A layer that groups other layers together.
/// </summary>
public sealed partial class GroupLayer : Layer
{
    [ObservableProperty]
    private bool _isExpanded = true;

    public ObservableCollection<Layer> Children { get; } = new();

    public override LayerType LayerType => LayerType.Group;

    public GroupLayer()
    {
        Name = "Group";
    }

    public GroupLayer(string name)
    {
        Name = name;
    }

    public void AddChild(Layer layer)
    {
        ArgumentNullException.ThrowIfNull(layer);
        Children.Add(layer);
    }

    public void RemoveChild(Layer layer)
    {
        ArgumentNullException.ThrowIfNull(layer);
        Children.Remove(layer);
    }

    public override Layer Clone()
    {
        var clone = new GroupLayer(Name + " Copy")
        {
            IsVisible = IsVisible,
            IsLocked = IsLocked,
            Opacity = Opacity,
            BlendMode = BlendMode,
            IsExpanded = IsExpanded
        };

        foreach (var child in Children)
        {
            clone.AddChild(child.Clone());
        }

        return clone;
    }
}
