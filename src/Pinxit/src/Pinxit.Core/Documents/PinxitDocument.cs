namespace Pinxit.Core.Documents;

using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using Pinxit.Core.Layers;

/// <summary>
/// Represents an Pinxit document containing layers and metadata.
/// </summary>
public sealed partial class PinxitDocument : ObservableObject
{
    [ObservableProperty]
    private string _name = "Untitled";

    [ObservableProperty]
    private string? _filePath;

    [ObservableProperty]
    private int _width;

    [ObservableProperty]
    private int _height;

    [ObservableProperty]
    private int _bitDepth = 8;

    [ObservableProperty]
    private ColorSpace _colorSpace = ColorSpace.SRGB;

    [ObservableProperty]
    private double _resolution = 72.0;

    [ObservableProperty]
    private bool _isDirty;

    [ObservableProperty]
    private Layer? _activeLayer;

    public ObservableCollection<Layer> Layers { get; } = new();

    public DateTime CreatedAt { get; } = DateTime.UtcNow;

    public DateTime ModifiedAt { get; private set; } = DateTime.UtcNow;

    public PinxitDocument(int width, int height)
    {
        Width = width;
        Height = height;
    }

    public void AddLayer(Layer layer)
    {
        ArgumentNullException.ThrowIfNull(layer);
        Layers.Add(layer);
        ActiveLayer ??= layer;
        MarkDirty();
    }

    public void RemoveLayer(Layer layer)
    {
        ArgumentNullException.ThrowIfNull(layer);
        Layers.Remove(layer);

        if (ActiveLayer == layer)
        {
            ActiveLayer = Layers.FirstOrDefault();
        }

        MarkDirty();
    }

    public void MoveLayer(int fromIndex, int toIndex)
    {
        if (fromIndex < 0 || fromIndex >= Layers.Count)
        {
            throw new ArgumentOutOfRangeException(nameof(fromIndex));
        }

        if (toIndex < 0 || toIndex >= Layers.Count)
        {
            throw new ArgumentOutOfRangeException(nameof(toIndex));
        }

        Layers.Move(fromIndex, toIndex);
        MarkDirty();
    }

    public void MarkDirty()
    {
        IsDirty = true;
        ModifiedAt = DateTime.UtcNow;
    }

    public void MarkClean()
    {
        IsDirty = false;
    }
}
