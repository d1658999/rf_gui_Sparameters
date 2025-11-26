# Data Model: S-Parameter Viewer

**Feature**: `001-s-parameter-viewer`

## Entities

### SParameterDataset
Represents the loaded RF Network data from a Touchstone file.
*Wraps `skrf.Network`*

| Field | Type | Description |
|-------|------|-------------|
| `network` | `skrf.Network` | The underlying scikit-rf network object. |
| `filename` | `str` | Name of the loaded file (e.g., "filter.s2p"). |
| `filepath` | `str` | Full path to source file. |
| `port_count` | `int` | Number of ports (derived from network). |
| `frequencies` | `List[float]` | Frequency points in Hz (derived from network). |
| `parameter_names` | `List[str]` | List of S-parameters available (e.g., ["S11", "S21", ...]). |

### ViewportConfig
Represents the state of a single tab's visualization.

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `active_plot_type` | `Enum` | `MAGNITUDE_DB`, `PHASE_DEG`, `SMITH` | `MAGNITUDE_DB` |
| `visible_traces` | `Set[str]` | Set of S-parameter names currently visible (e.g., {"S11"}). | All parameters |
| `freq_min` | `float` | Minimum frequency for x-axis (Hz). | `network.f[0]` |
| `freq_max` | `float` | Maximum frequency for x-axis (Hz). | `network.f[-1]` |

## State Management

**Application State** (Runtime only):
- `open_datasets`: `List[SParameterDataset]`
- `active_tab_index`: `int`

## Relationships

- One `Application` holds Many `SParameterDataset` (via tabs).
- One `SParameterDataset` is associated with One `ViewportConfig` (state per tab).
