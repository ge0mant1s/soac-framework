
"""
Correlation Engine - Multi-source event correlation for threat detection
Implements the strategic correlation patterns defined in the SOaC Framework
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class CorrelationEngine:
    """
    Main correlation engine for multi-source threat detection
    Implements correlation patterns from the tactical library
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the correlation engine
        
        Args:
            config: Configuration dictionary containing correlation settings
        """
        self.config = config
        self.correlation_windows = {
            'real_time': timedelta(minutes=15),
            'short_term': timedelta(minutes=90),
            'long_term': timedelta(hours=24)
        }
        self.confidence_threshold = config.get('confidence_threshold', 3)
        logger.info("Correlation Engine initialized")
    
    def correlate_events(self, events: List[Dict[str, Any]], 
                        pattern_id: str,
                        time_window: str = 'short_term') -> List[Dict[str, Any]]:
        """
        Correlate events based on a specific pattern
        
        Args:
            events: List of events from various sources
            pattern_id: Pattern identifier (e.g., 'R1', 'D1', 'C1')
            time_window: Time window for correlation
            
        Returns:
            List of correlated incident objects
        """
        window = self.correlation_windows.get(time_window, timedelta(minutes=60))
        correlated_incidents = []
        
        # Group events by entity (UserName, ComputerName, etc.)
        entity_groups = self._group_by_entity(events)
        
        for entity_key, entity_events in entity_groups.items():
            # Check if events match the pattern phases
            phases_matched = self._match_pattern_phases(entity_events, pattern_id)
            
            if len(phases_matched) >= self.confidence_threshold:
                incident = self._create_incident(
                    entity_key=entity_key,
                    matched_events=entity_events,
                    phases=phases_matched,
                    pattern_id=pattern_id
                )
                correlated_incidents.append(incident)
                logger.warning(f"High-confidence incident detected: {incident['incident_id']}")
        
        return correlated_incidents
    
    def _group_by_entity(self, events: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Group events by common entities (UserName, ComputerName, IP)"""
        entity_groups = {}
        
        for event in events:
            # Extract entity identifiers
            entities = []
            if 'UserName' in event:
                entities.append(('user', event['UserName']))
            if 'ComputerName' in event:
                entities.append(('computer', event['ComputerName']))
            if 'aip' in event:
                entities.append(('ip', event['aip']))
            
            # Create composite key
            entity_key = "|".join([f"{k}:{v}" for k, v in entities])
            
            if entity_key not in entity_groups:
                entity_groups[entity_key] = []
            entity_groups[entity_key].append(event)
        
        return entity_groups
    
    def _match_pattern_phases(self, events: List[Dict[str, Any]], 
                             pattern_id: str) -> List[str]:
        """
        Match events against pattern phases
        
        Pattern phases are based on MITRE ATT&CK tactics:
        - Initial Access
        - Execution
        - Persistence
        - Privilege Escalation
        - Defense Evasion
        - Credential Access
        - Discovery
        - Lateral Movement
        - Collection
        - Exfiltration
        - Command and Control
        - Impact
        """
        matched_phases = set()
        
        for event in events:
            event_type = event.get('event_type', '')
            source = event.get('source', '')
            
            # Pattern-specific phase matching
            if pattern_id == 'R1':  # Ransomware
                if 'email' in source.lower() or 'proofpoint' in source.lower():
                    matched_phases.add('Initial Access')
                if 'ProcessRollup' in event_type or 'powershell' in event.get('CommandLine', '').lower():
                    matched_phases.add('Execution')
                if 'FileWriteInfo' in event_type or 'encrypted' in event.get('TargetFileName', '').lower():
                    matched_phases.add('Impact')
            
            elif pattern_id == 'D1':  # Data Exfiltration
                if 'DataStaged' in event_type:
                    matched_phases.add('Collection')
                if 'NetworkConnectIP4' in event_type:
                    matched_phases.add('Exfiltration')
                if 'PutObject' in event.get('aws_eventName', ''):
                    matched_phases.add('Impact')
            
            elif pattern_id == 'C1':  # Credential Abuse
                if 'LDAP' in event_type or 'NTLM' in event_type:
                    matched_phases.add('Credential Access')
                if 'MFA' in event.get('ResultType', ''):
                    matched_phases.add('Persistence')
            
            elif pattern_id == 'IN1':  # Intrusion
                if 'ProcessRollup' in event_type:
                    matched_phases.add('Execution')
                if event.get('RemotePort') in [445, 135, 3389]:
                    matched_phases.add('Lateral Movement')
                if 'ScheduledTask' in event_type or 'ServiceInstall' in event_type:
                    matched_phases.add('Persistence')
        
        return list(matched_phases)
    
    def _create_incident(self, entity_key: str, matched_events: List[Dict],
                        phases: List[str], pattern_id: str) -> Dict[str, Any]:
        """Create an incident object from correlated events"""
        incident_id = f"INC-{pattern_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            'incident_id': incident_id,
            'pattern_id': pattern_id,
            'entity_key': entity_key,
            'phases_matched': phases,
            'confidence_level': self._calculate_confidence(len(phases)),
            'event_count': len(matched_events),
            'events': matched_events,
            'timestamp': datetime.now().isoformat(),
            'status': 'open',
            'severity': self._calculate_severity(pattern_id, len(phases))
        }
    
    def _calculate_confidence(self, phase_count: int) -> str:
        """Calculate confidence level based on matched phases"""
        if phase_count >= 4:
            return 'Critical'
        elif phase_count >= 3:
            return 'High'
        elif phase_count >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_severity(self, pattern_id: str, phase_count: int) -> str:
        """Calculate severity based on pattern and phase count"""
        high_severity_patterns = ['R1', 'D1', 'FF1', 'IN1']
        
        if pattern_id in high_severity_patterns and phase_count >= 3:
            return 'Critical'
        elif phase_count >= 3:
            return 'High'
        elif phase_count >= 2:
            return 'Medium'
        else:
            return 'Low'


def test_correlation_engine():
    """Test function for correlation engine"""
    config = {'confidence_threshold': 3}
    engine = CorrelationEngine(config)
    
    # Sample events for testing
    sample_events = [
        {
            'event_type': 'ProcessRollup2',
            'source': 'Falcon',
            'UserName': 'test_user',
            'ComputerName': 'DESKTOP-001',
            'CommandLine': 'powershell.exe -enc ABCD',
            'timestamp': datetime.now().isoformat()
        },
        {
            'event_type': 'NetworkConnectIP4',
            'source': 'Falcon',
            'UserName': 'test_user',
            'ComputerName': 'DESKTOP-001',
            'RemoteAddressIP4': '192.168.1.100',
            'timestamp': datetime.now().isoformat()
        },
        {
            'event_type': 'FileWriteInfo',
            'source': 'Falcon',
            'UserName': 'test_user',
            'ComputerName': 'DESKTOP-001',
            'TargetFileName': 'document.encrypted',
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    incidents = engine.correlate_events(sample_events, pattern_id='R1')
    print(f"Detected {len(incidents)} incidents")
    if incidents:
        print(json.dumps(incidents[0], indent=2))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_correlation_engine()
