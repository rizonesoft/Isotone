namespace Pinxit.Core.Selections;

using System.Buffers;
using System.Runtime.CompilerServices;

/// <summary>
/// Represents a pixel selection mask. Each pixel has a selection value from 0 (not selected) to 255 (fully selected).
/// Supports anti-aliased and feathered selections.
/// </summary>
public sealed class Selection : IDisposable
{
    private byte[]? _mask;
    private readonly int _width;
    private readonly int _height;
    private bool _disposed;
    private bool _isEmpty = true;

    /// <summary>
    /// Gets the width of the selection mask.
    /// </summary>
    public int Width => _width;

    /// <summary>
    /// Gets the height of the selection mask.
    /// </summary>
    public int Height => _height;

    /// <summary>
    /// Gets whether the selection is empty (no pixels selected).
    /// </summary>
    public bool IsEmpty => _isEmpty;

    /// <summary>
    /// Gets the bounding rectangle of the selection.
    /// </summary>
    public SelectionBounds Bounds { get; private set; }

    /// <summary>
    /// Gets the current feather radius.
    /// </summary>
    public float FeatherRadius { get; private set; }

    public Selection(int width, int height)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(width);
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(height);

        _width = width;
        _height = height;
        _mask = ArrayPool<byte>.Shared.Rent(width * height);
        Array.Clear(_mask, 0, width * height);
        Bounds = SelectionBounds.Empty;
    }

    /// <summary>
    /// Gets the selection value at a pixel (0-255).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public byte GetValue(int x, int y)
    {
        if (x < 0 || x >= _width || y < 0 || y >= _height)
            return 0;

        return _mask![y * _width + x];
    }

    /// <summary>
    /// Sets the selection value at a pixel (0-255).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public void SetValue(int x, int y, byte value)
    {
        if (x < 0 || x >= _width || y < 0 || y >= _height)
            return;

        _mask![y * _width + x] = value;
        if (value > 0) _isEmpty = false;
    }

    /// <summary>
    /// Gets a span of the raw mask data.
    /// </summary>
    public Span<byte> GetMaskData()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        return _mask.AsSpan(0, _width * _height);
    }

    /// <summary>
    /// Gets a read-only span of the raw mask data.
    /// </summary>
    public ReadOnlySpan<byte> GetReadOnlyMaskData()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        return _mask.AsSpan(0, _width * _height);
    }

    /// <summary>
    /// Clears the selection (deselects all).
    /// </summary>
    public void Clear()
    {
        Array.Clear(_mask!, 0, _width * _height);
        _isEmpty = true;
        Bounds = SelectionBounds.Empty;
        FeatherRadius = 0;
    }

    /// <summary>
    /// Selects all pixels.
    /// </summary>
    public void SelectAll()
    {
        Array.Fill(_mask!, (byte)255, 0, _width * _height);
        _isEmpty = false;
        Bounds = new SelectionBounds(0, 0, _width, _height);
    }

    /// <summary>
    /// Inverts the selection.
    /// </summary>
    public void Invert()
    {
        var span = GetMaskData();
        for (int i = 0; i < span.Length; i++)
        {
            span[i] = (byte)(255 - span[i]);
        }
        _isEmpty = false;
        UpdateBounds();
    }

    /// <summary>
    /// Combines this selection with another using the specified operation.
    /// </summary>
    public void Combine(Selection other, SelectionOperation operation)
    {
        ArgumentNullException.ThrowIfNull(other);

        if (other.Width != _width || other.Height != _height)
            throw new ArgumentException("Selection dimensions must match", nameof(other));

        var thisSpan = GetMaskData();
        var otherSpan = other.GetReadOnlyMaskData();

        switch (operation)
        {
            case SelectionOperation.Replace:
                otherSpan.CopyTo(thisSpan);
                break;

            case SelectionOperation.Add:
                for (int i = 0; i < thisSpan.Length; i++)
                {
                    thisSpan[i] = (byte)Math.Min(255, thisSpan[i] + otherSpan[i]);
                }
                break;

            case SelectionOperation.Subtract:
                for (int i = 0; i < thisSpan.Length; i++)
                {
                    thisSpan[i] = (byte)Math.Max(0, thisSpan[i] - otherSpan[i]);
                }
                break;

            case SelectionOperation.Intersect:
                for (int i = 0; i < thisSpan.Length; i++)
                {
                    thisSpan[i] = Math.Min(thisSpan[i], otherSpan[i]);
                }
                break;

            case SelectionOperation.Difference:
                for (int i = 0; i < thisSpan.Length; i++)
                {
                    thisSpan[i] = (byte)Math.Abs(thisSpan[i] - otherSpan[i]);
                }
                break;
        }

        UpdateBounds();
        _isEmpty = Bounds.IsEmpty;
    }

    /// <summary>
    /// Applies feathering (blur) to the selection edges.
    /// </summary>
    public void Feather(float radius)
    {
        if (radius <= 0) return;

        FeatherRadius = radius;

        // Simple box blur approximation for feathering
        int kernelSize = (int)Math.Ceiling(radius) * 2 + 1;
        ApplyBoxBlur(kernelSize);
    }

    private void ApplyBoxBlur(int kernelSize)
    {
        var temp = ArrayPool<byte>.Shared.Rent(_width * _height);
        try
        {
            var src = GetMaskData();
            var dst = temp.AsSpan(0, _width * _height);
            int radius = kernelSize / 2;

            // Horizontal pass
            for (int y = 0; y < _height; y++)
            {
                for (int x = 0; x < _width; x++)
                {
                    int sum = 0, count = 0;
                    for (int kx = -radius; kx <= radius; kx++)
                    {
                        int sx = x + kx;
                        if (sx >= 0 && sx < _width)
                        {
                            sum += src[y * _width + sx];
                            count++;
                        }
                    }
                    dst[y * _width + x] = (byte)(sum / count);
                }
            }

            // Vertical pass
            dst.CopyTo(src);
            for (int y = 0; y < _height; y++)
            {
                for (int x = 0; x < _width; x++)
                {
                    int sum = 0, count = 0;
                    for (int ky = -radius; ky <= radius; ky++)
                    {
                        int sy = y + ky;
                        if (sy >= 0 && sy < _height)
                        {
                            sum += dst[sy * _width + x];
                            count++;
                        }
                    }
                    src[y * _width + x] = (byte)(sum / count);
                }
            }
        }
        finally
        {
            ArrayPool<byte>.Shared.Return(temp);
        }
    }

    /// <summary>
    /// Updates the bounding rectangle based on current selection.
    /// </summary>
    public void UpdateBounds()
    {
        int minX = _width, minY = _height, maxX = -1, maxY = -1;
        var span = GetReadOnlyMaskData();

        for (int y = 0; y < _height; y++)
        {
            for (int x = 0; x < _width; x++)
            {
                if (span[y * _width + x] > 0)
                {
                    minX = Math.Min(minX, x);
                    minY = Math.Min(minY, y);
                    maxX = Math.Max(maxX, x);
                    maxY = Math.Max(maxY, y);
                }
            }
        }

        Bounds = maxX >= 0
            ? new SelectionBounds(minX, minY, maxX - minX + 1, maxY - minY + 1)
            : SelectionBounds.Empty;

        _isEmpty = Bounds.IsEmpty;
    }

    /// <summary>
    /// Creates a copy of this selection.
    /// </summary>
    public Selection Clone()
    {
        var clone = new Selection(_width, _height);
        GetReadOnlyMaskData().CopyTo(clone.GetMaskData());
        clone.Bounds = Bounds;
        clone._isEmpty = _isEmpty;
        clone.FeatherRadius = FeatherRadius;
        return clone;
    }

    public void Dispose()
    {
        if (_disposed) return;

        if (_mask is not null)
        {
            ArrayPool<byte>.Shared.Return(_mask);
            _mask = null;
        }

        _disposed = true;
    }
}

