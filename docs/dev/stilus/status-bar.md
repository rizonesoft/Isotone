# Status Bar

This page describes the C# prototype preserved at the `csharp-final` Git tag, kept as a behavior reference; none of the code it names is on `main`. The native design is in [`docs/design/`](../../design/README.md) and [`docs/specs/2026-10-22-native-stack-design.md`](../../specs/2026-10-22-native-stack-design.md).

The Status Bar at the bottom of the main window provides real-time information about your document and editing state.

## Left Section

| Indicator | Description |
|-----------|-------------|
| **Status** | Current action or tool name (e.g., "Ready", "Tool: Select") |
| **Selection** | Selected object count and dimensions |
| **Color Mode** | Document color mode (RGB/CMYK) |
| **Snap** | Snap to grid/guides status (highlighted when enabled) |
| **Artboard** | Name of the active artboard (only shown when an artboard is active) |

## Right Section

| Indicator | Description |
|-----------|-------------|
| **Cursor** | X, Y coordinates on canvas |
| **Zoom** | Current zoom percentage |
| **Elements** | Total element count |
| **Document Size** | Canvas dimensions (e.g., "800 × 600") |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + +` | Zoom in |
| `Ctrl + -` | Zoom out |
| `Ctrl + 0` | Fit to window |
| `Ctrl + 1` | Actual size (100%) |
