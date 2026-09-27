namespace Pinxit.Core.Masks;

using System.Buffers;
using System.Runtime.CompilerServices;
using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Represents a grayscale mask attached to a layer.
/// White (255) = fully visible, Black (0) = fully hidden.
/// </summary>
public sealed partial class LayerMask : ObservableObject, IDisposable
{
    private byte[]? _data;
    private readonly int _width;
    private readonly int _height;
    private bool _disposed;

    [ObservableProperty]
    private bool _isEnabled = true;

    [ObservableProperty]
    private bool _isLinked = true;

    [ObservableProperty]
    private float _density = 1.0f;

    [ObservableProperty]
    private float _feather;

    [ObservableProperty]
    private bool _isInverted;

    /// <summary>
    /// Gets the width of the mask.
    /// </summary>
    public int Width => _width;

    /// <summary>
    /// Gets the height of the mask.
    /// </summary>
    public int Height => _height;

    /// <summary>
    /// Gets whether the mask has been modified.
    /// </summary>
    public bool IsDirty { get; private set; }

    public LayerMask(int width, int height, byte initialValue = 255)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(width);
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(height);

        _width = width;
        _height = height;
        _data = ArrayPool<byte>.Shared.Rent(width * height);
        Array.Fill(_data, initialValue, 0, width * height);
    }

    /// <summary>
    /// Gets the mask value at a pixel (0-255).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public byte GetValue(int x, int y)
    {
        if (x < 0 || x >= _width || y < 0 || y >= _height)
            return IsInverted ? (byte)255 : (byte)0;

        byte value = _data![y * _width + x];

        if (IsInverted)
            value = (byte)(255 - value);

        // Apply density
        if (Density < 1.0f)
            value = (byte)(value * Density);

        return value;
    }

    /// <summary>
    /// Sets the mask value at a pixel (0-255).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public void SetValue(int x, int y, byte value)
    {
        if (x < 0 || x >= _width || y < 0 || y >= _height)
            return;

        _data![y * _width + x] = value;
        IsDirty = true;
    }

    /// <summary>
    /// Gets a span of the raw mask data (without density/invert applied).
    /// </summary>
    public Span<byte> GetRawData()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        return _data.AsSpan(0, _width * _height);
    }

    /// <summary>
    /// Gets a read-only span of the raw mask data.
    /// </summary>
    public ReadOnlySpan<byte> GetReadOnlyRawData()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        return _data.AsSpan(0, _width * _height);
    }

    /// <summary>
    /// Fills the entire mask with a value.
    /// </summary>
    public void Fill(byte value)
    {
        Array.Fill(_data!, value, 0, _width * _height);
        IsDirty = true;
    }

    /// <summary>
    /// Inverts the mask values.
    /// </summary>
    public void InvertData()
    {
        var span = GetRawData();
        for (int i = 0; i < span.Length; i++)
        {
            span[i] = (byte)(255 - span[i]);
        }
        IsDirty = true;
    }

    /// <summary>
    /// Applies feathering (blur) to the mask.
    /// </summary>
    public void ApplyFeather(float radius)
    {
        if (radius <= 0) return;

        Feather = radius;
        int kernelSize = (int)Math.Ceiling(radius) * 2 + 1;
        ApplyBoxBlur(kernelSize);
    }

    private void ApplyBoxBlur(int kernelSize)
    {
        var temp = ArrayPool<byte>.Shared.Rent(_width * _height);
        try
        {
            var src = GetRawData();
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

            IsDirty = true;
        }
        finally
        {
            ArrayPool<byte>.Shared.Return(temp);
        }
    }

    /// <summary>
    /// Creates a copy of this mask.
    /// </summary>
    public LayerMask Clone()
    {
        var clone = new LayerMask(_width, _height)
        {
            IsEnabled = IsEnabled,
            IsLinked = IsLinked,
            Density = Density,
            Feather = Feather,
            IsInverted = IsInverted
        };
        GetReadOnlyRawData().CopyTo(clone.GetRawData());
        return clone;
    }

    /// <summary>
    /// Marks the mask as clean (not dirty).
    /// </summary>
    public void MarkClean() => IsDirty = false;

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
