
"""
Palo Alto NGFW API Client
Supports PAN-OS REST API for firewall management and threat log collection
"""
import requests
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class PaloAltoClient:
    """
    Client for Palo Alto Networks firewall API integration
    Supports authentication, configuration retrieval, and log collection
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Palo Alto client with configuration
        
        Args:
            config: Dictionary containing:
                - api_url: Base URL for PAN-OS API (e.g., https://firewall.example.com)
                - api_key: API key for authentication
                - verify_ssl: Optional, default True
        """
        self.api_url = config.get("api_url", "").rstrip("/")
        self.api_key = config.get("api_key", "")
        self.verify_ssl = config.get("verify_ssl", True)
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        
        if not self.api_url or not self.api_key:
            raise ValueError("api_url and api_key are required for Palo Alto integration")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to Palo Alto firewall
        
        Returns:
            Dictionary with success status, message, and details
        """
        try:
            # Use show system info command to test connectivity
            params = {
                "type": "op",
                "cmd": "<show><system><info></info></system></show>",
                "key": self.api_key
            }
            
            response = self.session.get(
                f"{self.api_url}/api/",
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"Connection failed with status {response.status_code}",
                    "details": {
                        "error": response.text[:200],
                        "suggestion": "Check API URL and network connectivity"
                    }
                }
            
            # Parse XML response
            root = ET.fromstring(response.text)
            status = root.get("status")
            
            if status != "success":
                error_msg = root.find(".//msg")
                return {
                    "success": False,
                    "message": "Authentication failed",
                    "details": {
                        "error": error_msg.text if error_msg is not None else "Invalid API key",
                        "suggestion": "Verify your API key is correct and has proper permissions"
                    }
                }
            
            # Extract system info
            result = root.find(".//result")
            system_info = {}
            if result is not None:
                system_info = {
                    "hostname": self._get_xml_text(result, "hostname"),
                    "model": self._get_xml_text(result, "model"),
                    "sw_version": self._get_xml_text(result, "sw-version"),
                    "serial": self._get_xml_text(result, "serial")
                }
            
            return {
                "success": True,
                "message": "Successfully connected to Palo Alto firewall",
                "details": {
                    "device_info": system_info,
                    "api_version": "PAN-OS REST API",
                    "latency_ms": int(response.elapsed.total_seconds() * 1000)
                }
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Connection timeout",
                "details": {
                    "error": "Request timed out after 10 seconds",
                    "suggestion": "Check network connectivity and firewall accessibility"
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": "Connection error",
                "details": {
                    "error": str(e),
                    "suggestion": "Verify API URL format and network connectivity"
                }
            }
        except Exception as e:
            logger.error(f"Palo Alto connection test failed: {e}", exc_info=True)
            return {
                "success": False,
                "message": "Unexpected error during connection test",
                "details": {
                    "error": str(e),
                    "suggestion": "Check logs for detailed error information"
                }
            }
    
    def get_security_rules(self) -> List[Dict[str, Any]]:
        """
        Fetch security rules from Palo Alto firewall
        
        Returns:
            List of security rules in normalized format
        """
        try:
            params = {
                "type": "config",
                "action": "get",
                "xpath": "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/security/rules",
                "key": self.api_key
            }
            
            response = self.session.get(
                f"{self.api_url}/api/",
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch security rules: {response.status_code}")
                return []
            
            root = ET.fromstring(response.text)
            
            if root.get("status") != "success":
                logger.error("Security rules fetch failed")
                return []
            
            rules = []
            result = root.find(".//result/rules")
            if result is not None:
                for entry in result.findall("entry"):
                    rule = self._parse_security_rule(entry)
                    if rule:
                        rules.append(rule)
            
            logger.info(f"Fetched {len(rules)} security rules from Palo Alto")
            return rules
            
        except Exception as e:
            logger.error(f"Error fetching security rules: {e}", exc_info=True)
            return []
    
    def get_threat_logs(self, time_range: str = "last-24-hrs", limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch threat logs from Palo Alto firewall
        
        Args:
            time_range: Time range for logs (e.g., "last-24-hrs", "last-hour")
            limit: Maximum number of logs to retrieve
            
        Returns:
            List of threat log entries
        """
        try:
            query = f"( receive_time geq '{time_range}' )"
            
            params = {
                "type": "log",
                "log-type": "threat",
                "query": query,
                "nlogs": limit,
                "key": self.api_key
            }
            
            response = self.session.get(
                f"{self.api_url}/api/",
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch threat logs: {response.status_code}")
                return []
            
            root = ET.fromstring(response.text)
            
            if root.get("status") != "success":
                logger.error("Threat logs fetch failed")
                return []
            
            logs = []
            result = root.find(".//result/log/logs")
            if result is not None:
                for entry in result.findall("entry"):
                    log = self._parse_threat_log(entry)
                    if log:
                        logs.append(log)
            
            logger.info(f"Fetched {len(logs)} threat logs from Palo Alto")
            return logs
            
        except Exception as e:
            logger.error(f"Error fetching threat logs: {e}", exc_info=True)
            return []
    
    def get_device_health(self) -> Dict[str, Any]:
        """
        Get device health metrics
        
        Returns:
            Dictionary with health metrics
        """
        try:
            params = {
                "type": "op",
                "cmd": "<show><system><info></info></system></show>",
                "key": self.api_key
            }
            
            response = self.session.get(
                f"{self.api_url}/api/",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                if root.get("status") == "success":
                    result = root.find(".//result")
                    if result is not None:
                        return {
                            "status": "healthy",
                            "uptime": self._get_xml_text(result, "uptime"),
                            "version": self._get_xml_text(result, "sw-version"),
                            "model": self._get_xml_text(result, "model")
                        }
            
            return {"status": "unhealthy", "error": "Failed to fetch health metrics"}
            
        except Exception as e:
            logger.error(f"Error fetching device health: {e}")
            return {"status": "error", "error": str(e)}
    
    def _parse_security_rule(self, entry: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse XML security rule entry to dictionary"""
        try:
            return {
                "name": entry.get("name", ""),
                "action": self._get_xml_text(entry, "action"),
                "source_zones": self._get_xml_list(entry, "from/member"),
                "dest_zones": self._get_xml_list(entry, "to/member"),
                "source_addresses": self._get_xml_list(entry, "source/member"),
                "dest_addresses": self._get_xml_list(entry, "destination/member"),
                "applications": self._get_xml_list(entry, "application/member"),
                "services": self._get_xml_list(entry, "service/member"),
                "description": self._get_xml_text(entry, "description"),
                "disabled": self._get_xml_text(entry, "disabled") == "yes"
            }
        except Exception as e:
            logger.error(f"Error parsing security rule: {e}")
            return None
    
    def _parse_threat_log(self, entry: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse XML threat log entry to dictionary"""
        try:
            return {
                "timestamp": self._get_xml_text(entry, "receive_time"),
                "threat_type": self._get_xml_text(entry, "subtype"),
                "severity": self._get_xml_text(entry, "severity"),
                "source_ip": self._get_xml_text(entry, "src"),
                "dest_ip": self._get_xml_text(entry, "dst"),
                "threat_name": self._get_xml_text(entry, "threatid"),
                "action": self._get_xml_text(entry, "action"),
                "application": self._get_xml_text(entry, "app"),
                "rule": self._get_xml_text(entry, "rule")
            }
        except Exception as e:
            logger.error(f"Error parsing threat log: {e}")
            return None
    
    def _get_xml_text(self, element: ET.Element, path: str) -> str:
        """Safely get text from XML element"""
        try:
            node = element.find(path)
            return node.text if node is not None and node.text else ""
        except Exception:
            return ""
    
    def _get_xml_list(self, element: ET.Element, path: str) -> List[str]:
        """Get list of text values from XML elements"""
        try:
            nodes = element.findall(path)
            return [node.text for node in nodes if node.text]
        except Exception:
            return []
