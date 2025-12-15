namespace Bezier.Desktop.Controls;

using System.Data;
using System.Globalization;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Automation.Peers;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Input;
using System.Windows.Media;

/// <summary>
/// A compact number input control with drag-to-scrub, mouse wheel, math expressions, and more.
/// </summary>
public class CompactNumberBox : Control
{
    private const double DefaultDpi = 96.0;
    
    // Cached regex for unit parsing (compiled for performance)
    private static readonly Regex UnitPattern = new(
        @"([\d.]+)\s*(in|inch|inches|mm|cm|pt|pc|%)", 
        RegexOptions.IgnoreCase | RegexOptions.Compiled);
    
    // Cached regex for math sanitization
    private static readonly Regex MathSanitizePattern = new(
        @"[^0-9+\-*/().,%\s]", 
        RegexOptions.Compiled);
    
    // Cached DataTable for math evaluation (reused to avoid allocations)
    private static readonly DataTable MathEvaluator = new();
    
    // Cached format strings
    private static readonly string[] DecimalFormatStrings = [
        "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"
    ];
    
    // Cached action for select all (avoid lambda allocation)
    private Action? _selectAllAction;
    
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
            new PropertyMetadata(double.MinValue, OnRangeChanged));

    public static readonly DependencyProperty MaximumProperty =
        DependencyProperty.Register(nameof(Maximum), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(double.MaxValue, OnRangeChanged));

    public static readonly DependencyProperty StepProperty =
        DependencyProperty.Register(nameof(Step), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(1.0));

    public static readonly DependencyProperty LargeStepMultiplierProperty =
        DependencyProperty.Register(nameof(LargeStepMultiplier), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(10.0));

    public static readonly DependencyProperty SmallStepMultiplierProperty =
        DependencyProperty.Register(nameof(SmallStepMultiplier), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(0.1));

    public static readonly DependencyProperty PlaceholderTextProperty =
        DependencyProperty.Register(nameof(PlaceholderText), typeof(string), typeof(CompactNumberBox),
            new PropertyMetadata(string.Empty));

    public static readonly DependencyProperty SuffixProperty =
        DependencyProperty.Register(nameof(Suffix), typeof(string), typeof(CompactNumberBox),
            new PropertyMetadata(string.Empty));

    public static readonly DependencyProperty PrefixProperty =
        DependencyProperty.Register(nameof(Prefix), typeof(string), typeof(CompactNumberBox),
            new PropertyMetadata(string.Empty));

    public static readonly DependencyProperty ShowClearButtonProperty =
        DependencyProperty.Register(nameof(ShowClearButton), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(true));

    public static readonly DependencyProperty EnableDragToScrubProperty =
        DependencyProperty.Register(nameof(EnableDragToScrub), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(true));

    public static readonly DependencyProperty EnableMouseWheelProperty =
        DependencyProperty.Register(nameof(EnableMouseWheel), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(true));

    public static readonly DependencyProperty EnableArrowKeysProperty =
        DependencyProperty.Register(nameof(EnableArrowKeys), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(true));

    public static readonly DependencyProperty SelectAllOnFocusProperty =
        DependencyProperty.Register(nameof(SelectAllOnFocus), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(true));

    public static readonly DependencyProperty ShowSpinButtonsProperty =
        DependencyProperty.Register(nameof(ShowSpinButtons), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(false));

    public static readonly DependencyProperty ShowProgressBarProperty =
        DependencyProperty.Register(nameof(ShowProgressBar), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(false));

    public static readonly DependencyProperty IsOutOfRangeProperty =
        DependencyProperty.Register(nameof(IsOutOfRange), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(false));

    public static readonly DependencyProperty ProgressPercentageProperty =
        DependencyProperty.Register(nameof(ProgressPercentage), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(0.0));

    public static readonly DependencyProperty DecimalPlacesProperty =
        DependencyProperty.Register(nameof(DecimalPlaces), typeof(int), typeof(CompactNumberBox),
            new PropertyMetadata(0));

    public static readonly DependencyProperty AutoWidthProperty =
        DependencyProperty.Register(nameof(AutoWidth), typeof(bool), typeof(CompactNumberBox),
            new PropertyMetadata(false, OnAutoWidthChanged));


    public static readonly DependencyProperty CharacterWidthProperty =
        DependencyProperty.Register(nameof(CharacterWidth), typeof(double), typeof(CompactNumberBox),
            new PropertyMetadata(7.0, OnAutoWidthChanged)); // Approximate width per character at FontSize 11

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

    public double Step
    {
        get => (double)GetValue(StepProperty);
        set => SetValue(StepProperty, value);
    }

    public double LargeStepMultiplier
    {
        get => (double)GetValue(LargeStepMultiplierProperty);
        set => SetValue(LargeStepMultiplierProperty, value);
    }

    public double SmallStepMultiplier
    {
        get => (double)GetValue(SmallStepMultiplierProperty);
        set => SetValue(SmallStepMultiplierProperty, value);
    }

    public string PlaceholderText
    {
        get => (string)GetValue(PlaceholderTextProperty);
        set => SetValue(PlaceholderTextProperty, value);
    }

    public string Suffix
    {
        get => (string)GetValue(SuffixProperty);
        set => SetValue(SuffixProperty, value);
    }

    public string Prefix
    {
        get => (string)GetValue(PrefixProperty);
        set => SetValue(PrefixProperty, value);
    }

    public bool ShowClearButton
    {
        get => (bool)GetValue(ShowClearButtonProperty);
        set => SetValue(ShowClearButtonProperty, value);
    }

    public bool EnableDragToScrub
    {
        get => (bool)GetValue(EnableDragToScrubProperty);
        set => SetValue(EnableDragToScrubProperty, value);
    }

    public bool EnableMouseWheel
    {
        get => (bool)GetValue(EnableMouseWheelProperty);
        set => SetValue(EnableMouseWheelProperty, value);
    }

    public bool EnableArrowKeys
    {
        get => (bool)GetValue(EnableArrowKeysProperty);
        set => SetValue(EnableArrowKeysProperty, value);
    }

    public bool SelectAllOnFocus
    {
        get => (bool)GetValue(SelectAllOnFocusProperty);
        set => SetValue(SelectAllOnFocusProperty, value);
    }

    public bool ShowSpinButtons
    {
        get => (bool)GetValue(ShowSpinButtonsProperty);
        set => SetValue(ShowSpinButtonsProperty, value);
    }

    public bool ShowProgressBar
    {
        get => (bool)GetValue(ShowProgressBarProperty);
        set => SetValue(ShowProgressBarProperty, value);
    }

    public bool IsOutOfRange
    {
        get => (bool)GetValue(IsOutOfRangeProperty);
        private set => SetValue(IsOutOfRangeProperty, value);
    }

    public double ProgressPercentage
    {
        get => (double)GetValue(ProgressPercentageProperty);
        private set => SetValue(ProgressPercentageProperty, value);
    }

    public int DecimalPlaces
    {
        get => (int)GetValue(DecimalPlacesProperty);
        set => SetValue(DecimalPlacesProperty, value);
    }

    public bool AutoWidth
    {
        get => (bool)GetValue(AutoWidthProperty);
        set => SetValue(AutoWidthProperty, value);
    }

    public double CharacterWidth
    {
        get => (double)GetValue(CharacterWidthProperty);
        set => SetValue(CharacterWidthProperty, value);
    }

    #endregion

    private TextBox? _textBox;
    private Button? _clearButton;
    private RepeatButton? _incrementButton;
    private RepeatButton? _decrementButton;
    private Border? _contentBorder;
    private FrameworkElement? _scrubZone;
    private bool _isUpdating;
    
    // Drag-to-scrub state
    private bool _isDragging;
    private Point _dragStartPoint;
    private double _dragStartValue;
    private double _lastDragValue;
    private const double DragSensitivity = 2.0; // pixels per unit step (higher = less sensitive)

    public override void OnApplyTemplate()
    {
        base.OnApplyTemplate();

        // Unsubscribe from old elements
        if (_textBox is not null)
        {
            _textBox.LostFocus -= OnTextBoxLostFocus;
            _textBox.GotFocus -= OnTextBoxGotFocus;
            _textBox.KeyDown -= OnTextBoxKeyDown;
            _textBox.PreviewKeyDown -= OnTextBoxPreviewKeyDown;
            _textBox.TextChanged -= OnTextBoxTextChanged;
            _textBox.PreviewMouseWheel -= OnTextBoxPreviewMouseWheel;
        }

        if (_scrubZone is not null)
        {
            _scrubZone.MouseLeftButtonDown -= OnScrubZoneMouseLeftButtonDown;
            _scrubZone.MouseMove -= OnScrubZoneMouseMove;
            _scrubZone.MouseLeftButtonUp -= OnScrubZoneMouseLeftButtonUp;
        }

        _textBox = GetTemplateChild("PART_TextBox") as TextBox;
        _clearButton = GetTemplateChild("PART_ClearButton") as Button;
        _incrementButton = GetTemplateChild("PART_IncrementButton") as RepeatButton;
        _decrementButton = GetTemplateChild("PART_DecrementButton") as RepeatButton;
        _contentBorder = GetTemplateChild("ContentBorder") as Border;
        _scrubZone = GetTemplateChild("PART_ScrubZone") as FrameworkElement;

        if (_textBox is not null)
        {
            _textBox.Text = FormatValue(Value);
            _textBox.LostFocus += OnTextBoxLostFocus;
            _textBox.GotFocus += OnTextBoxGotFocus;
            _textBox.KeyDown += OnTextBoxKeyDown;
            _textBox.PreviewKeyDown += OnTextBoxPreviewKeyDown;
            _textBox.TextChanged += OnTextBoxTextChanged;
            _textBox.PreviewMouseWheel += OnTextBoxPreviewMouseWheel;
        }

        // Scrub zone handles drag-to-scrub (like Figma: drag on label to scrub)
        if (_scrubZone is not null)
        {
            _scrubZone.MouseLeftButtonDown += OnScrubZoneMouseLeftButtonDown;
            _scrubZone.MouseMove += OnScrubZoneMouseMove;
            _scrubZone.MouseLeftButtonUp += OnScrubZoneMouseLeftButtonUp;
        }

        if (_clearButton is not null)
        {
            _clearButton.Click += OnClearButtonClick;
        }

        if (_incrementButton is not null)
        {
            _incrementButton.Click += OnIncrementClick;
        }

        if (_decrementButton is not null)
        {
            _decrementButton.Click += OnDecrementClick;
        }

        UpdateProgressPercentage();
        UpdateTooltip();
        UpdateAutoWidth();
    }

    #region Static Callbacks

    private static void OnValueChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is CompactNumberBox control && !control._isUpdating)
        {
            control.UpdateTextFromValue();
            control.UpdateProgressPercentage();
            control.AnnounceValueChange((double)e.NewValue);
        }
    }

    private static void OnRangeChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is CompactNumberBox control)
        {
            control.UpdateProgressPercentage();
            control.UpdateTooltip();
            control.UpdateAutoWidth();
        }
    }

    private static void OnAutoWidthChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is CompactNumberBox control)
        {
            control.UpdateAutoWidth();
        }
    }

    #endregion

    #region Value Formatting and Parsing

    private string FormatValue(double value)
    {
        if (DecimalPlaces > 0 && DecimalPlaces < DecimalFormatStrings.Length)
        {
            return value.ToString(DecimalFormatStrings[DecimalPlaces], CultureInfo.CurrentCulture);
        }
        return value.ToString(CultureInfo.CurrentCulture);
    }

    private void UpdateTextFromValue()
    {
        if (_textBox is not null && !_isUpdating)
        {
            _isUpdating = true;
            _textBox.Text = FormatValue(Value);
            _isUpdating = false;
        }
    }

    private void UpdateProgressPercentage()
    {
        if (Maximum > Minimum)
        {
            ProgressPercentage = Math.Clamp((Value - Minimum) / (Maximum - Minimum) * 100, 0, 100);
        }
        else
        {
            ProgressPercentage = 0;
        }
    }

    private void UpdateTooltip()
    {
        if (Minimum != double.MinValue && Maximum != double.MaxValue)
        {
            ToolTip = $"Range: {Minimum} – {Maximum}";
        }
    }

    private void UpdateAutoWidth()
    {
        if (!AutoWidth) return;

        // Calculate character count needed
        int maxValueDigits = Maximum != double.MaxValue 
            ? Math.Max(Maximum.ToString("F0").Length, Minimum.ToString("F0").Length)
            : 6; // Default for unbounded

        // Add decimal places if any
        if (DecimalPlaces > 0)
        {
            maxValueDigits += DecimalPlaces + 1; // +1 for decimal point
        }

        // Add prefix and suffix lengths
        int prefixLen = string.IsNullOrEmpty(Prefix) ? 0 : Prefix.Length + 1; // +1 for spacing
        int suffixLen = string.IsNullOrEmpty(Suffix) ? 0 : Suffix.Length + 1; // +1 for spacing

        // Scrub zone takes some space (drag handle or prefix)
        int scrubZoneChars = EnableDragToScrub ? (string.IsNullOrEmpty(Prefix) ? 2 : 0) : 0;

        int totalChars = maxValueDigits + prefixLen + suffixLen + scrubZoneChars;

        // Calculate width: characters * char width + padding for borders, clear button, etc.
        double padding = 24; // For borders, clear button space, margins
        double calculatedWidth = (totalChars * CharacterWidth) + padding;

        // Apply MaxWidth constraint
        if (MaxWidth > 0 && MaxWidth < double.PositiveInfinity)
        {
            calculatedWidth = Math.Min(calculatedWidth, MaxWidth);
        }

        // Set minimum reasonable width
        calculatedWidth = Math.Max(calculatedWidth, 50);

        Width = calculatedWidth;
    }

    #endregion

    #region Focus Handling

    private void OnTextBoxLostFocus(object sender, RoutedEventArgs e)
    {
        CommitValue();
        UpdateClearButtonVisibility();
        IsOutOfRange = false;
    }

    private void OnTextBoxGotFocus(object sender, RoutedEventArgs e)
    {
        UpdateClearButtonVisibility();
        
        if (SelectAllOnFocus && _textBox is not null)
        {
            // Delay to ensure the text box has focus (reuse cached action)
            _selectAllAction ??= () => _textBox?.SelectAll();
            Dispatcher.BeginInvoke(_selectAllAction, System.Windows.Threading.DispatcherPriority.Input);
        }
    }

    #endregion

    #region Keyboard Handling

    private void OnTextBoxKeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter)
        {
            CommitValue();
            e.Handled = true;
        }
        else if (e.Key == Key.Escape)
        {
            // Revert to current value
            if (_textBox is not null)
            {
                _textBox.Text = FormatValue(Value);
                IsOutOfRange = false;
            }
            e.Handled = true;
        }
    }

    private void OnTextBoxPreviewKeyDown(object sender, KeyEventArgs e)
    {
        if (!EnableArrowKeys) return;

        double step = GetEffectiveStep();

        if (e.Key == Key.Up)
        {
            IncrementValue(step);
            e.Handled = true;
        }
        else if (e.Key == Key.Down)
        {
            DecrementValue(step);
            e.Handled = true;
        }
    }

    #endregion

    #region Mouse Handling (Drag-to-Scrub on Scrub Zone)

    // Drag-to-scrub works like Figma/Illustrator:
    // - Drag on the LABEL (scrub zone) to scrub the value
    // - Click on the VALUE (text input) to edit text
    
    private void OnScrubZoneMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        if (!EnableDragToScrub || _scrubZone is null) return;

        _isDragging = true;
        _dragStartPoint = e.GetPosition(this);
        _dragStartValue = Value;
        _lastDragValue = Value;
        _scrubZone.CaptureMouse();
        Mouse.OverrideCursor = Cursors.SizeWE;
        e.Handled = true;
    }

    private void OnScrubZoneMouseMove(object sender, MouseEventArgs e)
    {
        if (!_isDragging) return;

        var currentPoint = e.GetPosition(this);
        var deltaX = currentPoint.X - _dragStartPoint.X;
        var step = GetEffectiveStep();
        var delta = deltaX / DragSensitivity * step;

        var newValue = Math.Clamp(_dragStartValue + delta, Minimum, Maximum);
        newValue = DecimalPlaces > 0 ? Math.Round(newValue, DecimalPlaces) : Math.Round(newValue);
        
        // Only update text preview if value changed (don't update binding during drag)
        if (Math.Abs(newValue - _lastDragValue) < 0.001) return;
        
        _lastDragValue = newValue;
        
        // Only update text display during drag - defer Value binding update until drag ends
        if (_textBox is not null)
        {
            _textBox.Text = FormatValue(newValue);
        }
    }

    private void OnScrubZoneMouseLeftButtonUp(object sender, MouseButtonEventArgs e)
    {
        if (_isDragging && _scrubZone is not null)
        {
            _isDragging = false;
            _scrubZone.ReleaseMouseCapture();
            Mouse.OverrideCursor = null;
            
            // Commit the final value only when drag ends
            if (Math.Abs(_lastDragValue - _dragStartValue) > 0.001)
            {
                _isUpdating = true;
                Value = _lastDragValue;
                _isUpdating = false;
            }
        }
    }

    #endregion

    #region Mouse Wheel Handling

    private void OnTextBoxPreviewMouseWheel(object sender, MouseWheelEventArgs e)
    {
        if (!EnableMouseWheel) return;

        var step = GetEffectiveStep();
        
        if (e.Delta > 0)
        {
            IncrementValue(step);
        }
        else
        {
            DecrementValue(step);
        }

        e.Handled = true;
    }

    #endregion

    #region Text Changed and Validation

    private void OnTextBoxTextChanged(object sender, TextChangedEventArgs e)
    {
        UpdateClearButtonVisibility();
        ValidateCurrentInput();
    }

    private void ValidateCurrentInput()
    {
        if (_textBox is null || _isUpdating) return;

        var text = _textBox.Text;
        if (string.IsNullOrWhiteSpace(text))
        {
            IsOutOfRange = false;
            return;
        }

        // Try to parse with unit conversion and math
        if (TryParseWithUnitsAndMath(text, out var value))
        {
            IsOutOfRange = value < Minimum || value > Maximum;
        }
        else
        {
            IsOutOfRange = false; // Can't determine yet
        }
    }

    private void UpdateClearButtonVisibility()
    {
        if (_clearButton is not null && ShowClearButton)
        {
            bool hasFocus = _textBox?.IsFocused == true || _textBox?.IsKeyboardFocusWithin == true;
            bool hasText = !string.IsNullOrEmpty(_textBox?.Text);
            _clearButton.Visibility = (hasFocus && hasText) ? Visibility.Visible : Visibility.Collapsed;
        }
        else if (_clearButton is not null)
        {
            _clearButton.Visibility = Visibility.Collapsed;
        }
    }

    #endregion

    #region Value Commit and Math/Unit Parsing

    private void CommitValue()
    {
        if (_textBox is null || _isUpdating) return;

        var text = _textBox.Text.Trim();
        
        if (string.IsNullOrEmpty(text))
        {
            // Reset to minimum or 0
            _isUpdating = true;
            Value = Math.Max(Minimum, 0);
            _textBox.Text = FormatValue(Value);
            _isUpdating = false;
            IsOutOfRange = false;
            return;
        }

        if (TryParseWithUnitsAndMath(text, out var value))
        {
            _isUpdating = true;
            Value = Math.Clamp(value, Minimum, Maximum);
            _textBox.Text = FormatValue(Value);
            _isUpdating = false;
            IsOutOfRange = false;
        }
        else
        {
            // Revert to current value
            _textBox.Text = FormatValue(Value);
            IsOutOfRange = false;
        }
    }

    private bool TryParseWithUnitsAndMath(string text, out double result)
    {
        result = 0;
        text = text.Trim();

        // First, try to handle unit conversions
        text = ConvertUnitsToPixels(text);

        // Then, try to evaluate math expressions
        if (TryEvaluateMath(text, out result))
        {
            if (DecimalPlaces > 0)
            {
                result = Math.Round(result, DecimalPlaces);
            }
            return true;
        }

        return false;
    }

    private string ConvertUnitsToPixels(string text)
    {
        // Use cached compiled regex for better performance
        return UnitPattern.Replace(text, match =>
        {
            if (!double.TryParse(match.Groups[1].Value, NumberStyles.Float, CultureInfo.InvariantCulture, out var number))
                return match.Value;

            var unit = match.Groups[2].Value.ToLowerInvariant();
            double pixels = unit switch
            {
                "in" or "inch" or "inches" => number * DefaultDpi,
                "mm" => number * DefaultDpi / 25.4,
                "cm" => number * DefaultDpi / 2.54,
                "pt" => number * DefaultDpi / 72.0,
                "pc" => number * DefaultDpi / 6.0,
                "%" => Value * number / 100.0, // Percentage of current value
                _ => number
            };

            return pixels.ToString(CultureInfo.InvariantCulture);
        });
    }

    private bool TryEvaluateMath(string expression, out double result)
    {
        result = 0;

        // Simple direct parse first
        if (double.TryParse(expression, NumberStyles.Float, CultureInfo.InvariantCulture, out result))
            return true;

        // Try with current culture
        if (double.TryParse(expression, NumberStyles.Float, CultureInfo.CurrentCulture, out result))
            return true;

        // Try to evaluate as math expression
        try
        {
            // Basic sanitization - only allow numbers and math operators (use cached regex)
            var sanitized = MathSanitizePattern.Replace(expression, "");
            if (string.IsNullOrWhiteSpace(sanitized)) return false;

            // Replace comma with dot for decimal separator
            sanitized = sanitized.Replace(',', '.');

            // Use cached DataTable for math evaluation (avoid allocation)
            var computed = MathEvaluator.Compute(sanitized, null);
            
            if (computed is not DBNull && computed is not null)
            {
                result = Convert.ToDouble(computed);
                return true;
            }
        }
        catch
        {
            // Math evaluation failed
        }

        return false;
    }

    #endregion

    #region Increment/Decrement

    private double GetEffectiveStep()
    {
        var step = Step;
        
        if (Keyboard.Modifiers.HasFlag(ModifierKeys.Shift))
        {
            step *= LargeStepMultiplier;
        }
        else if (Keyboard.Modifiers.HasFlag(ModifierKeys.Control))
        {
            step *= SmallStepMultiplier;
        }

        return step;
    }

    private void IncrementValue(double step)
    {
        var newValue = Math.Clamp(Value + step, Minimum, Maximum);
        if (DecimalPlaces > 0)
        {
            newValue = Math.Round(newValue, DecimalPlaces);
        }
        Value = newValue;
    }

    private void DecrementValue(double step)
    {
        var newValue = Math.Clamp(Value - step, Minimum, Maximum);
        if (DecimalPlaces > 0)
        {
            newValue = Math.Round(newValue, DecimalPlaces);
        }
        Value = newValue;
    }

    private void OnIncrementClick(object sender, RoutedEventArgs e)
    {
        IncrementValue(GetEffectiveStep());
        _textBox?.Focus();
    }

    private void OnDecrementClick(object sender, RoutedEventArgs e)
    {
        DecrementValue(GetEffectiveStep());
        _textBox?.Focus();
    }

    private void OnClearButtonClick(object sender, RoutedEventArgs e)
    {
        if (_textBox is not null)
        {
            // Just clear the text for editing - don't change the Value
            _textBox.Text = string.Empty;
            _textBox.Focus();
        }
    }

    #endregion

    #region Accessibility

    private void AnnounceValueChange(double newValue)
    {
        // Announce to screen readers using UI Automation
        if (AutomationPeer.ListenerExists(AutomationEvents.PropertyChanged))
        {
            var peer = UIElementAutomationPeer.FromElement(this);
            peer?.RaisePropertyChangedEvent(
                System.Windows.Automation.RangeValuePatternIdentifiers.ValueProperty,
                null, newValue);
        }
    }

    protected override AutomationPeer OnCreateAutomationPeer()
    {
        return new CompactNumberBoxAutomationPeer(this);
    }

    #endregion
}

/// <summary>
/// Automation peer for CompactNumberBox to support screen readers.
/// </summary>
public class CompactNumberBoxAutomationPeer : FrameworkElementAutomationPeer
{
    public CompactNumberBoxAutomationPeer(CompactNumberBox owner) : base(owner) { }

    protected override string GetClassNameCore() => "CompactNumberBox";

    protected override AutomationControlType GetAutomationControlTypeCore() 
        => AutomationControlType.Spinner;

    protected override string GetNameCore()
    {
        var control = (CompactNumberBox)Owner;
        var name = base.GetNameCore();
        
        if (string.IsNullOrEmpty(name))
        {
            name = $"Number input: {control.Value}";
            if (!string.IsNullOrEmpty(control.Suffix))
                name += $" {control.Suffix}";
        }
        
        return name;
    }
}
