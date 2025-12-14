using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.ComponentModel;
using Bezier.Core.Interfaces;

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
    private IFill? _background;

    public event PropertyChangedEventHandler? PropertyChanged;

    /// <summary>
    /// Initializes a new instance of the VectorDocument class.
    /// </summary>
    public VectorDocument()
    {
        // Subscribe to collection changes for IsDirty tracking
        Elements.CollectionChanged += OnCollectionChanged;
        Defs.CollectionChanged += OnCollectionChanged;
    }

    /// <summary>
    /// Document width in pixels. Must be greater than 0.
    /// </summary>
    /// <exception cref="ArgumentOutOfRangeException">Thrown when value is less than or equal to 0.</exception>
    public double Width
    {
        get => _width;
        set
        {
            if (value <= 0)
                throw new ArgumentOutOfRangeException(nameof(value), "Width must be greater than 0.");
            if (Math.Abs(_width - value) < 0.0001) return;
            _width = value;
            OnPropertyChanged(nameof(Width));
            IsDirty = true;
        }
    }

    /// <summary>
    /// Document height in pixels. Must be greater than 0.
    /// </summary>
    /// <exception cref="ArgumentOutOfRangeException">Thrown when value is less than or equal to 0.</exception>
    public double Height
    {
        get => _height;
        set
        {
            if (value <= 0)
                throw new ArgumentOutOfRangeException(nameof(value), "Height must be greater than 0.");
            if (Math.Abs(_height - value) < 0.0001) return;
            _height = value;
            OnPropertyChanged(nameof(Height));
            IsDirty = true;
        }
    }

    /// <summary>
    /// SVG viewBox for coordinate system mapping.
    /// </summary>
    public ViewBox ViewBox
    {
        get => _viewBox;
        set
        {
            _viewBox = value;
            OnPropertyChanged(nameof(ViewBox));
            IsDirty = true;
        }
    }

    /// <summary>
    /// Document title.
    /// </summary>
    public string Title
    {
        get => _title;
        set
        {
            if (_title == value) return;
            _title = value ?? "Untitled";
            OnPropertyChanged(nameof(Title));
            IsDirty = true;
        }
    }

    /// <summary>
    /// Document author.
    /// </summary>
    public string Author
    {
        get => _author;
        set
        {
            if (_author == value) return;
            _author = value ?? string.Empty;
            OnPropertyChanged(nameof(Author));
            IsDirty = true;
        }
    }

    /// <summary>
    /// Document description.
    /// </summary>
    public string Description
    {
        get => _description;
        set
        {
            if (_description == value) return;
            _description = value ?? string.Empty;
            OnPropertyChanged(nameof(Description));
            IsDirty = true;
        }
    }

    /// <summary>
    /// Document license information.
    /// </summary>
    public string License
    {
        get => _license;
        set
        {
            if (_license == value) return;
            _license = value ?? string.Empty;
            OnPropertyChanged(nameof(License));
            IsDirty = true;
        }
    }

    /// <summary>
    /// Document background fill (color, gradient, or pattern). Null for transparent.
    /// </summary>
    public IFill? Background
    {
        get => _background;
        set
        {
            if (_background == value) return;
            _background = value;
            OnPropertyChanged(nameof(Background));
            IsDirty = true;
        }
    }

    /// <summary>
    /// Whether the document has unsaved changes.
    /// </summary>
    public bool IsDirty
    {
        get => _isDirty;
        set
        {
            if (_isDirty == value) return;
            _isDirty = value;
            OnPropertyChanged(nameof(IsDirty));
        }
    }

    /// <summary>
    /// Collection of definitions (gradients, patterns, symbols).
    /// </summary>
    public ObservableCollection<VectorElement> Defs { get; } = [];

    /// <summary>
    /// Collection of all elements in the document.
    /// </summary>
    public ObservableCollection<VectorElement> Elements { get; } = [];

    /// <summary>
    /// Marks the document as saved (IsDirty = false).
    /// </summary>
    public void MarkAsSaved() => IsDirty = false;

    /// <summary>
    /// Clears all elements and resets the document to default state.
    /// </summary>
    public void Clear()
    {
        Elements.Clear();
        Defs.Clear();
        _title = "Untitled";
        _author = string.Empty;
        _description = string.Empty;
        _license = string.Empty;
        _background = null;
        _width = 800;
        _height = 600;
        _viewBox = new ViewBox(0, 0, 800, 600);
        
        OnPropertyChanged(nameof(Title));
        OnPropertyChanged(nameof(Author));
        OnPropertyChanged(nameof(Description));
        OnPropertyChanged(nameof(License));
        OnPropertyChanged(nameof(Background));
        OnPropertyChanged(nameof(Width));
        OnPropertyChanged(nameof(Height));
        OnPropertyChanged(nameof(ViewBox));
        
        IsDirty = false;
    }

    private void OnCollectionChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        IsDirty = true;
    }

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
