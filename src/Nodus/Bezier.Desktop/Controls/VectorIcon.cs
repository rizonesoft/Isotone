using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Bezier.Desktop.Services;

namespace Bezier.Desktop.Controls;

/// <summary>
/// A reusable vector icon control that renders SVG path data from the IconService.
/// Supports Lucide, Heroicons, and custom SVG paths defined in icons.json.
/// </summary>
/// <remarks>
/// <para><b>Usage:</b></para>
/// <code>&lt;controls:VectorIcon Icon="Magnet" Size="24" /&gt;</code>
/// 
/// <para><b>Defaults:</b></para>
/// <list type="bullet">
///   <item>Stroke rendering with Round line caps and joins (Lucide style)</item>
///   <item>StrokeThickness: 2</item>
///   <item>Stretch: Uniform</item>
/// </list>
/// 
/// <para><b>Adding Icons:</b></para>
/// Add entries to <c>Resources/icons.json</c> with the format:
/// <code>{ "IconName": "M10 10 L20 20..." }</code>
/// </remarks>
public class VectorIcon : Control
{
    static VectorIcon()
    {
        DefaultStyleKeyProperty.OverrideMetadata(typeof(VectorIcon), 
            new FrameworkPropertyMetadata(typeof(VectorIcon)));
    }

    #region Icon Property
    /// <summary>
    /// Gets or sets the icon name to render (must exist in icons.json).
    /// </summary>
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
    /// <summary>
    /// Gets the parsed geometry from the IconService.
    /// </summary>
    public Geometry Geometry
    {
        get => (Geometry)GetValue(GeometryProperty);
        private set => SetValue(GeometryPropertyKey, value);
    }

    private static readonly DependencyPropertyKey GeometryPropertyKey =
        DependencyProperty.RegisterReadOnly(nameof(Geometry), typeof(Geometry), typeof(VectorIcon),
            new PropertyMetadata(Geometry.Empty));

    public static readonly DependencyProperty GeometryProperty = GeometryPropertyKey.DependencyProperty;
    #endregion

    #region Size Property
    /// <summary>
    /// Gets or sets the size (Width and Height) of the icon.
    /// </summary>
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
    /// <summary>
    /// Gets or sets the stroke thickness. Default is 2 (Lucide standard).
    /// </summary>
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
    /// <summary>
    /// Gets or sets whether the icon should be filled instead of stroked.
    /// </summary>
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
