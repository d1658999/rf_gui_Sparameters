from dataclasses import dataclass, field
from enum import Enum
from typing import Set

class PlotType(Enum):
    MAGNITUDE_DB = "MAGNITUDE_DB"
    PHASE_DEG = "PHASE_DEG"
    SMITH = "SMITH"

@dataclass
class ViewportConfig:
    active_plot_type: PlotType = PlotType.MAGNITUDE_DB
    visible_traces: Set[str] = field(default_factory=set)
    freq_min: float = 0.0
    freq_max: float = 0.0
