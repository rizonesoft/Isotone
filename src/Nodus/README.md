# Bezier - Visual SVG Editor

> A production-ready SVG editor built with WPF, SkiaSharp, and Monaco Editor.

![.NET](https://img.shields.io/badge/.NET-10.0-512BD4)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- 🎨 **Visual WYSIWYG Editor** - Edit SVG elements directly on canvas
- ✏️ **Pen Tool** - Create Bezier curves with precision
- 📝 **Monaco Code Editor** - Full SVG syntax highlighting and editing
- 🎭 **Layers Panel** - Organize elements with drag-and-drop
- 🎨 **Color Picker** - Solid fills, gradients, and patterns
- ⚡ **SkiaSharp Rendering** - GPU-accelerated, 60fps canvas
- 🌙 **Dark/Light Themes** - Catppuccin color palette

## Getting Started

### Prerequisites

- Windows 10/11
- .NET 10 SDK
- Visual Studio 2022 or VS Code

### Build

```bash
git clone https://github.com/yourusername/Bezier.git
cd Bezier
dotnet build
```

### Run

```bash
dotnet run --project Bezier.Desktop
```

## Project Structure

```
Bezier/
├── Bezier.Core/        # Domain models, interfaces, services
├── Bezier.Desktop/     # WPF UI, SkiaSharp rendering
└── Bezier.Tests/       # Unit and integration tests
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| UI Framework | WPF + WPF-UI (Fluent Design) |
| Rendering | SkiaSharp + Svg.Skia |
| Code Editor | Monaco (WebView2) |
| Layout | AvalonDock |
| MVVM | CommunityToolkit.Mvvm |

## License

MIT License - see [LICENSE](LICENSE) for details.
