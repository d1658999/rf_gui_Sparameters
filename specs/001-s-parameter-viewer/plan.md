# Implementation Plan: S-Parameter Viewer

**Branch**: `001-s-parameter-viewer` | **Date**: 2025-11-26 | **Spec**: [specs/001-s-parameter-viewer/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-s-parameter-viewer/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The "S-Parameter Viewer" is a desktop application designed for RF engineers to visualize Touchstone files (.snp). It enables users to load multiple files (v1.0 and v2.0) in tabs, view Magnitude/Phase/Smith Charts, toggle trace visibility, and inspect data points. The technical approach leverages `scikit-rf` for parsing and network analysis, `matplotlib` for plotting, and `PyQt6` for the application framework.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `scikit-rf` (RF logic), `matplotlib` (Plotting), `PyQt6` (GUI Framework)
**Storage**: N/A (Local file read-only)
**Testing**: `pytest` (Unit), `pytest-qt` (GUI integration)
**Target Platform**: Desktop (Cross-platform Python)
**Project Type**: Desktop GUI
**Performance Goals**: Load 1000-pt file < 1s, Plot update < 100ms
**Constraints**: Touchstone v2.0 support required.
**Scale/Scope**: Multi-file support (Tabbed interface).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **High Quality & Testability**: `pytest` and `pytest-qt` configured. Logic separated from UI.
- [x] **MVP & Simplicity**: Using established libraries (`skrf`, `qt`, `mpl`) to avoid custom implementation.
- [x] **Pythonic Standards**: Adhering to PEP 8.

## Project Structure

### Documentation (this feature)

```text
specs/001-s-parameter-viewer/
├── plan.md              # This file
├── research.md          # Phase 0 output (PyQt6 selection)
├── data-model.md        # Phase 1 output (Dataset entities)
├── quickstart.md        # Phase 1 output (Usage guide)
├── contracts/           # Phase 1 output (Core API)
└── tasks.md             # Phase 2 output (Pending)
```

### Source Code (repository root)

```text
src/
├── app.py               # Entry point
├── core/
│   ├── loader.py        # File I/O and parsing (scikit-rf wrapper)
│   └── analyzer.py      # Data processing
├── gui/
│   ├── main_window.py   # Main application shell (TabWidget)
│   ├── plot_widget.py   # Matplotlib embedding
│   ├── control_panel.py # Checkboxes and inputs
│   └── tabs.py          # Tab management
└── models/
    ├── dataset.py       # SParameterDataset
    └── view_config.py   # ViewportConfig

tests/
├── unit/
│   ├── test_loader.py
│   └── test_models.py
└── integration/
    └── test_gui_flows.py
```

**Structure Decision**: Option 1 (Single Project) - Desktop GUI Application Structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| GUI Framework (`PyQt6`) | Required for "Tabs", "Multiple Files", and "Control Panel" layout. | `matplotlib` native widgets are too limited for the specified UX (Multi-tab app). |
