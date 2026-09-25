using System.Collections.ObjectModel;
using System.ComponentModel;

namespace Bezier.Core.Models;

/// <summary>
/// Preset artboard sizes.
/// </summary>
public static class ArtboardPresets
{
    public static readonly (string Name, double Width, double Height)[] Presets =
    [
        // Web
        ("Desktop HD", 1920, 1080),
        ("Desktop", 1440, 900),
        ("Tablet Landscape", 1024, 768),
        ("Tablet Portrait", 768, 1024),
        ("Mobile", 375, 812),
        ("Mobile Small", 320, 568),
        
        // Social Media
        ("Instagram Post", 1080, 1080),
        ("Instagram Story", 1080, 1920),
        ("Facebook Post", 1200, 630),
        ("Twitter Post", 1200, 675),
        ("LinkedIn Post", 1200, 627),
        
        // Print (72 DPI)
        ("A4 Portrait", 595, 842),
        ("A4 Landscape", 842, 595),
        ("A3 Portrait", 842, 1191),
        ("Letter Portrait", 612, 792),
        ("Letter Landscape", 792, 612),
        
        // Icons
        ("Icon 16x16", 16, 16),
        ("Icon 24x24", 24, 24),
        ("Icon 32x32", 32, 32),
        ("Icon 48x48", 48, 48),
        ("Icon 64x64", 64, 64),
        ("Icon 128x128", 128, 128),
        ("Icon 256x256", 256, 256),
        ("Icon 512x512", 512, 512),
    ];

    public static (string Name, double Width, double Height)? FindPreset(string name)
    {
        foreach (var preset in Presets)
        {
            if (preset.Name.Equals(name, StringComparison.OrdinalIgnoreCase))
                return preset;
        }
        return null;
    }
}

/// <summary>
/// Represents an artboard (canvas region) in the document.
/// </summary>
public class Artboard : INotifyPropertyChanged
{
    private string _name = "Artboard";
    private double _x;
    private double _y;
    private double _width = 800;
    private double _height = 600;
    private uint _backgroundColor = 0xFFFFFFFF;
    private bool _isSelected;
    private bool _showBackground = true;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    /// <summary>
    /// Gets the unique identifier for this artboard.
    /// </summary>
    public Guid Id { get; init; } = Guid.NewGuid();

    /// <summary>
    /// Gets or sets the artboard name.
    /// </summary>
    public string Name
    {
        get => _name;
        set { _name = value; OnPropertyChanged(nameof(Name)); }
    }

    /// <summary>
    /// Gets or sets the X position.
    /// </summary>
    public double X
    {
        get => _x;
        set { _x = value; OnPropertyChanged(nameof(X)); OnPropertyChanged(nameof(Bounds)); }
    }

    /// <summary>
    /// Gets or sets the Y position.
    /// </summary>
    public double Y
    {
        get => _y;
        set { _y = value; OnPropertyChanged(nameof(Y)); OnPropertyChanged(nameof(Bounds)); }
    }

    /// <summary>
    /// Gets or sets the width.
    /// </summary>
    public double Width
    {
        get => _width;
        set { _width = Math.Max(1, value); OnPropertyChanged(nameof(Width)); OnPropertyChanged(nameof(Bounds)); }
    }

    /// <summary>
    /// Gets or sets the height.
    /// </summary>
    public double Height
    {
        get => _height;
        set { _height = Math.Max(1, value); OnPropertyChanged(nameof(Height)); OnPropertyChanged(nameof(Bounds)); }
    }

    /// <summary>
    /// Gets or sets the background color (ARGB).
    /// </summary>
    public uint BackgroundColor
    {
        get => _backgroundColor;
        set { _backgroundColor = value; OnPropertyChanged(nameof(BackgroundColor)); }
    }

    /// <summary>
    /// Gets or sets whether the background is shown.
    /// </summary>
    public bool ShowBackground
    {
        get => _showBackground;
        set { _showBackground = value; OnPropertyChanged(nameof(ShowBackground)); }
    }

    /// <summary>
    /// Gets or sets whether this artboard is selected.
    /// </summary>
    public bool IsSelected
    {
        get => _isSelected;
        set { _isSelected = value; OnPropertyChanged(nameof(IsSelected)); }
    }

