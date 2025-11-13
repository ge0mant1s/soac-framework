"""
Event Processor - Normalizes events from different sources into a common format
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

logger = logging.getLogger(__name__)


class EventProcessor:
    """
    Normalizes events from various sources (Palo Alto, Entra ID, SIEM, etc.)
    into a common format for detection engine processing
    """
    
    # Common field mappings for different sources
    FIELD_MAPPINGS = {
        "paloalto": {
            "user": "UserName",
            "src_ip": "LocalAddressIP4",
            "dest_ip": "RemoteAddressIP4",
            "src_port": "LocalPort",
            "dest_port": "RemotePort",
            "action": "Action",
            "device": "DeviceName"
        },
        "entraid": {
            "userPrincipalName": "UserName",
            "ipAddress": "aip",
            "location": "Location",
            "appDisplayName": "Application",
            "status": "Status",
            "deviceDetail.operatingSystem": "OperatingSystem"
        },
        "falcon": {
            "ComputerName": "ComputerName",
            "UserName": "UserName",
            "FileName": "FileName",
            "CommandLine": "CommandLine",
            "SHA256HashData": "SHA256HashData",
            "event_simpleName": "event_type"
        },
        "siem": {
            "host": "ComputerName",
            "user": "UserName",
            "source_ip": "aip",
            "event_type": "event_type"
        }
    }
    
    def __init__(self):
        self.processed_count = 0
    
    def normalize_event(self, raw_event: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Normalize a raw event from a specific source
        
        Args:
            raw_event: Raw event data from source
            source: Source type (paloalto, entraid, falcon, siem)
        
        Returns:
            Normalized event dictionary
        """
        self.processed_count += 1
        
        # Create base normalized event
        normalized = {
            "event_id": str(uuid.uuid4()),
            "source": source.lower(),
            "timestamp": self._extract_timestamp(raw_event),
            "raw_event": raw_event
        }
        
        # Apply source-specific field mappings
        if source.lower() in self.FIELD_MAPPINGS:
            mappings = self.FIELD_MAPPINGS[source.lower()]
            for raw_field, normalized_field in mappings.items():
                value = self._extract_nested_field(raw_event, raw_field)
                if value is not None:
                    normalized[normalized_field] = value
        
        # Extract common fields that might be in different formats
        normalized = self._extract_common_fields(normalized, raw_event)
        
        # Add event type classification
        normalized["event_type"] = self._classify_event_type(normalized)
        
        logger.debug(f"Normalized event from {source}: {normalized['event_id']}")
        return normalized
    
    def _extract_timestamp(self, event: Dict[str, Any]) -> str:
        """Extract or generate timestamp"""
        timestamp_fields = ["timestamp", "time", "@timestamp", "eventTime", "createdDateTime", "Timestamp"]
        
        for field in timestamp_fields:
            if field in event:
                ts = event[field]
                if isinstance(ts, str):
                    return ts
                elif isinstance(ts, datetime):
                    return ts.isoformat()
        
        # If no timestamp found, use current time
        return datetime.utcnow().isoformat()
    
    def _extract_nested_field(self, data: Dict[str, Any], field_path: str) -> Any:
        """Extract field from nested dictionary using dot notation"""
        parts = field_path.split('.')
        value = data
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        
        return value
    
    def _extract_common_fields(self, normalized: Dict[str, Any], raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """Extract common fields that might be in different formats"""
        
        # User identification
        if "UserName" not in normalized:
            for field in ["user", "username", "user_name", "userName", "account", "identity"]:
                value = raw_event.get(field)
                if value:
                    normalized["UserName"] = value
                    break
        
        # Computer/Host identification
        if "ComputerName" not in normalized:
            for field in ["computer", "hostname", "host", "device", "machine", "endpoint"]:
                value = raw_event.get(field)
                if value:
                    normalized["ComputerName"] = value
                    break
        
        # IP Address
        if "aip" not in normalized:
            for field in ["ip", "ip_address", "ipAddress", "source_ip", "src_ip", "clientIP"]:
                value = raw_event.get(field)
                if value:
                    normalized["aip"] = value
                    break
        
        # File information
        if "FileName" not in normalized:
            for field in ["file", "filename", "file_name", "targetFileName", "path"]:
                value = raw_event.get(field)
                if value:
                    normalized["FileName"] = value
                    break
        
        # Process information
        if "CommandLine" not in normalized:
            for field in ["command", "commandline", "cmd", "process_command", "command_line"]:
                value = raw_event.get(field)
                if value:
                    normalized["CommandLine"] = value
                    break
        
        # Action/Result
        if "Action" not in normalized:
            for field in ["action", "result", "status", "outcome", "disposition"]:
                value = raw_event.get(field)
                if value:
                    normalized["Action"] = value
                    break
        
        return normalized
    
    def _classify_event_type(self, event: Dict[str, Any]) -> str:
        """
        Classify event type based on fields and content
        
        Returns one of:
        - authentication
        - network
        - process_execution
        - file_operation
        - cloud_operation
        - email
        - unknown
        """
        # Check source-specific event types
        if "event_type" in event:
            return event["event_type"]
        
        # Authentication events
        if any(field in event for field in ["UserName", "login", "signin", "authentication"]):
            if event.get("source") == "entraid" or "auth" in str(event.get("raw_event", {})).lower():
                return "authentication"
        
        # Network events
        if any(field in event for field in ["RemoteAddressIP4", "LocalAddressIP4", "RemotePort"]):
            return "network"
        
        # Process execution
        if any(field in event for field in ["CommandLine", "ProcessRollup", "FileName"]):
            cmd = str(event.get("CommandLine", "")).lower()
            if any(proc in cmd for proc in ["powershell", "cmd.exe", "wscript", "rundll32"]):
                return "process_execution"
        
        # File operations
        if "FileWrite" in str(event.get("raw_event", {})) or "file" in str(event.get("Action", "")).lower():
            return "file_operation"
        
        # Cloud operations
        if event.get("source") in ["aws", "azure", "gcp"] or "cloud" in event.get("source", ""):
            return "cloud_operation"
        
        # Email events
        if event.get("source") == "proofpoint" or "email" in str(event.get("raw_event", {})).lower():
            return "email"
        
        return "unknown"
    
    def normalize_batch(self, events: list, source: str) -> list:
        """
        Normalize a batch of events
        
        Args:
            events: List of raw events
            source: Source type
        
        Returns:
            List of normalized events
        """
        return [self.normalize_event(event, source) for event in events]
    
    def get_stats(self) -> Dict[str, int]:
        """Get processor statistics"""
        return {
            "events_processed": self.processed_count
        }


# Convenience functions for common sources

def normalize_paloalto_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Palo Alto firewall event"""
    processor = EventProcessor()
    return processor.normalize_event(event, "paloalto")


def normalize_entraid_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Entra ID authentication event"""
    processor = EventProcessor()
    return processor.normalize_event(event, "entraid")


def normalize_falcon_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize CrowdStrike Falcon event"""
    processor = EventProcessor()
    return processor.normalize_event(event, "falcon")


def normalize_siem_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize generic SIEM event"""
    processor = EventProcessor()
    return processor.normalize_event(event, "siem")
