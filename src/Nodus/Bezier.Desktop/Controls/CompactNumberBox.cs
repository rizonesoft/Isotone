namespace Bezier.Desktop.Controls;

using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

/// <summary>
/// A compact number input control with centered clear button.
/// </summary>
public class CompactNumberBox : Control
{
    static CompactNumberBox()
    {
        DefaultStyleKeyProperty.OverrideMetadata(typeof(CompactNumberBox), 
            new FrameworkPropertyMetadata(typeof(CompactNumberBox)));
    }

    #region Dependency Properties

    public static readonly DependencyProperty ValueProperty =
        DependencyProperty.Register(nameof(Value), typeof(double), typeof(CompactNumberBox),
            new FrameworkPropertyMetadata(0.0, FrameworkPropertyMetadataOptions.BindsTwoWayByDefault, OnValueChanged));

    public static readonly DependencyProperty MinimumProperty =
        DependencyProperty.Register(nameof(Minimum), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(double.MinValue));

    public static readonly DependencyProperty MaximumProperty =
        DependencyProperty.Register(nameof(Maximum), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(double.MaxValue));

    public static readonly DependencyProperty PlaceholderTextProperty =
        DependencyProperty.Register(nameof(PlaceholderText), typeof(string), typeof(CompactNumberBox),
            new PropertyMetadata(string.Empty));

    public static readonly DependencyProperty ShowClearButtonProperty =
        DependencyProperty.Register(nameof(ShowClearButton), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(true));

    public double Value
    {
        get => (double)GetValue(ValueProperty);
        set => SetValue(ValueProperty, value);
    }

    public double Minimum
    {
        get => (double)GetValue(MinimumProperty);
        set => SetValue(MinimumProperty, value);
    }

    public double Maximum
    {
        get => (double)GetValue(MaximumProperty);
        set => SetValue(MaximumProperty, value);
    }

    public string PlaceholderText
    {
        get => (string)GetValue(PlaceholderTextProperty);
        set => SetValue(PlaceholderTextProperty, value);
    }

    public bool ShowClearButton
    {
        get => (bool)GetValue(ShowClearButtonProperty);
        set => SetValue(ShowClearButtonProperty, value);
    }

    #endregion

    private TextBox? _textBox;
    private Button? _clearButton;
    private bool _isUpdating;

    public override void OnApplyTemplate()
    {
        base.OnApplyTemplate();

        _textBox = GetTemplateChild("PART_TextBox") as TextBox;
        _clearButton = GetTemplateChild("PART_ClearButton") as Button;

        if (_textBox is not null)
        {
            _textBox.Text = Value.ToString();
            _textBox.LostFocus += OnTextBoxLostFocus;
            _textBox.KeyDown += OnTextBoxKeyDown;
            _textBox.TextChanged += OnTextBoxTextChanged;
        }

        if (_clearButton is not null)
        {
            _clearButton.Click += OnClearButtonClick;
        }
    }

    private static void OnValueChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is CompactNumberBox control && !control._isUpdating)
        {
            control.UpdateTextFromValue();
        }
    }

    private void UpdateTextFromValue()
    {
        if (_textBox is not null && !_isUpdating)
        {
            _isUpdating = true;
            _textBox.Text = Value.ToString();
            _isUpdating = false;
        }
    }

    private void OnTextBoxLostFocus(object sender, RoutedEventArgs e)
    {
        CommitValue();
    }

    private void OnTextBoxKeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter)
        {
            CommitValue();
            e.Handled = true;
        }
    }

    private void OnTextBoxTextChanged(object sender, TextChangedEventArgs e)
    {
        // Update clear button visibility
        if (_clearButton is not null && ShowClearButton)
        {
            _clearButton.Visibility = string.IsNullOrEmpty(_textBox?.Text) 
                ? Visibility.Collapsed 
                : Visibility.Visible;
        }
    }

    private void CommitValue()
    {
        if (_textBox is null || _isUpdating) return;

        if (double.TryParse(_textBox.Text, out var value))
        {
            _isUpdating = true;
            Value = Math.Clamp(value, Minimum, Maximum);
            _textBox.Text = Value.ToString();
            _isUpdating = false;
        }
        else
        {
            // Revert to current value
            _textBox.Text = Value.ToString();
        }
    }

    private void OnClearButtonClick(object sender, RoutedEventArgs e)
    {
        if (_textBox is not null)
        {
            _textBox.Text = string.Empty;
            _textBox.Focus();
        }
    }
}
