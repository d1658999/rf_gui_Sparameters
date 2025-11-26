import skrf as rf
import os
from src.models.dataset import SParameterDataset

def load_touchstone_file(filepath: str) -> SParameterDataset:
    """
    Loads and parses a Touchstone file.
    
    Args:
        filepath: Absolute path to the .sXp file.
    
    Returns:
        SParameterDataset: Validated dataset object.
    
    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file format is invalid or parsing fails.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    try:
        # skrf.Network automatically parses Touchstone v1/v2 based on content
        network = rf.Network(filepath)
        
        # Validate basics?
        if network.number_of_ports == 0:
             # Sometimes empty files might load as 0 ports
             raise ValueError("Loaded network has 0 ports.")
             
        filename = os.path.basename(filepath)
        return SParameterDataset(network, filename, filepath)
        
    except (ValueError, OSError, Exception) as e:
        # skrf can raise generic Exceptions for bad parsing
        # Ensure we propagate FileNotFoundError if it wasn't caught by os.path.exists check
        # (e.g. race condition, or permissions)
        if isinstance(e, FileNotFoundError):
            raise e
        # Wrap other errors as ValueError for the UI to handle gracefully
        raise ValueError(f"Failed to parse Touchstone file: {str(e)}") from e
