using System.Collections.ObjectModel;
using Bezier.Core.Models;

namespace Bezier.Core.Services;

/// <summary>
/// Event args for artboard events.
/// </summary>
public class ArtboardEventArgs : EventArgs
{
    public Artboard Artboard { get; }
    public ArtboardEventArgs(Artboard artboard) => Artboard = artboard;
}

/// <summary>
/// Manages artboards in the document.
/// </summary>
public class ArtboardManager
{
    private Artboard? _activeArtboard;
    private int _artboardCounter = 1;

    /// <summary>
    /// Gets the artboards collection.
    /// </summary>
    public ObservableCollection<Artboard> Artboards { get; } = [];

    /// <summary>
    /// Gets or sets the active artboard.
    /// </summary>
    public Artboard? ActiveArtboard
    {
        get => _activeArtboard;
        set
        {
            if (_activeArtboard != value)
            {
                if (_activeArtboard != null)
                    _activeArtboard.IsSelected = false;

                _activeArtboard = value;

                if (_activeArtboard != null)
                    _activeArtboard.IsSelected = true;

                ActiveArtboardChanged?.Invoke(this, value != null
                    ? new ArtboardEventArgs(value)
                    : EventArgs.Empty);
            }
        }
    }

    /// <summary>
    /// Event raised when the active artboard changes.
    /// </summary>
    public event EventHandler? ActiveArtboardChanged;

    /// <summary>
    /// Event raised when artboards are modified.
    /// </summary>
    public event EventHandler? ArtboardsChanged;

    /// <summary>
    /// Event raised when an artboard is added.
    /// </summary>
    public event EventHandler<ArtboardEventArgs>? ArtboardAdded;

    /// <summary>
    /// Event raised when an artboard is removed.
    /// </summary>
    public event EventHandler<ArtboardEventArgs>? ArtboardRemoved;

    /// <summary>
    /// Creates a new artboard with default size.
    /// </summary>
    public Artboard CreateArtboard(double x = 0, double y = 0, double width = 800, double height = 600)
    {
        var artboard = new Artboard
        {
            Name = $"Artboard {_artboardCounter++}",
            X = x,
            Y = y,
            Width = width,
            Height = height
        };

        AddArtboard(artboard);
        return artboard;
    }

    /// <summary>
    /// Creates an artboard from a preset.
    /// </summary>
    public Artboard CreateFromPreset(string presetName, double x = 0, double y = 0)
    {
        var preset = ArtboardPresets.FindPreset(presetName);
        if (!preset.HasValue)
            throw new ArgumentException($"Preset '{presetName}' not found");

        var artboard = new Artboard
        {
            Name = $"{preset.Value.Name} {_artboardCounter++}",
            X = x,
            Y = y,
            Width = preset.Value.Width,
            Height = preset.Value.Height
        };

        AddArtboard(artboard);
        return artboard;
    }

