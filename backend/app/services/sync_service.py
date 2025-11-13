
"""
Device synchronization service
Handles fetching rules and data from security devices
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Device, Rule
from ..integrations import PaloAltoClient, EntraIDClient, SIEMClient

logger = logging.getLogger(__name__)


class SyncService:
    """
    Service for synchronizing configuration and rules from security devices
    """
    
    @staticmethod
    def sync_device(device: Device, db: Session) -> Dict[str, Any]:
        """
        Synchronize rules from a device
        
        Args:
            device: Device model instance
            db: Database session
            
        Returns:
            Dictionary with sync results
        """
        try:
            logger.info(f"Starting sync for device {device.name} (type: {device.type})")
            
            # Get appropriate client based on device type
            if device.type == "paloalto":
                client = PaloAltoClient(device.config)
                rules = client.get_security_rules()
                normalized_rules = SyncService._normalize_paloalto_rules(rules, device.id)
            elif device.type == "entraid":
                client = EntraIDClient(device.config)
                # For Entra ID, we'll fetch sign-in logs instead of rules
                # In a full implementation, you'd define detection rules from policies
                logs = client.get_sign_in_logs(hours=1, limit=10)
                normalized_rules = []
                logger.info(f"Fetched {len(logs)} sign-in logs (rules sync not applicable for Entra ID)")
            elif device.type == "siem":
                # SIEM rules would need to be fetched based on the SIEM type
                # This is a simplified example
                normalized_rules = []
                logger.info("SIEM rule sync not fully implemented yet")
            else:
                return {
                    "success": False,
                    "message": f"Unsupported device type: {device.type}",
                    "rules_synced": 0,
                    "rules_updated": 0,
                    "rules_created": 0
                }
            
            # Sync rules to database
            rules_created = 0
            rules_updated = 0
            
            for rule_data in normalized_rules:
                existing_rule = db.query(Rule).filter(Rule.id == rule_data["id"]).first()
                
                if existing_rule:
                    # Update existing rule
                    for key, value in rule_data.items():
                        if key != "id":
                            setattr(existing_rule, key, value)
                    existing_rule.updated_at = datetime.utcnow()
                    rules_updated += 1
                else:
                    # Create new rule
                    new_rule = Rule(**rule_data)
                    db.add(new_rule)
                    rules_created += 1
            
            # Update device sync timestamp
            device.last_sync = datetime.utcnow()
            device.connection_status = "connected"
            
            db.commit()
            
            total_synced = rules_created + rules_updated
            
            logger.info(f"Sync completed for {device.name}: {total_synced} rules ({rules_created} created, {rules_updated} updated)")
            
            return {
                "success": True,
                "message": f"Successfully synced {total_synced} rules",
                "rules_synced": total_synced,
                "rules_created": rules_created,
                "rules_updated": rules_updated,
                "last_sync": device.last_sync.isoformat() if device.last_sync else None
            }
            
        except Exception as e:
            logger.error(f"Sync failed for device {device.name}: {e}", exc_info=True)
            device.connection_status = "error"
            db.commit()
            
            return {
                "success": False,
                "message": f"Sync failed: {str(e)}",
                "rules_synced": 0,
                "rules_created": 0,
                "rules_updated": 0,
                "error": str(e)
            }
    
    @staticmethod
    def _normalize_paloalto_rules(rules: List[Dict[str, Any]], device_id: str) -> List[Dict[str, Any]]:
        """
        Normalize Palo Alto security rules to SOaC rule format
        
        Args:
            rules: List of Palo Alto security rules
            device_id: Device UUID
            
        Returns:
            List of normalized rules
        """
        normalized = []
        
        for idx, rule in enumerate(rules, start=1):
            try:
                rule_id = f"PALOALTO-{idx:03d}"
                
                # Create query representation
                query = f"""
Source Zones: {', '.join(rule.get('source_zones', []))}
Destination Zones: {', '.join(rule.get('dest_zones', []))}
Source Addresses: {', '.join(rule.get('source_addresses', []))}
Destination Addresses: {', '.join(rule.get('dest_addresses', []))}
Applications: {', '.join(rule.get('applications', []))}
Services: {', '.join(rule.get('services', []))}
Action: {rule.get('action', 'allow')}
                """.strip()
                
                normalized_rule = {
                    "id": rule_id,
                    "device_id": device_id,
                    "name": rule.get("name", f"PA Rule {idx}"),
                    "description": rule.get("description", ""),
                    "severity": SyncService._map_pa_severity(rule.get("action", "allow")),
                    "category": "Network Security",
                    "query": query,
                    "enabled": not rule.get("disabled", False),
                    "status": "active" if not rule.get("disabled", False) else "disabled",
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                normalized.append(normalized_rule)
                
            except Exception as e:
                logger.error(f"Error normalizing Palo Alto rule: {e}")
                continue
        
        return normalized
    
    @staticmethod
    def _map_pa_severity(action: str) -> str:
        """Map Palo Alto action to severity level"""
        action_severity_map = {
            "deny": "High",
            "drop": "High",
            "reset-client": "Medium",
            "reset-server": "Medium",
            "reset-both": "Medium",
            "allow": "Low"
        }
        return action_severity_map.get(action.lower(), "Medium")
    
    @staticmethod
    def get_device_health(device: Device) -> Dict[str, Any]:
        """
        Get health metrics for a device
        
        Args:
            device: Device model instance
            
        Returns:
            Dictionary with health information
        """
        try:
            if device.type == "paloalto":
                client = PaloAltoClient(device.config)
            elif device.type == "entraid":
                client = EntraIDClient(device.config)
            elif device.type == "siem":
                client = SIEMClient(device.config)
            else:
                return {
                    "success": False,
                    "message": f"Unsupported device type: {device.type}",
                    "health": {}
                }
            
            health_data = client.get_device_health()
            
            return {
                "success": True,
                "message": "Health check completed",
                "health": health_data
            }
            
        except Exception as e:
            logger.error(f"Health check failed for device {device.name}: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Health check failed: {str(e)}",
                "health": {"status": "error", "error": str(e)}
            }
    
    @staticmethod
    def test_device_connection(device_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test connection to a device
        
        Args:
            device_type: Type of device (paloalto, entraid, siem)
            config: Device configuration
            
        Returns:
            Dictionary with connection test results
        """
        try:
            if device_type == "paloalto":
                client = PaloAltoClient(config)
            elif device_type == "entraid":
                client = EntraIDClient(config)
            elif device_type == "siem":
                client = SIEMClient(config)
            else:
                return {
                    "success": False,
                    "message": f"Unsupported device type: {device_type}",
                    "details": {
                        "error": "Invalid device type",
                        "suggestion": "Use paloalto, entraid, or siem"
                    }
                }
            
            result = client.test_connection()
            return result
            
        except ValueError as e:
            # Configuration validation errors
            return {
                "success": False,
                "message": "Configuration error",
                "details": {
                    "error": str(e),
                    "suggestion": "Check that all required configuration parameters are provided"
                }
            }
        except Exception as e:
            logger.error(f"Connection test failed for {device_type}: {e}", exc_info=True)
            return {
                "success": False,
                "message": "Connection test failed",
                "details": {
                    "error": str(e),
                    "suggestion": "Check logs for detailed error information"
                }
            }
