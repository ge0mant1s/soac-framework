"""
Detection Engine - Multi-phase attack detection using operational models
"""
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
from ..operational_models.model_loader import get_model_loader
from ..models import Incident
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DetectionEngine:
    """
    Intelligent detection engine that:
    1. Processes events against operational model patterns
    2. Tracks multi-phase attack sequences
    3. Correlates events across time windows
    4. Creates incidents when patterns match
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.model_loader = get_model_loader()
        
        # In-memory state tracking for correlation
        # Structure: {entity_key: {model_id: {phase_id: [events]}}}
        self.entity_state: Dict[str, Dict[str, Dict[str, List[Dict]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )
        
        # Track when entities were last seen
        self.entity_last_seen: Dict[str, datetime] = {}
        
        # Statistics
        self.stats = {
            "events_processed": 0,
            "incidents_created": 0,
            "patterns_matched": 0
        }
    
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single event and check for pattern matches
        
        Args:
            event: Normalized event dictionary
        
        Returns:
            Incident data if a pattern is matched, None otherwise
        """
        self.stats["events_processed"] += 1
        
        # Extract entity key for correlation
        entity_key = self._extract_entity_key(event)
        
        # Update entity last seen
        self.entity_last_seen[entity_key] = datetime.utcnow()
        
        # Try to match against all models
        for model_id, model in self.model_loader.get_all_models().items():
            matched_incident = self._match_against_model(event, entity_key, model_id, model)
            if matched_incident:
                return matched_incident
        
        return None
    
    def process_batch(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple events in batch
        
        Args:
            events: List of normalized events
        
        Returns:
            List of created incidents
        """
        incidents = []
        for event in events:
            incident = self.process_event(event)
            if incident:
                incidents.append(incident)
        return incidents
    
    def _extract_entity_key(self, event: Dict[str, Any]) -> str:
        """
        Extract entity key for correlation (user, computer, IP, etc.)
        
        Priority:
        1. UserName + ComputerName
        2. UserName + aip (IP address)
        3. ComputerName
        4. UserName
        5. aip
        """
        username = event.get("UserName") or event.get("UserPrincipalName") or event.get("user")
        computer = event.get("ComputerName") or event.get("hostname") or event.get("host")
        ip = event.get("aip") or event.get("RemoteAddressIP4") or event.get("ip")
        
        # Build entity key
        parts = []
        if username:
            parts.append(f"user:{username}")
        if computer:
            parts.append(f"host:{computer}")
        if ip and not username and not computer:
            parts.append(f"ip:{ip}")
        
        if not parts:
            # Fallback to event ID if no entity identifiers
            parts.append(f"event:{event.get('event_id', 'unknown')}")
        
        return "|".join(parts)
    
    def _match_against_model(
        self, 
        event: Dict[str, Any], 
        entity_key: str, 
        model_id: str, 
        model: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Match event against a specific operational model
        
        Returns:
            Incident data if pattern matches threshold, None otherwise
        """
        correlation_pattern = model.get("correlation_pattern", {})
        phases = correlation_pattern.get("phases", [])
        
        if not phases:
            return None
        
        # Try to match event against each phase
        matched_phase = self._match_phase(event, phases)
        
        if matched_phase:
            # Add event to entity state
            self.entity_state[entity_key][model_id][matched_phase["name"]].append({
                "event": event,
                "timestamp": datetime.utcnow(),
                "phase": matched_phase["name"]
            })
            
            # Clean old events outside correlation window
            self._clean_old_events(entity_key, model_id, correlation_pattern)
            
            # Check if we have enough phases matched to create an incident
            incident = self._check_incident_threshold(entity_key, model_id, model)
            if incident:
                self.stats["incidents_created"] += 1
                return incident
        
        return None
    
    def _match_phase(self, event: Dict[str, Any], phases: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Check if event matches any phase in the operational model
        
        Args:
            event: Normalized event
            phases: List of phases from operational model
        
        Returns:
            Matched phase dict or None
        """
        event_type = event.get("event_type", "").lower()
        source = event.get("source", "").lower()
        
        for phase in phases:
            phase_name = phase.get("name", "").lower()
            phase_source = phase.get("source", "").lower()
            phase_indicators = phase.get("indicators", "").lower()
            
            # Match by source
            source_match = False
            if source:
                # Check if event source matches phase source
                if any(s in source for s in ["falcon", "paloalto", "entraid", "umbrella", "proofpoint"]):
                    if any(s in phase_source for s in ["falcon", "paloalto", "entraid", "umbrella", "proofpoint"]):
                        if source.split('_')[0] in phase_source or phase_source.split()[0] in source:
                            source_match = True
            
            # Match by indicators
            indicator_match = False
            if phase_indicators:
                # Check for common indicator patterns
                if any(keyword in str(event.values()).lower() for keyword in [
                    "powershell", "cmd.exe", "wscript", "rundll32",  # Execution
                    "processrollup", "filewrite", "dataStaged",  # Endpoint
                    "networkconnect", "remoteaddress", "putobject",  # Network/Cloud
                    "authentication", "login", "signin",  # Auth
                    "upload", "download", "transfer"  # Data movement
                ]):
                    indicator_match = True
            
            # Also match by phase name keywords in event
            phase_keyword_match = False
            phase_keywords = {
                "delivery": ["email", "attachment", "proofpoint"],
                "execution": ["process", "cmd", "powershell", "script"],
                "network": ["connection", "outbound", "remote", "c2"],
                "persistence": ["filewrite", "service", "startup", "registry"],
                "staging": ["zip", "rar", "archive", "staged"],
                "transfer": ["upload", "download", "exfil"],
                "authentication": ["login", "auth", "signin", "mfa"],
                "privilege": ["admin", "elevate", "privilege"],
                "lateral": ["smb", "rdp", "wmi", "movement"],
                "discovery": ["recon", "whoami", "ipconfig", "enum"]
            }
            
            for keyword_group, keywords in phase_keywords.items():
                if keyword_group in phase_name:
                    if any(kw in str(event.values()).lower() for kw in keywords):
                        phase_keyword_match = True
                        break
            
            # Match if any criteria met
            if source_match or indicator_match or phase_keyword_match:
                logger.info(f"Event matched phase: {phase['name']}")
                self.stats["patterns_matched"] += 1
                return phase
        
        return None
    
    def _clean_old_events(self, entity_key: str, model_id: str, correlation_pattern: Dict[str, Any]):
        """Remove events outside the correlation window"""
        window_str = correlation_pattern.get("correlation_window", "60 minutes")
        
        # Parse window (e.g., "0-60 minutes", "6 hours", "90m")
        window_minutes = self._parse_time_window(window_str)
        cutoff_time = datetime.utcnow() - timedelta(minutes=window_minutes)
        
        # Clean old events for this entity and model
        if entity_key in self.entity_state and model_id in self.entity_state[entity_key]:
            for phase_name in self.entity_state[entity_key][model_id]:
                self.entity_state[entity_key][model_id][phase_name] = [
                    e for e in self.entity_state[entity_key][model_id][phase_name]
                    if e["timestamp"] > cutoff_time
                ]
    
    def _parse_time_window(self, window_str: str) -> int:
        """Parse time window string to minutes"""
        window_str = window_str.lower().strip()
        
        # Extract number
        import re
        numbers = re.findall(r'\d+', window_str)
        if not numbers:
            return 60  # Default 60 minutes
        
        value = int(numbers[-1])  # Take last number (handles "0-60 minutes")
        
        # Determine unit
        if 'hour' in window_str or 'h' in window_str:
            return value * 60
        elif 'minute' in window_str or 'm' in window_str:
            return value
        elif 'second' in window_str or 's' in window_str:
            return max(1, value // 60)
        else:
            return value  # Assume minutes
    
    def _check_incident_threshold(
        self, 
        entity_key: str, 
        model_id: str, 
        model: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Check if enough phases are matched to create an incident
        
        Returns:
            Incident data if threshold met, None otherwise
        """
        # Get alert policy
        alert_policy = model.get("alert_policy", {})
        trigger = alert_policy.get("trigger_condition", "")
        
        # Parse threshold (e.g., "≥ 3 correlated phases", "3 phases correlated")
        import re
        threshold_match = re.search(r'(\d+)', trigger)
        threshold = int(threshold_match.group(1)) if threshold_match else 3
        
        # Count unique phases matched
        phases_matched = []
        event_count = 0
        all_events = []
        
        if entity_key in self.entity_state and model_id in self.entity_state[entity_key]:
            for phase_name, events in self.entity_state[entity_key][model_id].items():
                if events:
                    phases_matched.append(phase_name)
                    event_count += len(events)
                    all_events.extend(events)
        
        # Check if threshold met
        if len(phases_matched) >= threshold:
            # Calculate confidence level
            total_phases = len(model.get("correlation_pattern", {}).get("phases", []))
            confidence_pct = (len(phases_matched) / total_phases) * 100 if total_phases > 0 else 0
            
            if confidence_pct >= 80:
                confidence = "high"
            elif confidence_pct >= 50:
                confidence = "medium"
            else:
                confidence = "low"
            
            # Create incident
            incident_data = {
                "incident_id": f"INC-{uuid.uuid4().hex[:8].upper()}",
                "pattern_id": model["id"],
                "pattern_name": model["name"],
                "entity_key": entity_key,
                "phases_matched": phases_matched,
                "confidence_level": confidence,
                "event_count": event_count,
                "events": [
                    {
                        "phase": e["phase"],
                        "timestamp": e["timestamp"].isoformat(),
                        "event_data": e["event"]
                    }
                    for e in all_events
                ],
                "severity": alert_policy.get("severity", "High"),
                "status": "open",
                "created_at": datetime.utcnow()
            }
            
            # Save to database
            self._save_incident(incident_data)
            
            # Clear entity state for this model (to avoid duplicate incidents)
            if entity_key in self.entity_state and model_id in self.entity_state[entity_key]:
                self.entity_state[entity_key][model_id].clear()
            
            logger.info(f"Created incident: {incident_data['incident_id']} for pattern {model['name']}")
            return incident_data
        
        return None
    
    def _save_incident(self, incident_data: Dict[str, Any]):
        """Save incident to database"""
        try:
            incident = Incident(
                incident_id=incident_data["incident_id"],
                pattern_id=incident_data["pattern_id"],
                pattern_name=incident_data["pattern_name"],
                entity_key=incident_data["entity_key"],
                phases_matched=incident_data["phases_matched"],
                confidence_level=incident_data["confidence_level"],
                event_count=incident_data["event_count"],
                events=incident_data["events"],
                severity=incident_data["severity"],
                status=incident_data["status"],
                created_at=incident_data["created_at"]
            )
            self.db.add(incident)
            self.db.commit()
            logger.info(f"Saved incident to database: {incident_data['incident_id']}")
        except Exception as e:
            logger.error(f"Failed to save incident: {str(e)}")
            self.db.rollback()
    
    def get_stats(self) -> Dict[str, int]:
        """Get detection engine statistics"""
        return {
            **self.stats,
            "active_entities": len(self.entity_state),
            "loaded_models": len(self.model_loader.get_all_models())
        }
    
    def clear_entity_state(self, entity_key: Optional[str] = None):
        """Clear entity state (useful for testing or manual cleanup)"""
        if entity_key:
            if entity_key in self.entity_state:
                del self.entity_state[entity_key]
        else:
            self.entity_state.clear()
    
    def get_entity_state(self, entity_key: str) -> Dict[str, Any]:
        """Get current state for an entity"""
        if entity_key not in self.entity_state:
            return {}
        
        return {
            model_id: {
                phase_name: len(events)
                for phase_name, events in phases.items()
            }
            for model_id, phases in self.entity_state[entity_key].items()
        }
