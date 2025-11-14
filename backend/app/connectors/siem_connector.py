
"""
Generic SIEM Connector
Connects to SIEM platforms (Splunk, Elastic) and collects security events
"""
from typing import Dict, Any, List
import logging
from .base_connector import BaseConnector
from .mock_data import MockDataGenerator
from ..integrations.siem_client import SIEMClient

logger = logging.getLogger(__name__)


class SIEMConnector(BaseConnector):
    """Connector for SIEM platforms (Splunk, Elasticsearch, etc.)"""
    
    def __init__(self, config: Dict[str, Any], mock_mode: bool = False):
        super().__init__(config, mock_mode)
        
        if not mock_mode:
            try:
                self.client = SIEMClient(config)
            except Exception as e:
                logger.error(f"Failed to initialize SIEM client: {e}")
                self.client = None
        else:
            self.client = None
            logger.info("SIEM connector initialized in mock mode")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to SIEM"""
        if self.mock_mode:
            siem_type = self.config.get("siem_type", "splunk")
            return {
                "success": True,
                "message": f"Successfully connected to {siem_type.title()} (Mock Mode)",
                "details": {
                    "server_info": {
                        "name": f"{siem_type}-mock",
                        "version": "9.0.0" if siem_type == "splunk" else "8.10.0",
                        "build": "mock-build-123"
                    },
                    "api_version": f"{siem_type.title()} REST API (Mock)",
                    "latency_ms": 55,
                    "mock_mode": True
                }
            }
        
        if not self.client:
            return {
                "success": False,
                "message": "SIEM client not initialized",
                "details": {"error": "Configuration error"}
            }
        
        return self.client.test_connection()
    
    def collect_events(self, hours: int = 1, limit: int = 100) -> List[Dict[str, Any]]:
        """Collect events from SIEM"""
        if self.mock_mode:
            logger.info(f"Generating {limit} mock SIEM events")
            raw_events = MockDataGenerator.generate_siem_events(
                count=limit,
                hours_back=hours
            )
            self.log_collection(len(raw_events))
            return [self.normalize_siem_event(e) for e in raw_events]
        
        if not self.client:
            logger.error("SIEM client not initialized")
            return []
        
        try:
            # Generic search query for security events
            query = "security OR threat OR alert"
            
            events = self.client.search_events(
                query=query,
                time_range=f"{hours}h",
                limit=limit
            )
            
            normalized_events = [
                self.normalize_siem_event(event) for event in events
            ]
            
            self.log_collection(len(normalized_events))
            return normalized_events
            
        except Exception as e:
            logger.error(f"Error collecting SIEM events: {e}", exc_info=True)
            return []
    
    def get_health(self) -> Dict[str, Any]:
        """Get SIEM health"""
        if self.mock_mode:
            siem_type = self.config.get("siem_type", "splunk")
            return {
                "status": "healthy",
                "siem_type": siem_type,
                "response_time_ms": 45,
                "mock_mode": True
            }
        
        if not self.client:
            return {"status": "error", "error": "Client not initialized"}
        
        return self.client.get_device_health()
    
    def normalize_siem_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize SIEM event to standard format"""
        severity = self.extract_severity(raw_event)
        
        return {
            "timestamp": raw_event.get("@timestamp", raw_event.get("timestamp")),
            "event_type": raw_event.get("event_type", "security_event"),
            "severity": severity,
            "source": "siem",
            "host": raw_event.get("host"),
            "user": raw_event.get("user"),
            "source_ip": raw_event.get("source_ip"),
            "message": raw_event.get("message"),
            "tags": raw_event.get("tags", []),
            "raw_event": raw_event
        }
