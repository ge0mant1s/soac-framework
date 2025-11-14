
"""
Microsoft Entra ID Connector
Connects to Microsoft Entra ID and collects authentication events
"""
from typing import Dict, Any, List
import logging
from .base_connector import BaseConnector
from .mock_data import MockDataGenerator
from ..integrations.entraid_client import EntraIDClient

logger = logging.getLogger(__name__)


class EntraIDConnector(BaseConnector):
    """Connector for Microsoft Entra ID (Azure AD)"""
    
    def __init__(self, config: Dict[str, Any], mock_mode: bool = False):
        super().__init__(config, mock_mode)
        
        if not mock_mode:
            try:
                self.client = EntraIDClient(config)
            except Exception as e:
                logger.error(f"Failed to initialize Entra ID client: {e}")
                self.client = None
        else:
            self.client = None
            logger.info("Entra ID connector initialized in mock mode")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Entra ID"""
        if self.mock_mode:
            return {
                "success": True,
                "message": "Successfully connected to Microsoft Entra ID (Mock Mode)",
                "details": {
                    "organization": {
                        "display_name": "Straumann Group Mock",
                        "tenant_id": "mock-tenant-id-12345",
                        "verified_domains": 3
                    },
                    "api_version": "Microsoft Graph v1.0 (Mock)",
                    "latency_ms": 45,
                    "mock_mode": True
                }
            }
        
        if not self.client:
            return {
                "success": False,
                "message": "Entra ID client not initialized",
                "details": {"error": "Configuration error"}
            }
        
        return self.client.test_connection()
    
    def collect_events(self, hours: int = 1, limit: int = 100) -> List[Dict[str, Any]]:
        """Collect authentication events from Entra ID"""
        if self.mock_mode:
            logger.info(f"Generating {limit} mock Entra ID events")
            raw_events = MockDataGenerator.generate_entraid_events(
                count=limit,
                hours_back=hours
            )
            self.log_collection(len(raw_events))
            return [self.normalize_entraid_event(e) for e in raw_events]
        
        if not self.client:
            logger.error("Entra ID client not initialized")
            return []
        
        try:
            # Collect sign-in logs
            sign_in_logs = self.client.get_sign_in_logs(
                hours=hours,
                limit=limit
            )
            
            normalized_events = [
                self.normalize_entraid_event(log) for log in sign_in_logs
            ]
            
            self.log_collection(len(normalized_events))
            return normalized_events
            
        except Exception as e:
            logger.error(f"Error collecting Entra ID events: {e}", exc_info=True)
            return []
    
    def get_health(self) -> Dict[str, Any]:
        """Get Entra ID service health"""
        if self.mock_mode:
            return {
                "status": "healthy",
                "api_version": "Microsoft Graph v1.0",
                "token_valid": True,
                "mock_mode": True
            }
        
        if not self.client:
            return {"status": "error", "error": "Client not initialized"}
        
        return self.client.get_device_health()
    
    def normalize_entraid_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Entra ID event to standard format"""
        # Determine if success or failure
        status = raw_event.get("status", {})
        error_code = status.get("errorCode", 0)
        is_success = error_code == 0
        
        # Extract severity based on risk and outcome
        severity = "info"
        risk_level = raw_event.get("riskLevelDuringSignIn", "none")
        if risk_level in ["high", "medium"]:
            severity = "high" if risk_level == "high" else "medium"
        elif not is_success:
            severity = "medium"
        
        # Extract location
        location = raw_event.get("location", {})
        country = location.get("countryOrRegion", "Unknown")
        
        return {
            "timestamp": raw_event.get("createdDateTime"),
            "event_type": "authentication",
            "severity": severity,
            "source": "entraid",
            "user": raw_event.get("userPrincipalName"),
            "source_ip": raw_event.get("ipAddress"),
            "country": country,
            "application": raw_event.get("appDisplayName"),
            "success": is_success,
            "risk_level": risk_level,
            "device_os": raw_event.get("deviceDetail", {}).get("operatingSystem"),
            "client_app": raw_event.get("clientAppUsed"),
            "conditional_access_status": raw_event.get("conditionalAccessStatus"),
            "raw_event": raw_event
        }
