
"""
Palo Alto NGFW Connector
Connects to Palo Alto firewalls and collects security events
"""
from typing import Dict, Any, List
import logging
from .base_connector import BaseConnector
from .mock_data import MockDataGenerator
from ..integrations.paloalto_client import PaloAltoClient

logger = logging.getLogger(__name__)


class PaloAltoConnector(BaseConnector):
    """Connector for Palo Alto Networks firewalls"""
    
    def __init__(self, config: Dict[str, Any], mock_mode: bool = False):
        super().__init__(config, mock_mode)
        
        if not mock_mode:
            try:
                self.client = PaloAltoClient(config)
            except Exception as e:
                logger.error(f"Failed to initialize Palo Alto client: {e}")
                self.client = None
        else:
            self.client = None
            logger.info("Palo Alto connector initialized in mock mode")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Palo Alto firewall"""
        if self.mock_mode:
            return {
                "success": True,
                "message": "Successfully connected to Palo Alto (Mock Mode)",
                "details": {
                    "device_info": {
                        "hostname": "pa-firewall-mock",
                        "model": "PA-VM",
                        "sw_version": "10.2.3",
                        "serial": "MOCK123456789"
                    },
                    "api_version": "PAN-OS REST API (Mock)",
                    "latency_ms": 50,
                    "mock_mode": True
                }
            }
        
        if not self.client:
            return {
                "success": False,
                "message": "Palo Alto client not initialized",
                "details": {"error": "Configuration error"}
            }
        
        return self.client.test_connection()
    
    def collect_events(self, hours: int = 1, limit: int = 100) -> List[Dict[str, Any]]:
        """Collect events from Palo Alto firewall"""
        if self.mock_mode:
            logger.info(f"Generating {limit} mock Palo Alto events")
            raw_events = MockDataGenerator.generate_paloalto_events(
                count=limit,
                hours_back=hours
            )
            self.log_collection(len(raw_events))
            return [self.normalize_paloalto_event(e) for e in raw_events]
        
        if not self.client:
            logger.error("Palo Alto client not initialized")
            return []
        
        try:
            # Collect threat logs
            threat_logs = self.client.get_threat_logs(
                time_range=f"last-{hours}-hrs",
                limit=limit
            )
            
            normalized_events = [
                self.normalize_paloalto_event(log) for log in threat_logs
            ]
            
            self.log_collection(len(normalized_events))
            return normalized_events
            
        except Exception as e:
            logger.error(f"Error collecting Palo Alto events: {e}", exc_info=True)
            return []
    
    def get_health(self) -> Dict[str, Any]:
        """Get Palo Alto firewall health"""
        if self.mock_mode:
            return {
                "status": "healthy",
                "uptime": "45 days, 12:34:56",
                "version": "10.2.3",
                "model": "PA-VM",
                "mock_mode": True
            }
        
        if not self.client:
            return {"status": "error", "error": "Client not initialized"}
        
        return self.client.get_device_health()
    
    def normalize_paloalto_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Palo Alto event to standard format"""
        event_type = "network"
        if raw_event.get("type") == "THREAT":
            event_type = "threat"
        
        severity = self.extract_severity(raw_event)
        
        return {
            "timestamp": raw_event.get("receive_time", raw_event.get("time_generated")),
            "event_type": event_type,
            "severity": severity,
            "source": "paloalto",
            "source_ip": raw_event.get("src"),
            "dest_ip": raw_event.get("dst"),
            "user": raw_event.get("srcuser"),
            "action": raw_event.get("action"),
            "threat_name": raw_event.get("threatid"),
            "application": raw_event.get("app"),
            "rule": raw_event.get("rule"),
            "raw_event": raw_event
        }
