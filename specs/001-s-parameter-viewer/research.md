# Research: S-Parameter Viewer

**Feature**: `001-s-parameter-viewer`
**Date**: 2025-11-26

## 1. GUI Framework Selection

**Decision**: Use **PyQt6**.

**Rationale**:
- **Requirement Match**: The spec requires a "Tabbed interface" and "Multiple open files". PyQt's `QTabWidget` provides this out-of-the-box.
- **Matplotlib Integration**: `matplotlib` has a robust `backend_qt5agg` (compatible with Qt6 via `backend_qtagg`) that allows embedding plots as native widgets (`FigureCanvasQTAgg`).
- **User Experience**: Provides a native look-and-feel on Linux (user's OS) and other platforms.
- **Constitution**: Fits "High Quality" principle better than Tkinter for complex data apps.

**Alternatives Considered**:
- **Tkinter**: Built-in to Python (Simpler dependency). Rejected because complex layouts (tabs + sidebars + resizeable plots) are more verbose to implement and look less professional.
- **PySide6**: Functionally identical to PyQt6 (Qt for Python). PyQt6 is chosen effectively arbitrarily as the standard; can swap to PySide6 if licensing requires (LGPL vs GPL), but for this internal tool/MVP, PyQt6 is fine.

## 2. Touchstone Parsing & Analysis

**Decision**: Use **scikit-rf (`skrf`)**.

**Rationale**:
- **Constitution**: "MVP & Simplicity" - Avoid writing a custom Touchstone parser.
- **Completeness**: Supports Touchstone v1.0 and v2.0 natively.
- **Features**: Built-in support for:
    - Reading/Writing `.sXp` files.
    - Plotting Magnitude (dB), Phase (deg), and Smith Charts.
    - Mixed-mode conversion (if needed for v2.0).

**Alternatives Considered**:
- **Custom Parser**: Rejected. High risk of errors with complex Touchstone formats (comments, different number formats, formatting). Violates "Don't overdesign" (re-inventing the wheel).
- **Pandas**: Can read CSV-like structures, but Touchstone headers and complex number formats require significant custom pre-processing.

## 3. Plotting Library

**Decision**: Use **matplotlib**.

**Rationale**:
- **Spec Clarification**: Explicitly requested.
- **Integration**: `scikit-rf` has `plot_s_db()`, `plot_s_smith()`, etc., which output directly to matplotlib axes.
- **Interactivity**: Supports "pick events" for the "Inspect Data Points" requirement (User Story 3).

**Alternatives Considered**:
- **PyQtGraph**: Faster, but requires mapping `scikit-rf` data manually to its format and implementing Smith Charts from scratch.
