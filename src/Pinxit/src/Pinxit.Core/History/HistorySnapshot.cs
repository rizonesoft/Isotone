namespace Pinxit.Core.History;

using System.Buffers;

/// <summary>
/// Represents a snapshot of state for undo/redo operations.
/// Uses pooled memory for zero-allocation in hot paths.
/// </summary>
public sealed class HistorySnapshot : IDisposable
{
    private byte[]? _data;
    private readonly int _dataLength;
    private bool _disposed;

    /// <summary>
    /// Gets the unique identifier for this snapshot.
    /// </summary>
    public Guid Id { get; } = Guid.NewGuid();

    /// <summary>
    /// Gets when this snapshot was created.
    /// </summary>
    public DateTime CreatedAt { get; } = DateTime.UtcNow;

    /// <summary>
    /// Gets the size of the snapshot data in bytes.
    /// </summary>
    public int Size => _dataLength;

    /// <summary>
    /// Gets whether this snapshot has been disposed.
    /// </summary>
    public bool IsDisposed => _disposed;

    private HistorySnapshot(byte[] data, int length)
    {
        _data = data;
        _dataLength = length;
    }

    /// <summary>
    /// Creates a snapshot from a byte span (copies data to pooled array).
    /// </summary>
    public static HistorySnapshot Create(ReadOnlySpan<byte> data)
    {
        var pooledArray = ArrayPool<byte>.Shared.Rent(data.Length);
        data.CopyTo(pooledArray);
        return new HistorySnapshot(pooledArray, data.Length);
    }

    /// <summary>
    /// Creates a snapshot by capturing state from a callback.
    /// </summary>
    public static HistorySnapshot Create(int size, Action<Span<byte>> captureAction)
    {
        var pooledArray = ArrayPool<byte>.Shared.Rent(size);
        captureAction(pooledArray.AsSpan(0, size));
        return new HistorySnapshot(pooledArray, size);
    }

    /// <summary>
    /// Gets a read-only span of the snapshot data.
    /// </summary>
    public ReadOnlySpan<byte> GetData()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        return _data.AsSpan(0, _dataLength);
    }

    /// <summary>
    /// Restores the snapshot data to a target span.
    /// </summary>
    public void RestoreTo(Span<byte> target)
    {
        ObjectDisposedException.ThrowIf(_disposed, this);

        if (target.Length < _dataLength)
            throw new ArgumentException("Target span is too small", nameof(target));

        _data.AsSpan(0, _dataLength).CopyTo(target);
    }

    /// <summary>
    /// Restores the snapshot data via a callback.
    /// </summary>
    public void RestoreTo(Action<ReadOnlySpan<byte>> restoreAction)
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        restoreAction(_data.AsSpan(0, _dataLength));
    }

    public void Dispose()
    {
        if (_disposed) return;

        if (_data is not null)
        {
            ArrayPool<byte>.Shared.Return(_data);
            _data = null;
        }

        _disposed = true;
    }
}

/// <summary>
/// Factory for creating history snapshots with memory tracking.
/// </summary>
public sealed class SnapshotFactory
{
    private readonly long _maxMemoryBytes;
    private long _currentMemoryBytes;
    private readonly List<WeakReference<HistorySnapshot>> _snapshots = [];

    public SnapshotFactory(long maxMemoryMB = 256)
    {
        _maxMemoryBytes = maxMemoryMB * 1024 * 1024;
    }

    /// <summary>
    /// Gets the current memory usage in bytes.
    /// </summary>
    public long MemoryUsageBytes => _currentMemoryBytes;

    /// <summary>
    /// Gets the maximum memory limit in bytes.
    /// </summary>
    public long MaxMemoryBytes => _maxMemoryBytes;

    /// <summary>
    /// Creates a snapshot and tracks its memory usage.
    /// </summary>
    public HistorySnapshot CreateSnapshot(ReadOnlySpan<byte> data)
    {
        // Clean up disposed snapshots first
        CleanupDisposed();

        // Check memory limit
        if (_currentMemoryBytes + data.Length > _maxMemoryBytes)
        {
            throw new InvalidOperationException(
                $"Cannot create snapshot: would exceed memory limit ({_currentMemoryBytes + data.Length} > {_maxMemoryBytes})");
        }

        var snapshot = HistorySnapshot.Create(data);
        _snapshots.Add(new WeakReference<HistorySnapshot>(snapshot));
        Interlocked.Add(ref _currentMemoryBytes, data.Length);

        return snapshot;
    }

    private void CleanupDisposed()
    {
        for (int i = _snapshots.Count - 1; i >= 0; i--)
        {
            if (!_snapshots[i].TryGetTarget(out var snapshot) || snapshot.IsDisposed)
            {
                if (_snapshots[i].TryGetTarget(out var s))
                {
                    Interlocked.Add(ref _currentMemoryBytes, -s.Size);
                }
                _snapshots.RemoveAt(i);
            }
        }
    }
}
