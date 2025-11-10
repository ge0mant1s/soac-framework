"""
Incident Management System
Complete lifecycle management for security incidents
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
import uuid


class IncidentStatus(Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    ERADICATED = "eradicated"
    RECOVERED = "recovered"
    CLOSED = "closed"


class IncidentSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Incident:
    """Incident data model"""

    def __init__(self, title: str, severity: str, use_case: str, **kwargs):
        self.id = str(uuid.uuid4())
        self.title = title
        self.severity = severity
        self.use_case = use_case
        self.status = IncidentStatus.NEW.value
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.assigned_to = kwargs.get('assigned_to')
        self.description = kwargs.get('description', '')
        self.source_alert = kwargs.get('source_alert', {})
        self.evidence = []
        self.timeline = []
        self.tags = kwargs.get('tags', [])

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'severity': self.severity,
            'use_case': self.use_case,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'assigned_to': self.assigned_to,
            'description': self.description,
            'evidence_count': len(self.evidence),
            'tags': self.tags
        }


class IncidentManager:
    """Manages security incidents throughout their lifecycle"""

    def __init__(self):
        self.incidents = {}
        self.sla_config = {
            'critical': {'response': 15, 'resolution': 240},  # minutes
            'high': {'response': 60, 'resolution': 480},
            'medium': {'response': 240, 'resolution': 1440},
            'low': {'response': 1440, 'resolution': 4320}
        }

    def create_incident(self, title: str, severity: str, use_case: str, **kwargs) -> Incident:
        """Create a new incident"""
        incident = Incident(title, severity, use_case, **kwargs)
        self.incidents[incident.id] = incident

        incident.timeline.append({
            'timestamp': datetime.utcnow().isoformat(),
            'action': 'created',
            'details': f'Incident created with severity {severity}'
        })

        return incident

    def update_status(self, incident_id: str, new_status: str, notes: str = '') -> bool:
        """Update incident status"""
        if incident_id not in self.incidents:
            return False

        incident = self.incidents[incident_id]
        old_status = incident.status
        incident.status = new_status
        incident.updated_at = datetime.utcnow()

        incident.timeline.append({
            'timestamp': datetime.utcnow().isoformat(),
            'action': 'status_changed',
            'details': f'Status changed from {old_status} to {new_status}',
            'notes': notes
        })

        return True

    def add_evidence(self, incident_id: str, evidence: Dict[str, Any]) -> bool:
        """Add evidence to incident"""
        if incident_id not in self.incidents:
            return False

        incident = self.incidents[incident_id]
        evidence['timestamp'] = datetime.utcnow().isoformat()
        evidence['id'] = str(uuid.uuid4())
        incident.evidence.append(evidence)
        incident.updated_at = datetime.utcnow()

        return True

    def assign_incident(self, incident_id: str, assignee: str) -> bool:
        """Assign incident to analyst"""
        if incident_id not in self.incidents:
            return False

        incident = self.incidents[incident_id]
        incident.assigned_to = assignee
        incident.updated_at = datetime.utcnow()

        incident.timeline.append({
            'timestamp': datetime.utcnow().isoformat(),
            'action': 'assigned',
            'details': f'Incident assigned to {assignee}'
        })

        return True

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        """Get incident by ID"""
        return self.incidents.get(incident_id)

    def list_incidents(self, filters: Dict[str, Any] = None) -> List[Incident]:
        """List incidents with optional filters"""
        incidents = list(self.incidents.values())

        if filters:
            if 'status' in filters:
                incidents = [i for i in incidents if i.status == filters['status']]
            if 'severity' in filters:
                incidents = [i for i in incidents if i.severity == filters['severity']]
            if 'use_case' in filters:
                incidents = [i for i in incidents if i.use_case == filters['use_case']]

        return incidents

    def check_sla(self, incident_id: str) -> Dict[str, Any]:
        """Check SLA compliance for incident"""
        incident = self.incidents.get(incident_id)
        if not incident:
            return {}

        sla = self.sla_config.get(incident.severity, {})
        age_minutes = (datetime.utcnow() - incident.created_at).total_seconds() / 60

        return {
            'incident_id': incident_id,
            'severity': incident.severity,
            'age_minutes': age_minutes,
            'response_sla': sla.get('response', 0),
            'resolution_sla': sla.get('resolution', 0),
            'response_breached': age_minutes > sla.get('response', 0),
            'resolution_breached': age_minutes > sla.get('resolution', 0) and incident.status != 'closed'
        }
