# Contributing to Imago

Thank you for your interest in contributing to Imago!

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include reproduction steps and environment details

### Suggesting Features

1. Check existing feature requests
2. Use the feature request template
3. Describe the use case and benefits

### Code Contributions

1. Fork the repository
2. Create a feature branch from `develop`
3. Follow the coding standards in `STANDARDS.md`
4. Write tests for new functionality
5. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Imago.git

# Install .NET 10 SDK
# https://dotnet.microsoft.com/download/dotnet/10.0

# Restore and build
dotnet restore
dotnet build

# Run tests
dotnet test

# Run the application
dotnet run --project src/Imago.UI
```

## Code Style

- Follow `STANDARDS.md` for coding conventions
- Use `.editorconfig` settings
- Run analyzers before committing
- No warnings in CI builds

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Request review from maintainers

## Code of Conduct

Be respectful and constructive. We're all here to build something great together.
