import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from src.models.dataset import SParameterDataset

@pytest.fixture
def mock_network():
    """Create a mock skrf.Network object."""
    mock_net = MagicMock()
    mock_net.name = "test_network"
    mock_net.filename = "test.s2p"
    mock_net.f = np.array([1e9, 2e9, 3e9])  # 1, 2, 3 GHz
    # S-params: 3 freq points, 2x2 matrix
    # Shape: (3, 2, 2)
    # Let's make simple data: S11=1, S21=0.5, S12=0.5, S22=1
    # complex values
    s_data = np.zeros((3, 2, 2), dtype=complex)
    s_data[:, 0, 0] = 1.0 + 0j  # S11
    s_data[:, 1, 0] = 0.5 + 0.5j # S21
    s_data[:, 0, 1] = 0.5 - 0.5j # S12
    s_data[:, 1, 1] = 0.1 + 0j   # S22
    
    mock_net.s = s_data
    mock_net.number_of_ports = 2
    return mock_net

def test_dataset_initialization(mock_network):
    dataset = SParameterDataset(mock_network, "test.s2p", "/path/to/test.s2p")
    
    assert dataset.filename == "test.s2p"
    assert dataset.filepath == "/path/to/test.s2p"
    assert dataset.port_count == 2
    np.testing.assert_array_equal(dataset.frequencies, mock_network.f)
    assert "S11" in dataset.parameter_names
    assert "S21" in dataset.parameter_names
    assert len(dataset.parameter_names) == 4

def test_get_magnitude_db(mock_network):
    dataset = SParameterDataset(mock_network, "test.s2p", "/path/to/test.s2p")
    
    freq, mag = dataset.get_magnitude_db("S11")
    # S11 is 1.0, 20*log10(1) = 0 dB
    np.testing.assert_array_almost_equal(mag, np.zeros(3))
    
    freq, mag = dataset.get_magnitude_db("S21")
    # S21 is 0.5+0.5j -> abs = sqrt(0.5) approx 0.707
    # 20*log10(0.707) approx -3.01 dB
    expected = 20 * np.log10(np.abs(0.5 + 0.5j))
    assert mag[0] == pytest.approx(expected)

def test_get_phase_deg(mock_network):
    dataset = SParameterDataset(mock_network, "test.s2p", "/path/to/test.s2p")
    
    freq, phase = dataset.get_phase_deg("S11")
    # S11 is 1+0j, phase 0
    assert phase[0] == 0
    
    freq, phase = dataset.get_phase_deg("S21")
    # S21 is 0.5+0.5j, phase 45 deg
    assert phase[0] == 45.0

def test_get_complex_data(mock_network):
    dataset = SParameterDataset(mock_network, "test.s2p", "/path/to/test.s2p")
    
    freq, complex_data = dataset.get_complex_data("S21")
    assert complex_data[0] == 0.5 + 0.5j

def test_invalid_parameter_name(mock_network):
    dataset = SParameterDataset(mock_network, "test.s2p", "/path/to/test.s2p")
    with pytest.raises(ValueError):
        dataset.get_magnitude_db("S99")
