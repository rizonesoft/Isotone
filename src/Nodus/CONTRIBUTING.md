# Contributing to Bezier

Thank you for your interest in contributing! 🎉

## Development Setup

1. Clone the repository
2. Open `Bezier.sln` in Visual Studio 2022
3. Build and run

## Code Style

- Use C# 12 features where appropriate
- Follow Microsoft's [C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- Use file-scoped namespaces
- Use primary constructors where appropriate
- Use `var` for obvious types

## Project Structure

- **Bezier.Core**: Pure business logic, no UI dependencies
- **Bezier.Desktop**: WPF-specific code, ViewModels, Views
- **Bezier.Tests**: Unit and integration tests

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure tests pass: `dotnet test`
4. Submit a PR with a clear description

## Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Adding tests
