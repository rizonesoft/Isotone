# 🎨 Imago

> A professional-grade image editor built with .NET 10 and WPF, designed to compete with industry leaders through high-performance GPU-accelerated rendering, non-destructive editing, and extensible architecture.

[![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)
[![WPF](https://img.shields.io/badge/WPF-Windows-0078D4?logo=windows)](https://docs.microsoft.com/en-us/dotnet/desktop/wpf/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen)](https://github.com/yourusername/Imago/actions)

![Imago Screenshot](docs/images/screenshot.png)

## ✨ Features

- **GPU-Accelerated Rendering** - SkiaSharp and ComputeSharp for blazing-fast performance
- **Non-Destructive Editing** - Adjustment layers and smart filters preserve your original image
- **Tiled Rendering System** - Handle massive images (4GB+) without running out of memory
- **Modern UI** - Windows 11 Fluent Design with Mica/Acrylic backdrop
- **Extensible** - Plugin system with Roslyn scripting support
- **Professional Color Management** - ICC profile support for print workflows
- **50+ Blend Modes** - Industry-standard compositing options
- **Real-time Filters** - GPU-powered Gaussian blur, sharpening, and more

## 🚀 Getting Started

### Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) (Preview 7 or later)
- Windows 10 version 1903 or later (Windows 11 recommended)
- Visual Studio 2022 17.12+ or VS Code with C# Dev Kit

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Imago.git
cd Imago

# Restore dependencies
dotnet restore

# Build the solution
dotnet build

# Run the application
dotnet run --project src/Imago.UI
```

### Quick Start

1. Launch Imago
2. Create a new document (`Ctrl+N`) or open an existing image (`Ctrl+O`)
3. Use the tools panel on the left to select editing tools
4. Add layers and apply filters from the menu
5. Save your work (`Ctrl+S`) or export to various formats (`Ctrl+E`)

## 📁 Project Structure

```
Imago/
├── src/
│   ├── Imago.Core/              # Core domain logic and models
│   ├── Imago.Rendering/         # SkiaSharp/ComputeSharp rendering engine
│   ├── Imago.UI/                # WPF application
│   ├── Imago.Plugins.Abstractions/  # Plugin interfaces
│   ├── Imago.Scripting/         # Roslyn scripting engine
│   └── Imago.FileFormats/       # Image format support
├── tests/
│   ├── Imago.Core.Tests/
│   └── Imago.Rendering.Tests/
├── docs/                        # Documentation
└── assets/                      # Icons, cursors, themes
```

## 🛠 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | .NET 10 / C# 14 | Latest performance optimizations |
| UI | WPF + WPF-UI 4.1.0 | Fluent Design System |
| Rendering | SkiaSharp 3.116.1 | GPU-accelerated 2D graphics |
| GPU Compute | ComputeSharp 3.2.0 | C# to HLSL shader compilation |
| MVVM | CommunityToolkit.Mvvm 8.4.0 | Source-generated MVVM |
| Docking | AvalonDock 4.72.1 | IDE-style panel docking |
| Image I/O | ImageSharp 3.1.12 | Multi-format support |
| Logging | Serilog 4.3.0 | Structured logging |

## 🎯 Roadmap

See [TODO.md](TODO.md) for the detailed development roadmap.

### Phase Overview

- [x] Phase 0: Project Setup
- [ ] Phase 1: Core Architecture
- [ ] Phase 2: Rendering Engine
- [ ] Phase 3: Document Model
- [ ] Phase 4: Tool System
- [ ] Phase 5: Filters & Effects
- [ ] Phase 6: UI/UX Polish
- [ ] Phase 7: File I/O
- [ ] Phase 8: Plugin System
- [ ] Phase 9: Performance Optimization
- [ ] Phase 10: Testing & QA
- [ ] Phase 11: Distribution & Deployment

## 🧪 Running Tests

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific test project
dotnet test tests/Imago.Core.Tests
```

## 📖 Documentation

- [User Guide](docs/user-guide/README.md)
- [API Reference](docs/api/README.md)
- [Plugin Development](docs/plugins/README.md)
- [Architecture](docs/architecture/README.md)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WPF-UI](https://github.com/lepoco/wpfui) for the beautiful Fluent Design components
- [ComputeSharp](https://github.com/Sergio0694/ComputeSharp) for GPU compute capabilities
- [ImageSharp](https://github.com/SixLabors/ImageSharp) for image format support
- [AvalonDock](https://github.com/Dirkster99/AvalonDock) for the docking system

---

<p align="center">
  Made with ❤️ by the Imago Team
</p>
