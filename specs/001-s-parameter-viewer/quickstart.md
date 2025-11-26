# Quickstart: S-Parameter Viewer

**Feature**: `001-s-parameter-viewer`

## Prerequisites

- Python 3.10+ installed.
- `pip` installed.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Core dependencies: `scikit-rf`, `matplotlib`, `PyQt6`, `numpy`)*

2.  **Run the Application**:
    ```bash
    python src/app.py
    ```

## Usage Guide

1.  **Load File**:
    - Click "File > Open" or use the "Load .snp" button.
    - Select a `.s1p`, `.s2p`, etc. file.
    - A new tab will appear with the file name.

2.  **View Control**:
    - **Tabs**: Click "Magnitude", "Phase", or "Smith" at the top of the plot area to switch views.
    - **Traces**: Use the checkboxes on the right panel to show/hide "S11", "S21", etc.
    - **Zoom**: Use the "Freq Min" and "Freq Max" inputs to set the range.

3.  **Inspect Data**:
    - Click anywhere on a trace line.
    - A marker annotation will appear showing `Freq: X GHz, Mag: Y dB`.

## Troubleshooting

- **"Invalid File" error**: Ensure the file follows Touchstone v1.0 or v2.0 specification.
- **Plot not updating**: Try resizing the window to force a redraw (should not be needed but useful for debugging).
