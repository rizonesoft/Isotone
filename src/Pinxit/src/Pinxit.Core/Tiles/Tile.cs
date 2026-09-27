namespace Pinxit.Core.Tiles;

using System.Buffers;

/// <summary>
/// Represents a 256x256 pixel tile for efficient memory management.
/// </summary>
public sealed class Tile : IDisposable
{
    public const int TileSize = 256;
    public const int PixelStride = 4; // RGBA
    public const int TileDataSize = TileSize * TileSize * PixelStride;

    private byte[]? _data;
    private bool _disposed;

    public TileCoordinate Coordinate { get; }

    public bool IsDirty { get; private set; }

    public bool IsEmpty { get; private set; } = true;

    public Tile(TileCoordinate coordinate)
    {
        Coordinate = coordinate;
        _data = ArrayPool<byte>.Shared.Rent(TileDataSize);
        Array.Clear(_data, 0, TileDataSize);
    }

    public Span<byte> GetData()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        return _data.AsSpan(0, TileDataSize);
    }

    public ReadOnlySpan<byte> GetReadOnlyData()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        return _data.AsSpan(0, TileDataSize);
    }

    public void MarkDirty()
    {
        IsDirty = true;
        IsEmpty = false;
    }

    public void MarkClean()
    {
        IsDirty = false;
    }

    public void Clear()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);

        if (_data != null)
        {
            Array.Clear(_data, 0, TileDataSize);
        }

        IsEmpty = true;
        IsDirty = true;
    }

    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        if (_data != null)
        {
            ArrayPool<byte>.Shared.Return(_data);
            _data = null;
        }

        _disposed = true;
    }
}
