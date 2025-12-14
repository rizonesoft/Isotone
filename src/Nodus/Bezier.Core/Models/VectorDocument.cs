using System.Collections.ObjectModel;
using System.ComponentModel;

namespace Bezier.Core.Models;

/// <summary>
/// Represents the SVG viewBox attribute.
/// </summary>
public struct ViewBox
{
    public double MinX { get; set; }
    public double MinY { get; set; }
    public double Width { get; set; }
    public double Height { get; set; }

    public ViewBox(double minX, double minY, double width, double height)
    {
        MinX = minX;
        MinY = minY;
        Width = width;
        Height = height;
    }

    public override string ToString() => $"{MinX} {MinY} {Width} {Height}";
}

/// <summary>
/// Represents an SVG document with all its elements and metadata.
/// </summary>
public class VectorDocument : INotifyPropertyChanged
{
    private double _width = 800;
    private double _height = 600;
    private ViewBox _viewBox = new(0, 0, 800, 600);
    private string _title = "Untitled";
    private string _author = string.Empty;
    private string _description = string.Empty;
    private string _license = string.Empty;
    private bool _isDirty;

    public event PropertyChangedEventHandler? PropertyChanged;

    /// <summary>
    /// Document width in pixels.
    /// </summary>
    public double Width
    {
        get => _width;
        set { _width = value; OnPropertyChanged(nameof(Width)); IsDirty = true; }
    }

    /// <summary>
    /// Document height in pixels.
    /// </summary>
    public double Height
    {
        get => _height;
        set { _height = value; OnPropertyChanged(nameof(Height)); IsDirty = true; }
    }

    /// <summary>
    /// SVG viewBox for coordinate system mapping.
    /// </summary>
    public ViewBox ViewBox
    {
        get => _viewBox;
        set { _viewBox = value; OnPropertyChanged(nameof(ViewBox)); IsDirty = true; }
    }

    /// <summary>
    /// Document title.
    /// </summary>
    public string Title
    {
        get => _title;
        set { _title = value; OnPropertyChanged(nameof(Title)); IsDirty = true; }
    }

    /// <summary>
    /// Document author.
    /// </summary>
    public string Author
    {
        get => _author;
        set { _author = value; OnPropertyChanged(nameof(Author)); IsDirty = true; }
    }

    /// <summary>
    /// Document description.
    /// </summary>
    public string Description
    {
        get => _description;
        set { _description = value; OnPropertyChanged(nameof(Description)); IsDirty = true; }
    }

    /// <summary>
    /// Document license information.
    /// </summary>
    public string License
    {
        get => _license;
        set { _license = value; OnPropertyChanged(nameof(License)); IsDirty = true; }
    }

    /// <summary>
    /// Whether the document has unsaved changes.
    /// </summary>
    public bool IsDirty
    {
        get => _isDirty;
        set { _isDirty = value; OnPropertyChanged(nameof(IsDirty)); }
    }

    /// <summary>
    /// Collection of definitions (gradients, patterns, symbols).
    /// </summary>
    public ObservableCollection<VectorElement> Defs { get; } = [];

    /// <summary>
    /// Collection of all elements in the document.
    /// </summary>
    public ObservableCollection<VectorElement> Elements { get; } = [];

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

