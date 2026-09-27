# VectorIcon Component

A reusable WPF control for rendering SVG vector icons from the centralized `IconService`.

## Features

- **Simple API**: Just set `Icon="IconName"` to render any icon defined in `icons.json`.
- **Lucide-style Defaults**: Stroked rendering with round line caps and joins (standard for Lucide, Heroicons, etc.).
- **Flexible**: Supports both **Stroke** (default) and **Fill** rendering modes via `IsFilled` property.
- **Dynamic Sizing**: Use the `Size` property to set both Width and Height simultaneously.
- **Theming**: Respects `Foreground` property for color, making it easy to integrate with existing styles.

---

## Usage

### Basic Usage

```xml
<controls:VectorIcon Icon="Magnet" Size="24" />
```

### With Custom Foreground

```xml
<controls:VectorIcon Icon="Magnet" Size="18" Foreground="Orange" />
```

### Filled Mode (for solid icons)

```xml
<controls:VectorIcon Icon="Magnet" Size="24" IsFilled="True" />
```

### Dynamic Color via Binding

```xml
<controls:VectorIcon Icon="Magnet" Size="18" 
                     Foreground="{Binding Foreground, RelativeSource={RelativeSource AncestorType=ToggleButton}}" />
```

### With Style Triggers

```xml
<controls:VectorIcon Icon="Magnet" Size="12">
    <controls:VectorIcon.Style>
        <Style TargetType="controls:VectorIcon">
            <Setter Property="Foreground" Value="{StaticResource SubtextBrush}"/>
            <Style.Triggers>
                <DataTrigger Binding="{Binding IsEnabled}" Value="True">
                    <Setter Property="Foreground" Value="{StaticResource AccentBrush}"/>
                </DataTrigger>
            </Style.Triggers>
        </Style>
    </controls:VectorIcon.Style>
</controls:VectorIcon>
```

---

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Icon` | `string` | `""` | Name of the icon (must exist in `icons.json`) |
| `Size` | `double` | `24` | Sets both Width and Height |
| `StrokeThickness` | `double` | `2` | Stroke width (Lucide default is 2) |
| `IsFilled` | `bool` | `false` | If true, fills the icon instead of stroking |
| `Foreground` | `Brush` | `SubtextBrush` | Color (stroke or fill depending on mode) |

---

## Adding New Icons

1. Open `Bezier.Desktop/Resources/icons.json`.
2. Add a new entry with the icon name and SVG path data:

```json
{
  "Magnet": "M12 15 l4 4 M2.352...",
  "NewIcon": "M10 10 L20 20 Z"
}
```

3. Use in XAML:

```xml
<controls:VectorIcon Icon="NewIcon" Size="24" />
```

### Importing from Lucide / Heroicons

1. Visit [Lucide](https://lucide.dev/icons) or [Heroicons](https://heroicons.com/).
2. Copy the `<path d="...">` attribute value.
3. Add to `icons.json` with a descriptive name.

> **Note**: Lucide icons use `stroke-width="2"` and `stroke-linecap="round"` by default. VectorIcon matches these defaults.

---

## Architecture

```
Bezier.Desktop/
├── Controls/
│   └── VectorIcon.cs         # Custom control
├── Themes/
│   └── Generic.xaml          # Default style & template
├── Resources/
│   └── icons.json            # Icon path database
├── Services/
│   └── IconService.cs        # Loads & caches geometries
└── Helpers/
    └── IconExtension.cs      # MarkupExtension (optional)
```

---

## Troubleshooting

### Icon not appearing?
- Verify the icon name exists in `icons.json`.
- Check for typos in the path data.
- Ensure `IconService.Instance.Initialize()` is called in `App.xaml.cs`.

### Icon appears distorted?
- Ensure the path uses **absolute** Move commands (`M`) at the start of each sub-path.
- Lucide icons are designed for a 24x24 viewport with `stroke-width="2"`.

---

## See Also

- [IconService](../services/icon-service.md) - Icon loading and caching
- [icons.json](../../Bezier.Desktop/Resources/icons.json) - Icon definitions