    /// <summary>
    /// Adds an artboard to the document.
    /// </summary>
    public void AddArtboard(Artboard artboard)
    {
        Artboards.Add(artboard);
        ActiveArtboard ??= artboard;
        ArtboardAdded?.Invoke(this, new ArtboardEventArgs(artboard));
        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Removes an artboard from the document.
    /// </summary>
    public bool RemoveArtboard(Artboard artboard)
    {
        if (!Artboards.Remove(artboard))
            return false;

        if (ActiveArtboard == artboard)
            ActiveArtboard = Artboards.FirstOrDefault();

        ArtboardRemoved?.Invoke(this, new ArtboardEventArgs(artboard));
        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
        return true;
    }

    /// <summary>
    /// Removes an artboard by ID.
    /// </summary>
    public bool RemoveArtboard(Guid id)
    {
        var artboard = GetArtboard(id);
        return artboard != null && RemoveArtboard(artboard);
    }

    /// <summary>
    /// Gets an artboard by ID.
    /// </summary>
    public Artboard? GetArtboard(Guid id)
    {
        return Artboards.FirstOrDefault(a => a.Id == id);
    }

    /// <summary>
    /// Gets an artboard by name.
    /// </summary>
    public Artboard? GetArtboardByName(string name)
    {
        return Artboards.FirstOrDefault(a =>
            a.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
    }

    /// <summary>
    /// Gets the artboard at a point.
    /// </summary>
    public Artboard? GetArtboardAtPoint(double x, double y)
    {
        // Return topmost (last in list) artboard at point
        for (var i = Artboards.Count - 1; i >= 0; i--)
        {
            if (Artboards[i].ContainsPoint(x, y))
                return Artboards[i];
        }
        return null;
    }

    /// <summary>
    /// Gets all artboards that contain a point.
    /// </summary>
    public IEnumerable<Artboard> GetArtboardsAtPoint(double x, double y)
    {
        return Artboards.Where(a => a.ContainsPoint(x, y));
    }

    /// <summary>
    /// Duplicates an artboard.
    /// </summary>
    public Artboard DuplicateArtboard(Artboard artboard)
    {
        var clone = artboard.Clone();
        clone.Name = $"{artboard.Name} Copy";

        // Position to avoid overlap
        var offset = 50;
        while (Artboards.Any(a => a.Intersects(clone)))
        {
            clone.X += offset;
            clone.Y += offset;
        }

        AddArtboard(clone);
        return clone;
    }

    /// <summary>
    /// Renames an artboard.
    /// </summary>
    public void RenameArtboard(Artboard artboard, string newName)
    {
        artboard.Name = newName;
        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Resizes an artboard.
    /// </summary>
    public void ResizeArtboard(Artboard artboard, double width, double height)
    {
        artboard.Width = width;
        artboard.Height = height;
        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Moves an artboard.
    /// </summary>
    public void MoveArtboard(Artboard artboard, double x, double y)
    {
        artboard.X = x;
        artboard.Y = y;
        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Reorders artboards.
    /// </summary>
    public void MoveArtboardToIndex(Artboard artboard, int newIndex)
    {
        var currentIndex = Artboards.IndexOf(artboard);
        if (currentIndex < 0) return;

        newIndex = Math.Clamp(newIndex, 0, Artboards.Count - 1);
        if (currentIndex == newIndex) return;

        Artboards.RemoveAt(currentIndex);
        Artboards.Insert(newIndex, artboard);
        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Brings an artboard to front.
    /// </summary>
    public void BringToFront(Artboard artboard)
    {
        MoveArtboardToIndex(artboard, Artboards.Count - 1);
    }

    /// <summary>
    /// Sends an artboard to back.
    /// </summary>
    public void SendToBack(Artboard artboard)
    {
        MoveArtboardToIndex(artboard, 0);
    }

    /// <summary>
    /// Navigates to the next artboard.
    /// </summary>
    public Artboard? NavigateNext()
    {
        if (Artboards.Count == 0) return null;

        var currentIndex = ActiveArtboard != null
            ? Artboards.IndexOf(ActiveArtboard)
            : -1;

        var nextIndex = (currentIndex + 1) % Artboards.Count;
        ActiveArtboard = Artboards[nextIndex];
        return ActiveArtboard;
    }

    /// <summary>
    /// Navigates to the previous artboard.
    /// </summary>
    public Artboard? NavigatePrevious()
    {
        if (Artboards.Count == 0) return null;

        var currentIndex = ActiveArtboard != null
            ? Artboards.IndexOf(ActiveArtboard)
            : 0;

        var prevIndex = currentIndex <= 0
            ? Artboards.Count - 1
            : currentIndex - 1;

        ActiveArtboard = Artboards[prevIndex];
        return ActiveArtboard;
    }

    /// <summary>
    /// Gets the combined bounds of all artboards.
    /// </summary>
    public (double X, double Y, double Width, double Height)? GetCombinedBounds()
    {
        if (Artboards.Count == 0) return null;

        var minX = Artboards.Min(a => a.X);
        var minY = Artboards.Min(a => a.Y);
        var maxX = Artboards.Max(a => a.X + a.Width);
        var maxY = Artboards.Max(a => a.Y + a.Height);

        return (minX, minY, maxX - minX, maxY - minY);
    }

    /// <summary>
    /// Arranges artboards in a grid.
    /// </summary>
    public void ArrangeInGrid(int columns, double spacing = 50)
    {
        if (Artboards.Count == 0) return;

        var maxWidth = Artboards.Max(a => a.Width);
        var maxHeight = Artboards.Max(a => a.Height);

        var x = 0.0;
        var y = 0.0;
        var col = 0;

        foreach (var artboard in Artboards)
        {
            artboard.X = x;
            artboard.Y = y;

            col++;
            if (col >= columns)
            {
                col = 0;
                x = 0;
                y += maxHeight + spacing;
            }
            else
            {
                x += maxWidth + spacing;
            }
        }

        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Arranges artboards horizontally.
    /// </summary>
    public void ArrangeHorizontally(double spacing = 50)
    {
        if (Artboards.Count == 0) return;

        var x = 0.0;
        foreach (var artboard in Artboards)
        {
            artboard.X = x;
            artboard.Y = 0;
            x += artboard.Width + spacing;
        }

        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Arranges artboards vertically.
    /// </summary>
    public void ArrangeVertically(double spacing = 50)
    {
        if (Artboards.Count == 0) return;

        var y = 0.0;
        foreach (var artboard in Artboards)
        {
            artboard.X = 0;
            artboard.Y = y;
            y += artboard.Height + spacing;
        }

        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Clears all artboards.
    /// </summary>
    public void Clear()
    {
        var artboards = Artboards.ToList();
        Artboards.Clear();
        _activeArtboard = null;
        _artboardCounter = 1;

        foreach (var artboard in artboards)
        {
            ArtboardRemoved?.Invoke(this, new ArtboardEventArgs(artboard));
        }

        ArtboardsChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Gets the count of artboards.
    /// </summary>
    public int Count => Artboards.Count;
}
