using System.Collections.ObjectModel;
using Bezier.Core.Models;

namespace Bezier.Core.Services;

/// <summary>
/// Event args for symbol events.
/// </summary>
public class SymbolEventArgs : EventArgs
{
    public Symbol Symbol { get; }
    public SymbolEventArgs(Symbol symbol) => Symbol = symbol;
}

/// <summary>
/// Manages the symbol library for reusable components.
/// </summary>
public class SymbolLibraryService
{
    private readonly Dictionary<Guid, Symbol> _symbols = [];
    private readonly Dictionary<Guid, List<SymbolInstance>> _instances = [];
    private Symbol? _editingSymbol;

    /// <summary>
    /// Gets all symbols in the library.
    /// </summary>
    public IReadOnlyCollection<Symbol> Symbols => _symbols.Values;

    /// <summary>
    /// Gets the symbol currently being edited.
    /// </summary>
    public Symbol? EditingSymbol => _editingSymbol;

    /// <summary>
    /// Gets whether we're in symbol editing mode.
    /// </summary>
    public bool IsEditing => _editingSymbol != null;

    /// <summary>
    /// Event raised when a symbol is added.
    /// </summary>
    public event EventHandler<SymbolEventArgs>? SymbolAdded;

    /// <summary>
    /// Event raised when a symbol is removed.
    /// </summary>
    public event EventHandler<SymbolEventArgs>? SymbolRemoved;

    /// <summary>
    /// Event raised when a symbol is modified.
    /// </summary>
    public event EventHandler<SymbolEventArgs>? SymbolModified;

    /// <summary>
    /// Event raised when entering/exiting symbol edit mode.
    /// </summary>
    public event EventHandler? EditModeChanged;

    /// <summary>
    /// Creates a new symbol from elements.
    /// </summary>
    public Symbol CreateSymbol(string name, IEnumerable<VectorElement> elements, string category = "Uncategorized")
    {
        var symbol = new Symbol
        {
            Name = name,
            Category = category
        };

        foreach (var element in elements)
        {
            symbol.Elements.Add(element.Clone());
        }

        // Calculate viewbox from content
        var bounds = symbol.GetBounds();
        symbol.ViewBox = bounds;

        AddSymbol(symbol);
        return symbol;
    }

    /// <summary>
    /// Adds a symbol to the library.
    /// </summary>
    public void AddSymbol(Symbol symbol)
    {
        _symbols[symbol.Id] = symbol;
        _instances[symbol.Id] = [];
        SymbolAdded?.Invoke(this, new SymbolEventArgs(symbol));
    }

    /// <summary>
    /// Removes a symbol from the library.
    /// </summary>
    public bool RemoveSymbol(Guid symbolId)
    {
        if (!_symbols.TryGetValue(symbolId, out var symbol))
            return false;

        _symbols.Remove(symbolId);
        _instances.Remove(symbolId);
        SymbolRemoved?.Invoke(this, new SymbolEventArgs(symbol));
        return true;
    }

    /// <summary>
    /// Gets a symbol by ID.
    /// </summary>
    public Symbol? GetSymbol(Guid symbolId)
    {
        return _symbols.GetValueOrDefault(symbolId);
    }

    /// <summary>
    /// Gets symbols by category.
    /// </summary>
    public IEnumerable<Symbol> GetSymbolsByCategory(string category)
    {
        return _symbols.Values.Where(s => s.Category == category);
    }

    /// <summary>
    /// Gets all unique categories.
    /// </summary>
    public IEnumerable<string> GetCategories()
    {
        return _symbols.Values.Select(s => s.Category).Distinct().OrderBy(c => c);
    }

    /// <summary>
    /// Searches symbols by name.
    /// </summary>
    public IEnumerable<Symbol> Search(string query)
    {
        if (string.IsNullOrWhiteSpace(query))
            return _symbols.Values;

        query = query.ToLowerInvariant();
        return _symbols.Values.Where(s =>
            s.Name.Contains(query, StringComparison.OrdinalIgnoreCase) ||
            (s.Description?.Contains(query, StringComparison.OrdinalIgnoreCase) ?? false) ||
            s.Category.Contains(query, StringComparison.OrdinalIgnoreCase)
        );
    }

    /// <summary>
    /// Creates an instance of a symbol.
    /// </summary>
    public SymbolInstance CreateInstance(Guid symbolId, double x, double y)
    {
        var symbol = GetSymbol(symbolId);
        if (symbol == null)
            throw new ArgumentException($"Symbol {symbolId} not found");

        var instance = new SymbolInstance
        {
            SymbolId = symbolId,
            X = x,
            Y = y,
            Width = symbol.ViewBox.Width,
            Height = symbol.ViewBox.Height,
            Name = symbol.Name
        };

        RegisterInstance(instance);
        return instance;
    }

    /// <summary>
    /// Registers an instance with its symbol.
    /// </summary>
    public void RegisterInstance(SymbolInstance instance)
    {
        if (_instances.TryGetValue(instance.SymbolId, out var list))
        {
            if (!list.Contains(instance))
                list.Add(instance);
        }
    }

