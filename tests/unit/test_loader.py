import pytest
from unittest.mock import patch, MagicMock
from src.core.loader import load_touchstone_file
from src.models.dataset import SParameterDataset

def test_load_touchstone_file_success():
    with patch("src.core.loader.rf.Network") as MockNetwork:
        mock_net = MagicMock()
        mock_net.number_of_ports = 2
        mock_net.f = [1, 2]
        MockNetwork.return_value = mock_net
        
        dataset = load_touchstone_file("/path/to/test.s2p")
        
        assert isinstance(dataset, SParameterDataset)
        assert dataset.filepath == "/path/to/test.s2p"
        # Verify skrf.Network was called with the path
        MockNetwork.assert_called_once_with("/path/to/test.s2p")

def test_load_touchstone_file_not_found():
    # skrf.Network raises FileNotFoundError if file missing (or OSError)
    with patch("src.core.loader.rf.Network") as MockNetwork:
        MockNetwork.side_effect = FileNotFoundError("File not found")
        
        with pytest.raises(FileNotFoundError):
            load_touchstone_file("missing.s2p")

def test_load_touchstone_file_invalid_format():
    # skrf might raise various errors for bad formats
    with patch("src.core.loader.rf.Network") as MockNetwork:
        MockNetwork.side_effect = Exception("Parse error")
        
        with pytest.raises(ValueError):
            load_touchstone_file("bad.s2p")
