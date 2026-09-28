namespace Gesso.Core.Tiles;

using System.Collections.Concurrent;

/// <summary>
/// LRU cache for tiles with memory limit management.
/// </summary>
public sealed class TileCache : IDisposable
{
    private readonly ConcurrentDictionary<TileCoordinate, TileEntry> _cache = new();
    private readonly Lock _evictionLock = new();
    private readonly long _maxMemoryBytes;
    private long _currentMemoryBytes;
    private bool _disposed;

    public TileCache(long maxMemoryMB = 512)
    {
        _maxMemoryBytes = maxMemoryMB * 1024 * 1024;
    }

    public int Count => _cache.Count;

    public long MemoryUsageBytes => _currentMemoryBytes;

    public Tile GetOrCreate(TileCoordinate coordinate)
    {
        ObjectDisposedException.ThrowIf(_disposed, this);

        if (_cache.TryGetValue(coordinate, out var entry))
        {
            entry.LastAccess = DateTime.UtcNow;
            return entry.Tile;
        }

        var tile = new Tile(coordinate);
        var newEntry = new TileEntry(tile);

        if (_cache.TryAdd(coordinate, newEntry))
        {
            Interlocked.Add(ref _currentMemoryBytes, Tile.TileDataSize);
            EvictIfNeeded();
        }
        else
        {
            tile.Dispose();
            return _cache[coordinate].Tile;
        }

        return tile;
    }

    public bool TryGet(TileCoordinate coordinate, out Tile? tile)
    {
        ObjectDisposedException.ThrowIf(_disposed, this);

        if (_cache.TryGetValue(coordinate, out var entry))
        {
            entry.LastAccess = DateTime.UtcNow;
            tile = entry.Tile;
            return true;
        }

        tile = null;
        return false;
    }

    public void Remove(TileCoordinate coordinate)
    {
        if (_cache.TryRemove(coordinate, out var entry))
        {
            Interlocked.Add(ref _currentMemoryBytes, -Tile.TileDataSize);
            entry.Tile.Dispose();
        }
    }

    public void Clear()
    {
        lock (_evictionLock)
        {
            foreach (var entry in _cache.Values)
            {
                entry.Tile.Dispose();
            }

            _cache.Clear();
            _currentMemoryBytes = 0;
        }
    }

    private void EvictIfNeeded()
    {
        if (_currentMemoryBytes <= _maxMemoryBytes)
        {
            return;
        }

        lock (_evictionLock)
        {
            if (_currentMemoryBytes <= _maxMemoryBytes)
            {
                return;
            }

            var entriesToEvict = _cache
                .Where(kvp => !kvp.Value.Tile.IsDirty)
                .OrderBy(kvp => kvp.Value.LastAccess)
                .Take(_cache.Count / 4)
                .ToList();

            foreach (var kvp in entriesToEvict)
            {
                Remove(kvp.Key);
            }
        }
    }

    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        Clear();
        _disposed = true;
    }

    private sealed class TileEntry
    {
        public Tile Tile { get; }
        public DateTime LastAccess { get; set; }

        public TileEntry(Tile tile)
        {
            Tile = tile;
            LastAccess = DateTime.UtcNow;
        }
    }
}