    /// <summary>
    /// Unregisters an instance.
    /// </summary>
    public void UnregisterInstance(SymbolInstance instance)
    {
        if (_instances.TryGetValue(instance.SymbolId, out var list))
        {
            list.Remove(instance);
        }
    }

    /// <summary>
    /// Gets all instances of a symbol.
    /// </summary>
    public IReadOnlyList<SymbolInstance> GetInstances(Guid symbolId)
    {
        return _instances.TryGetValue(symbolId, out var list)
            ? list.AsReadOnly()
            : [];
    }

    /// <summary>
    /// Gets the count of instances for a symbol.
    /// </summary>
    public int GetInstanceCount(Guid symbolId)
    {
        return _instances.TryGetValue(symbolId, out var list) ? list.Count : 0;
    }

    /// <summary>
    /// Enters symbol editing mode.
    /// </summary>
    public void BeginEdit(Guid symbolId)
    {
        var symbol = GetSymbol(symbolId);
        if (symbol == null)
            throw new ArgumentException($"Symbol {symbolId} not found");

        _editingSymbol = symbol;
        EditModeChanged?.Invoke(this, EventArgs.Empty);
    }

    /// <summary>
    /// Exits symbol editing mode.
    /// </summary>
    public void EndEdit()
    {
        if (_editingSymbol != null)
        {
            _editingSymbol.MarkModified();
            SymbolModified?.Invoke(this, new SymbolEventArgs(_editingSymbol));
            _editingSymbol = null;
            EditModeChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    /// <summary>
    /// Updates a symbol's content and notifies instances.
    /// </summary>
    public void UpdateSymbol(Guid symbolId, IEnumerable<VectorElement> newElements)
    {
        var symbol = GetSymbol(symbolId);
        if (symbol == null)
            throw new ArgumentException($"Symbol {symbolId} not found");

        symbol.Elements.Clear();
        foreach (var element in newElements)
        {
            symbol.Elements.Add(element.Clone());
        }

        symbol.ViewBox = symbol.GetBounds();
        symbol.MarkModified();
        SymbolModified?.Invoke(this, new SymbolEventArgs(symbol));
    }

    /// <summary>
    /// Renames a symbol.
    /// </summary>
    public void RenameSymbol(Guid symbolId, string newName)
    {
        var symbol = GetSymbol(symbolId);
        if (symbol == null)
            throw new ArgumentException($"Symbol {symbolId} not found");

        symbol.Name = newName;
        symbol.MarkModified();
        SymbolModified?.Invoke(this, new SymbolEventArgs(symbol));
    }

    /// <summary>
    /// Changes a symbol's category.
    /// </summary>
    public void SetCategory(Guid symbolId, string category)
    {
        var symbol = GetSymbol(symbolId);
        if (symbol == null)
            throw new ArgumentException($"Symbol {symbolId} not found");

        symbol.Category = category;
        symbol.MarkModified();
        SymbolModified?.Invoke(this, new SymbolEventArgs(symbol));
    }

    /// <summary>
    /// Duplicates a symbol.
    /// </summary>
    public Symbol DuplicateSymbol(Guid symbolId)
    {
        var original = GetSymbol(symbolId);
        if (original == null)
            throw new ArgumentException($"Symbol {symbolId} not found");

        var clone = original.Clone();
        AddSymbol(clone);
        return clone;
    }

    /// <summary>
    /// Detaches an instance from its master symbol.
    /// </summary>
    public IEnumerable<VectorElement> DetachInstance(SymbolInstance instance)
    {
        var symbol = GetSymbol(instance.SymbolId);
        if (symbol == null)
            return [];

        instance.IsDetached = true;
        UnregisterInstance(instance);

        // Return cloned elements positioned at instance location
        var elements = new List<VectorElement>();
        var scale = (instance.Width / symbol.ViewBox.Width, instance.Height / symbol.ViewBox.Height);

        foreach (var element in symbol.Elements)
        {
            var clone = element.Clone();
            // Apply instance transform
            var bounds = clone.GetBoundingBox();
            var newX = instance.X + (bounds.X - symbol.ViewBox.X) * scale.Item1;
            var newY = instance.Y + (bounds.Y - symbol.ViewBox.Y) * scale.Item2;

            clone.Transform = clone.Transform with
            {
                TranslateX = clone.Transform.TranslateX + newX - bounds.X,
                TranslateY = clone.Transform.TranslateY + newY - bounds.Y,
                ScaleX = clone.Transform.ScaleX * scale.Item1,
                ScaleY = clone.Transform.ScaleY * scale.Item2
            };

            elements.Add(clone);
        }

        return elements;
    }

    /// <summary>
    /// Clears all symbols.
    /// </summary>
    public void Clear()
    {
        var symbols = _symbols.Values.ToList();
        _symbols.Clear();
        _instances.Clear();
        _editingSymbol = null;

        foreach (var symbol in symbols)
        {
            SymbolRemoved?.Invoke(this, new SymbolEventArgs(symbol));
        }
    }

    /// <summary>
    /// Gets the total count of symbols.
    /// </summary>
    public int Count => _symbols.Count;
}
