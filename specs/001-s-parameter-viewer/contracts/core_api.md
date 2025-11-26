# Core API Contracts

**Feature**: `001-s-parameter-viewer`
**Type**: Internal Python API (GUI -> Core)

## Module: `core.loader`

### `load_touchstone_file`

Loads and parses a Touchstone file.

```python
def load_touchstone_file(filepath: str) -> SParameterDataset:
    """
    Args:
        filepath: Absolute path to the .sXp file.
    
    Returns:
        SParameterDataset: Validated dataset object.
    
    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file format is invalid or parsing fails.
    """
```

## Module: `models.dataset` (SParameterDataset Methods)

### `get_magnitude_db`

Get magnitude data for plotting.

```python
def get_magnitude_db(self, parameter: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Args:
        parameter: S-parameter name (e.g., "S11").
        
    Returns:
        (frequencies, magnitude_db): Tuple of numpy arrays.
    """
```

### `get_phase_deg`

Get phase data for plotting.

```python
def get_phase_deg(self, parameter: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        (frequencies, phase_deg): Tuple of numpy arrays (phase unwrapped if needed, or raw).
    """
```

### `get_complex_data`

Get complex data for Smith Chart.

```python
def get_complex_data(self, parameter: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        (frequencies, complex_s): Array of complex numbers for Smith chart plotting.
    """
```
