# S-Parameter Viewer

A Python desktop application for visualizing Touchstone (.snp) files (v1.0 and v2.0).
Built with **PyQt6**, **scikit-rf**, and **matplotlib**.

## Features

- **Load Touchstone Files**: Supports .s1p, .s2p, .s3p, .s4p, etc.
- **Tabbed Interface**: View multiple files simultaneously.
- **Visualization**:
  - Magnitude (dB)
  - Phase (Degrees)
  - Smith Chart
- **Analysis**:
  - Toggle trace visibility.
  - Inspect data points (Click on trace).
  - Adjust frequency range (Min/Max).

## Installation

1.  **Install Python 3.10+**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application**:
    ```bash
    python src/app.py
    ```
2.  **Open a file**: Use `File > Open` or `Ctrl+O`.
3.  **Interact**:
    - Switch plot types using the buttons above the plot.
    - Toggle traces using the right-side panel.
    - Set frequency range in the right-side panel.
    - Click on any line to see exact values.

## Development

### Running Tests

```bash
pytest tests/
```

### Project Structure

- `src/core`: RF data loading and logic.
- `src/gui`: PyQt6 widgets and windows.
- `src/models`: Data models (Dataset, Config).
- `tests/`: Unit tests.