    /// <summary>
    /// Gets the bounding rectangle.
    /// </summary>
    public (double X, double Y, double Width, double Height) Bounds => (X, Y, Width, Height);

    /// <summary>
    /// Gets the center point.
    /// </summary>
    public (double X, double Y) Center => (X + Width / 2, Y + Height / 2);

    /// <summary>
    /// Tests if a point is inside this artboard.
    /// </summary>
    public bool ContainsPoint(double x, double y)
    {
        return x >= X && x <= X + Width && y >= Y && y <= Y + Height;
    }

    /// <summary>
    /// Tests if a point is on the artboard border (for selection).
    /// </summary>
    public bool HitTestBorder(double x, double y, double tolerance = 5)
    {
        var inside = ContainsPoint(x, y);
        var innerX = X + tolerance;
        var innerY = Y + tolerance;
        var innerW = Width - tolerance * 2;
        var innerH = Height - tolerance * 2;
        var insideInner = x >= innerX && x <= innerX + innerW &&
                          y >= innerY && y <= innerY + innerH;

        return inside && !insideInner;
    }

    /// <summary>
    /// Tests if a point is on the title area.
    /// </summary>
    public bool HitTestTitle(double x, double y, double titleHeight = 20)
    {
        return x >= X && x <= X + Width && y >= Y - titleHeight && y < Y;
    }

    /// <summary>
    /// Gets the resize handle at a point, if any.
    /// </summary>
    public ResizeHandle? GetResizeHandle(double x, double y, double handleSize = 8)
    {
        var half = handleSize / 2;
        var corners = new[]
        {
            (X, Y, ResizeHandle.TopLeft),
            (X + Width, Y, ResizeHandle.TopRight),
            (X, Y + Height, ResizeHandle.BottomLeft),
            (X + Width, Y + Height, ResizeHandle.BottomRight),
        };

        foreach (var (cx, cy, handle) in corners)
        {
            if (Math.Abs(x - cx) <= half && Math.Abs(y - cy) <= half)
                return handle;
        }

        var edges = new[]
        {
            (X + Width / 2, Y, ResizeHandle.Top),
            (X + Width / 2, Y + Height, ResizeHandle.Bottom),
            (X, Y + Height / 2, ResizeHandle.Left),
            (X + Width, Y + Height / 2, ResizeHandle.Right),
        };

        foreach (var (cx, cy, handle) in edges)
        {
            if (Math.Abs(x - cx) <= half && Math.Abs(y - cy) <= half)
                return handle;
        }

        return null;
    }

    /// <summary>
    /// Applies a preset size.
    /// </summary>
    public void ApplyPreset(string presetName)
    {
        var preset = ArtboardPresets.FindPreset(presetName);
        if (preset.HasValue)
        {
            Width = preset.Value.Width;
            Height = preset.Value.Height;
        }
    }

    /// <summary>
    /// Creates a clone of this artboard.
    /// </summary>
    public Artboard Clone()
    {
        return new Artboard
        {
            Name = Name + " Copy",
            X = X + 50,
            Y = Y + 50,
            Width = Width,
            Height = Height,
            BackgroundColor = BackgroundColor,
            ShowBackground = ShowBackground
        };
    }

    /// <summary>
    /// Checks if this artboard intersects with another.
    /// </summary>
    public bool Intersects(Artboard other)
    {
        return X < other.X + other.Width &&
               X + Width > other.X &&
               Y < other.Y + other.Height &&
               Y + Height > other.Y;
    }

    /// <summary>
    /// Gets the area of intersection with another artboard.
    /// </summary>
    public (double X, double Y, double Width, double Height)? GetIntersection(Artboard other)
    {
        if (!Intersects(other))
            return null;

        var x = Math.Max(X, other.X);
        var y = Math.Max(Y, other.Y);
        var right = Math.Min(X + Width, other.X + other.Width);
        var bottom = Math.Min(Y + Height, other.Y + other.Height);

        return (x, y, right - x, bottom - y);
    }
}

/// <summary>
/// Resize handle positions.
/// </summary>
public enum ResizeHandle
{
    TopLeft,
    Top,
    TopRight,
    Right,
    BottomRight,
    Bottom,
    BottomLeft,
    Left
}
