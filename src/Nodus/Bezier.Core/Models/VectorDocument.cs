using System.Collections.ObjectModel;
using System.ComponentModel;

namespace Bezier.Core.Models;

/// <summary>
/// Represents an SVG document with all its elements and metadata.
/// </summary>
public class VectorDocument : INotifyPropertyChanged
{
    private double _width = 800;
    private double _height = 600;
    private string _title = "Untitled";
    private string _author = string.Empty;
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
    /// Whether the document has unsaved changes.
    /// </summary>
    public bool IsDirty
    {
        get => _isDirty;
        set { _isDirty = value; OnPropertyChanged(nameof(IsDirty)); }
    }

    /// <summary>
    /// Collection of all elements in the document.
    /// </summary>
    public ObservableCollection<VectorElement> Elements { get; } = new();

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
