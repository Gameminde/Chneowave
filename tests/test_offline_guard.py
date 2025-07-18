
import pytest
import socket
from unittest.mock import patch
from hrneowave.offline_guard import check_offline_mode

def test_offline_mode_detection():
    """Test la détection du mode offline"""
    with patch.dict('os.environ', {'CHNW_MODE': 'offline'}):
        assert check_offline_mode() is True
    
    with patch.dict('os.environ', {'CHNW_MODE': 'online'}):
        assert check_offline_mode() is False

def test_socket_guard():
    """Test le gardien socket"""
    with patch.dict('os.environ', {'CHNW_MODE': 'offline'}):
        with pytest.raises(RuntimeError, match="Network disabled in offline mode"):
            socket.create_connection(('google.com', 80))