/// <summary>
/// Selection combination operations.
/// </summary>
public enum SelectionOperation
{
    Replace,
    Add,
    Subtract,
    Intersect,
    Difference
}

/// <summary>
/// Bounding rectangle for a selection.
/// </summary>
public readonly record struct SelectionBounds(int X, int Y, int Width, int Height)
{
    public static SelectionBounds Empty => new(0, 0, 0, 0);

    public bool IsEmpty => Width <= 0 || Height <= 0;

    public int Right => X + Width;
    public int Bottom => Y + Height;

    public bool Contains(int x, int y) =>
        x >= X && x < Right && y >= Y && y < Bottom;

    public SelectionBounds Intersect(SelectionBounds other)
    {
        int x = Math.Max(X, other.X);
        int y = Math.Max(Y, other.Y);
        int right = Math.Min(Right, other.Right);
        int bottom = Math.Min(Bottom, other.Bottom);

        return right > x && bottom > y
            ? new SelectionBounds(x, y, right - x, bottom - y)
            : Empty;
    }

    public SelectionBounds Union(SelectionBounds other)
    {
        if (IsEmpty) return other;
        if (other.IsEmpty) return this;

        int x = Math.Min(X, other.X);
        int y = Math.Min(Y, other.Y);
        int right = Math.Max(Right, other.Right);
        int bottom = Math.Max(Bottom, other.Bottom);

        return new SelectionBounds(x, y, right - x, bottom - y);
    }
}
