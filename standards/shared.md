# Shared Standards for Photon (Rizonesoft Graphics Suite)

> Cross-cutting standards that apply to all apps (Nodus, Imago, Lumen) and `src/Photon.Core`.

## UI Framework Decision

**WPF-UI will NOT be used.** All applications use standard WPF with custom theming and controls.

### Rationale
- Full control over UI appearance and behavior
- No external UI library dependencies
- Consistent theming across all three apps
- Custom controls tailored to each app's needs

### What to Use Instead
- **Standard WPF** for all UI components
- **CommunityToolkit.Mvvm** for MVVM patterns:
  - `ObservableObject` for ViewModels
  - `RelayCommand` / `AsyncRelayCommand` for commands
  - `Ioc` for dependency injection
  - `IMessenger` for messaging
- **Custom WPF controls** developed as needed
- **Custom ResourceDictionaries** for theming (dark/light themes)

### Migration Notes
When importing code from `previous-dev/`:
- Remove any `WPF-UI` NuGet package references
- Replace `FluentWindow` with standard `Window` or custom base window class
- Replace WPF-UI controls with standard WPF equivalents or custom controls
- Preserve theming and styling using standard WPF ResourceDictionaries

---

## Logging Standards

### Framework
- Use **Serilog** for structured logging across all apps
- Logs written to `build/artifacts/logs/` directory
- Rotate logs daily, keep last 7 days

### Log Levels
| Level | Usage |
|-------|-------|
| `Verbose` | Detailed debugging, inner loops |
| `Debug` | Development diagnostics |
| `Information` | Normal operations (file opened, saved) |
| `Warning` | Recoverable issues, deprecated usage |
| `Error` | Errors that affect operation but app continues |
| `Fatal` | Application-terminating errors |

### Structured Logging Pattern
```csharp
// ✅ Good - Structured logging
Log.Information("Document {FileName} loaded in {Duration}ms", 
    fileName, stopwatch.ElapsedMilliseconds);

// ❌ Bad - String interpolation (loses structure)
Log.Information($"Document {fileName} loaded");
```

---

## Error Handling Standards

### Exception Guidelines
- Use specific exception types (`ArgumentNullException`, `InvalidOperationException`, etc.)
- Wrap exceptions with context when rethrowing
- Never catch and swallow silently
- Log all exceptions with context

### Global Exception Handling
- All apps must have a global unhandled exception handler
- Crash reports stored in `build/artifacts/logs/`
- User-friendly error dialogs with option to copy stack trace

### Result Pattern for Expected Failures
```csharp
public readonly record struct Result<T>
{
    public T? Value { get; }
    public string? Error { get; }
    public bool IsSuccess => Error is null;
    
    public static Result<T> Success(T value) => new() { Value = value };
    public static Result<T> Failure(string error) => new() { Error = error };
}
```

---

## Versioning Standards

See `standards/release.md` for detailed versioning rules.

### Format
- SemVer: `major.minor.patch`
- App-specific prefixes: `nodus-1.0.0`, `imago-1.0.0`, `lumen-1.0.0`
- `Photon.Core` versioned independently

---

## Testing Standards

See `standards/testing.md` for detailed testing strategy.

### Minimum Requirements
- Unit tests for all core logic
- Integration tests for file I/O
- UI automation tests for critical workflows
- >80% code coverage target for `Photon.Core`

---

## Dependency Injection

### Framework
- Use `Microsoft.Extensions.DependencyInjection`
- Register services in app startup
- Use constructor injection

### Service Lifetimes
| Lifetime | Usage |
|----------|-------|
| `Singleton` | Shared state, expensive to create (ILogger, ISettingsService) |
| `Scoped` | Per-operation state (IUndoService per document) |
| `Transient` | Lightweight, stateless (ISvgParser, IExporter) |

---

## Git Commit Conventions

### Conventional Commits Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Commit Types
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes bug nor adds feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |

---

*Last Updated: 2025-01-XX*

