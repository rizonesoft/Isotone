using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Imago.UI.Services;

namespace Imago.UI.Controls;

/// <summary>
/// A reusable vector icon control that renders SVG path data from the IconService.
/// Supports Lucide-style stroke icons and filled icons.
/// </summary>
/// <remarks>
/// <para><b>Usage:</b></para>
/// <code>&lt;controls:VectorIcon Icon="Brush" Size="24" /&gt;</code>
/// </remarks>
public class VectorIcon : Control
{
    static VectorIcon()
    {
        DefaultStyleKeyProperty.OverrideMetadata(typeof(VectorIcon),
            new FrameworkPropertyMetadata(typeof(VectorIcon)));
    }

    #region Icon Property
    public string Icon
    {
        get => (string)GetValue(IconProperty);
        set => SetValue(IconProperty, value);
    }

    public static readonly DependencyProperty IconProperty =
        DependencyProperty.Register(nameof(Icon), typeof(string), typeof(VectorIcon),
            new PropertyMetadata(string.Empty, OnIconChanged));

    private static void OnIconChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is VectorIcon icon)
        {
            icon.UpdateGeometry();
        }
    }
    #endregion

    #region Geometry Property (Read-Only)
    public Geometry Geometry
    {
        get => (Geometry)GetValue(GeometryProperty);
        private set => SetValue(s_geometryPropertyKey, value);
    }

    private static readonly DependencyPropertyKey s_geometryPropertyKey =
        DependencyProperty.RegisterReadOnly(nameof(Geometry), typeof(Geometry), typeof(VectorIcon),
            new PropertyMetadata(Geometry.Empty));

    public static readonly DependencyProperty GeometryProperty = s_geometryPropertyKey.DependencyProperty;
    #endregion

    #region Size Property
    public double Size
    {
        get => (double)GetValue(SizeProperty);
        set => SetValue(SizeProperty, value);
    }

    public static readonly DependencyProperty SizeProperty =
        DependencyProperty.Register(nameof(Size), typeof(double), typeof(VectorIcon),
            new PropertyMetadata(24.0, OnSizeChanged));

    private static void OnSizeChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is VectorIcon icon && e.NewValue is double size)
        {
            icon.Width = size;
            icon.Height = size;
        }
    }
    #endregion

    #region StrokeThickness Property
    public double StrokeThickness
    {
        get => (double)GetValue(StrokeThicknessProperty);
        set => SetValue(StrokeThicknessProperty, value);
    }

    public static readonly DependencyProperty StrokeThicknessProperty =
        DependencyProperty.Register(nameof(StrokeThickness), typeof(double), typeof(VectorIcon),
            new PropertyMetadata(2.0));
    #endregion

    #region IsFilled Property
    public bool IsFilled
    {
        get => (bool)GetValue(IsFilledProperty);
        set => SetValue(IsFilledProperty, value);
    }

    public static readonly DependencyProperty IsFilledProperty =
        DependencyProperty.Register(nameof(IsFilled), typeof(bool), typeof(VectorIcon),
            new PropertyMetadata(false));
    #endregion

    private void UpdateGeometry()
    {
        if (string.IsNullOrEmpty(Icon))
        {
            Geometry = Geometry.Empty;
            return;
        }

        Geometry = IconService.Instance.GetGeometry(Icon);
    }

    public override void OnApplyTemplate()
    {
        base.OnApplyTemplate();
        UpdateGeometry();
    }
}
