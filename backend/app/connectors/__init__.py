
"""
Device Connectors Package
Provides connector classes for device integrations
"""
from .base_connector import BaseConnector
from .paloalto_connector import PaloAltoConnector
from .entraid_connector import EntraIDConnector
from .siem_connector import SIEMConnector

__all__ = [
    "BaseConnector",
    "PaloAltoConnector",
    "EntraIDConnector",
    "SIEMConnector",
]


def get_connector(device_type: str, config: dict, mock_mode: bool = False):
    """
    Factory function to get the appropriate connector
    
    Args:
        device_type: Type of device (paloalto, entraid, siem)
        config: Device configuration dictionary
        mock_mode: Whether to use mock data (default: False)
    
    Returns:
        Connector instance
    """
    connectors = {
        "paloalto": PaloAltoConnector,
        "entraid": EntraIDConnector,
        "siem": SIEMConnector,
    }
    
    connector_class = connectors.get(device_type.lower())
    if not connector_class:
        raise ValueError(f"Unknown device type: {device_type}")
    
    return connector_class(config, mock_mode=mock_mode)
