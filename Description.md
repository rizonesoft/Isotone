# Project Photon (Codename)

**Project Photon** is the internal development codename for the **Rizonesoft Graphics Suite**.

This repository hosts the source code for a family of high-performance, standalone creative applications. While these tools share a unified architectural core (`Photon.Core`) for rendering, resource management, and plugin support, they are designed to be distributed and installed as independent products.

## The Application Family

### 1. Rizonesoft Imago
* **Type:** Standalone Raster Editor (Photoshop alternative)
* **Role:** Creation & Manipulation
* **Focus:** Digital painting, photo retouching, layer composition, and pixel-level editing.
* **Target Formats:** `.psd`, `.png`, `.tiff`, `.jpg`

### 2. Rizonesoft Nodus
* **Type:** Standalone Vector Editor (Illustrator alternative)
* **Role:** Structure & Design
* **Focus:** Precision illustration, typography, logo design, and scalable vector graphics.
* **Target Formats:** `.svg`, `.eps`, `.ai`, `.pdf`

### 3. Rizonesoft Lumen
* **Type:** Digital Darkroom & Asset Manager (Lightroom alternative)
* **Role:** Development & Organization
* **Focus:** RAW image processing, non-destructive editing, batch adjustments, and library management.
* **Workflow:** Acts as the bridge between the camera and **Imago**.

---

## Technical Architecture

The solution follows a **"Develop Together, Distribute Separately"** philosophy.

### The Photon Core (`src/Photon.Core`)
All three applications are built upon a shared .NET class library that strictly enforces logic separation from the UI. The Core handles:
* **Rendering Pipeline:** High-performance 2D drawing primitives.
* **File I/O:** Unified handling of complex file formats.
* **Plugin System:** A common interface allowing extensions (filters, brushes) to potentially work across apps.
* **Color Science:** Shared color management to ensure visual consistency between Imago, Nodus, and Lumen.

### Deployment Strategy
* **Monorepo:** Development occurs in a single Visual Studio Solution (`ProjectPhoton.sln`) for rapid refactoring and unified debugging.
* **Isolation:** Each application is compiled into a separate executable directory with its own copy of the core dependencies. There are no shared installation folders, ensuring that an update to *Rizonesoft Imago* never breaks an installed version of *Rizonesoft Nodus*.

## Development Goals
1.  **Performance:** Prioritize lightweight execution and startup speed over legacy feature bloat.
2.  **Interoperability:** Seamless "Edit In" workflows (e.g., sending a RAW file from *Lumen* to *Imago*).
3.  **Extensibility:** A plugin-first architecture allowing the community to extend toolsets.