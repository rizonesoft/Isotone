namespace Imago.Core.Colors;

using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

/// <summary>
/// Represents a 32-bit RGBA color (8 bits per channel).
/// Optimized for zero-allocation operations.
/// </summary>
[StructLayout(LayoutKind.Explicit, Size = 4)]
public readonly struct Rgba32 : IEquatable<Rgba32>
{
    [FieldOffset(0)] public readonly byte R;
    [FieldOffset(1)] public readonly byte G;
    [FieldOffset(2)] public readonly byte B;
    [FieldOffset(3)] public readonly byte A;
    [FieldOffset(0)] public readonly uint PackedValue;

    public Rgba32(byte r, byte g, byte b, byte a = 255)
    {
        Unsafe.SkipInit(out this);
        R = r;
        G = g;
        B = b;
        A = a;
    }

    public Rgba32(uint packed)
    {
        Unsafe.SkipInit(out this);
        PackedValue = packed;
    }

    /// <summary>
    /// Creates from normalized float values (0-1).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public static Rgba32 FromNormalized(float r, float g, float b, float a = 1f)
    {
        return new Rgba32(
            (byte)(Math.Clamp(r, 0f, 1f) * 255f + 0.5f),
            (byte)(Math.Clamp(g, 0f, 1f) * 255f + 0.5f),
            (byte)(Math.Clamp(b, 0f, 1f) * 255f + 0.5f),
            (byte)(Math.Clamp(a, 0f, 1f) * 255f + 0.5f));
    }

    /// <summary>
    /// Converts to normalized float values (0-1).
    /// </summary>
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    public readonly (float R, float G, float B, float A) ToNormalized()
    {
        const float scale = 1f / 255f;
        return (R * scale, G * scale, B * scale, A * scale);
    }

    /// <summary>
    /// Creates from hex string (#RRGGBB or #RRGGBBAA).
    /// </summary>
    public static Rgba32 FromHex(ReadOnlySpan<char> hex)
    {
        if (hex.Length > 0 && hex[0] == '#')
            hex = hex[1..];

        if (hex.Length == 6)
        {
            return new Rgba32(
                Convert.ToByte(hex[..2].ToString(), 16),
                Convert.ToByte(hex[2..4].ToString(), 16),
                Convert.ToByte(hex[4..6].ToString(), 16));
        }

        if (hex.Length == 8)
        {
            return new Rgba32(
                Convert.ToByte(hex[..2].ToString(), 16),
                Convert.ToByte(hex[2..4].ToString(), 16),
                Convert.ToByte(hex[4..6].ToString(), 16),
                Convert.ToByte(hex[6..8].ToString(), 16));
        }

        return default;
    }

    /// <summary>
    /// Converts to hex string.
    /// </summary>
    public readonly string ToHex(bool includeAlpha = false)
    {
        return includeAlpha
            ? $"#{R:X2}{G:X2}{B:X2}{A:X2}"
            : $"#{R:X2}{G:X2}{B:X2}";
    }

    // Common colors
    public static Rgba32 Transparent => new(0, 0, 0, 0);
    public static Rgba32 Black => new(0, 0, 0);
    public static Rgba32 White => new(255, 255, 255);
    public static Rgba32 Red => new(255, 0, 0);
    public static Rgba32 Green => new(0, 255, 0);
    public static Rgba32 Blue => new(0, 0, 255);

    public bool Equals(Rgba32 other) => PackedValue == other.PackedValue;
    public override bool Equals(object? obj) => obj is Rgba32 other && Equals(other);
    public override int GetHashCode() => (int)PackedValue;
    public override string ToString() => $"RGBA({R}, {G}, {B}, {A})";

    public static bool operator ==(Rgba32 left, Rgba32 right) => left.Equals(right);
    public static bool operator !=(Rgba32 left, Rgba32 right) => !left.Equals(right);
}
