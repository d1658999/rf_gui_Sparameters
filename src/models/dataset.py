import numpy as np
from typing import List, Tuple, Dict, Any

class SParameterDataset:
    def __init__(self, network, filename: str, filepath: str):
        """
        Initialize with a scikit-rf Network object.
        
        Args:
            network: skrf.Network object
            filename: Name of the file
            filepath: Full path to the file
        """
        self.network = network
        self.filename = filename
        self.filepath = filepath
        
    @property
    def frequencies(self) -> np.ndarray:
        """Frequency points in Hz."""
        return self.network.f
        
    @property
    def port_count(self) -> int:
        """Number of ports in the network."""
        return self.network.number_of_ports
        
    @property
    def parameter_names(self) -> List[str]:
        """
        Generate list of S-parameter names (e.g., S11, S21).
        Ordering: S11, S12, ... S1N, S21 ...
        """
        names = []
        n = self.port_count
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                names.append(f"S{i}{j}")
        return names

    def _get_indices(self, parameter: str) -> Tuple[int, int]:
        """Parse S-parameter string 'Sij' to indices (i-1, j-1)."""
        if not parameter.startswith("S") or len(parameter) < 3:
             raise ValueError(f"Invalid parameter name: {parameter}")
        
        try:
            # Handle potentially multi-digit ports? S11 is simple. S1010?
            # For MVP, assume single digit ports or standard parsing.
            # skrf usually handles up to 9 ports easily with naming.
            # Let's parse simple "S{i}{j}"
            # For >9 ports, naming gets ambiguous S1011 (10,11) or (1,011)?
            # Typically S_10_11 for large ports. 
            # Spec says ".s4p" so max 4 ports. Single digit is safe.
            row = int(parameter[1]) - 1
            col = int(parameter[2]) - 1
            
            if row < 0 or row >= self.port_count or col < 0 or col >= self.port_count:
                 raise ValueError(f"Port index out of range for {parameter}")
            return row, col
        except ValueError:
             raise ValueError(f"Could not parse indices from {parameter}")

    def get_complex_data(self, parameter: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get frequency and complex S-parameter data."""
        row, col = self._get_indices(parameter)
        # network.s shape is (n_freq, n_ports, n_ports)
        # access [:, row, col]
        s_data = self.network.s[:, row, col]
        return self.frequencies, s_data

    def get_magnitude_db(self, parameter: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get frequency and Magnitude (dB)."""
        freq, s = self.get_complex_data(parameter)
        # Avoid log10(0)
        s_abs = np.abs(s)
        # Small epsilon to prevent -inf
        s_abs[s_abs == 0] = 1e-12 
        mag_db = 20 * np.log10(s_abs)
        return freq, mag_db

    def get_phase_deg(self, parameter: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get frequency and Phase (degrees)."""
        freq, s = self.get_complex_data(parameter)
        phase_rad = np.angle(s)
        phase_deg = np.degrees(phase_rad)
        return freq, phase_deg

    def find_nearest_data_point(self, parameter: str, target_freq: float) -> Dict[str, Any]:
        """
        Find the nearest data point to the target frequency.
        Returns dict with freq, mag_db, phase_deg, complex.
        """
        idx = (np.abs(self.frequencies - target_freq)).argmin()
        actual_freq = self.frequencies[idx]
        
        freqs, s_complex = self.get_complex_data(parameter)
        val = s_complex[idx]
        
        mag_db = 20 * np.log10(np.abs(val) if np.abs(val) > 0 else 1e-12)
        phase_deg = np.degrees(np.angle(val))
        
        return {
            "frequency": actual_freq,
            "magnitude_db": mag_db,
            "phase_deg": phase_deg,
            "complex": val
        }