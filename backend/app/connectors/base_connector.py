
"""
Base Connector Class
Defines the interface for all device connectors
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseConnector(ABC):
    """
    Abstract base class for device connectors
    All device connectors must inherit from this class
    """
    
    def __init__(self, config: Dict[str, Any], mock_mode: bool = False):
        """
        Initialize connector
        
        Args:
            config: Device configuration dictionary
            mock_mode: Whether to use mock data instead of real API calls
        """
        self.config = config
        self.mock_mode = mock_mode
        self.device_name = config.get("name", "Unknown Device")
        logger.info(f"Initialized {self.__class__.__name__} (mock_mode={mock_mode})")
    
    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to the device
        
        Returns:
            Dictionary with:
                - success: bool
                - message: str
                - details: dict
        """
        pass
    
    @abstractmethod
    def collect_events(self, hours: int = 1, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Collect events from the device
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of events to collect
        
        Returns:
            List of event dictionaries
        """
        pass
    
    @abstractmethod
    def get_health(self) -> Dict[str, Any]:
        """
        Get device health status
        
        Returns:
            Dictionary with health information
        """
        pass
    
    def normalize_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw event to standard format
        Can be overridden by specific connectors
        
        Args:
            raw_event: Raw event from device
        
        Returns:
            Normalized event dictionary
        """
        return {
            "timestamp": raw_event.get("timestamp", datetime.utcnow().isoformat()),
            "event_type": raw_event.get("event_type", "unknown"),
            "severity": raw_event.get("severity", "info"),
            "source": self.__class__.__name__.replace("Connector", "").lower(),
            "raw_event": raw_event
        }
    
    def extract_severity(self, event: Dict[str, Any]) -> str:
        """
        Extract severity from event
        Can be overridden by specific connectors
        
        Returns:
            Severity level: critical, high, medium, low, info
        """
        severity = str(event.get("severity", "")).lower()
        
        if severity in ["critical", "5"]:
            return "critical"
        elif severity in ["high", "4", "error"]:
            return "high"
        elif severity in ["medium", "3", "warning"]:
            return "medium"
        elif severity in ["low", "2"]:
            return "low"
        else:
            return "info"
    
    def log_collection(self, event_count: int, status: str = "success"):
        """Log event collection activity"""
        logger.info(
            f"{self.__class__.__name__} collected {event_count} events - Status: {status}"
        )
