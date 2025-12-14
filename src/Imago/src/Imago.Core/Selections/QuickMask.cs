namespace Imago.Core.Selections;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Quick Mask mode allows editing a selection as if it were a grayscale image.
/// Red overlay indicates masked (unselected) areas.
/// </summary>
public sealed partial class QuickMask : ObservableObject, IDisposable
{
    private Selection? _originalSelection;
    private Selection? _maskSelection;
    private bool _disposed;

    [ObservableProperty]
    private bool _isActive;

    [ObservableProperty]
    private byte _overlayOpacity = 128;

    [ObservableProperty]
    private uint _overlayColor = 0x80FF0000; // Semi-transparent red (ARGB)

    [ObservableProperty]
    private bool _maskIndicatesSelected = false; // false = mask shows unselected areas

    /// <summary>
    /// Gets the editable mask selection.
    /// </summary>
    public Selection? MaskSelection => _maskSelection;

    /// <summary>
    /// Enters Quick Mask mode, copying the current selection.
    /// </summary>
    public void Enter(Selection currentSelection)
    {
        ArgumentNullException.ThrowIfNull(currentSelection);

        if (IsActive) return;

        _originalSelection = currentSelection.Clone();
        _maskSelection = currentSelection.Clone();

        // If mask shows unselected, invert so painting adds to selection
        if (!MaskIndicatesSelected)
        {
            _maskSelection.Invert();
        }

        IsActive = true;
    }

    /// <summary>
    /// Exits Quick Mask mode and applies the edited mask to the selection.
    /// </summary>
    public Selection? Exit()
    {
        if (!IsActive || _maskSelection is null)
            return null;

        // If mask shows unselected, invert back
        if (!MaskIndicatesSelected)
        {
            _maskSelection.Invert();
        }

        var result = _maskSelection;
        _maskSelection = null;

        _originalSelection?.Dispose();
        _originalSelection = null;

        IsActive = false;

        return result;
    }

    /// <summary>
    /// Cancels Quick Mask mode and restores the original selection.
    /// </summary>
    public Selection? Cancel()
    {
        if (!IsActive)
            return null;

        _maskSelection?.Dispose();
        _maskSelection = null;

        var result = _originalSelection;
        _originalSelection = null;

        IsActive = false;

        return result;
    }

    /// <summary>
    /// Gets the overlay color for rendering (considers opacity and mode).
    /// </summary>
    public (byte R, byte G, byte B, byte A) GetOverlayColor()
    {
        byte a = (byte)((OverlayColor >> 24) & 0xFF);
        byte r = (byte)((OverlayColor >> 16) & 0xFF);
        byte g = (byte)((OverlayColor >> 8) & 0xFF);
        byte b = (byte)(OverlayColor & 0xFF);

        // Apply overlay opacity
        a = (byte)((a * OverlayOpacity) / 255);

        return (r, g, b, a);
    }

    public void Dispose()
    {
        if (_disposed) return;

        _originalSelection?.Dispose();
        _maskSelection?.Dispose();
        _disposed = true;
    }
}
