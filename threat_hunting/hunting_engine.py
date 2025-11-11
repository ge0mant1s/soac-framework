"""
SOaC Threat Hunting Engine
"""

import json
from datetime import datetime
from typing import List, Dict, Any
import uuid

class ThreatHuntingEngine:
    
    def __init__(self, db_connection=None, ai_engine=None):
        self.db = db_connection
        self.ai = ai_engine
        self.hunt_templates = self._load_hunt_templates()
        
    def _load_hunt_templates(self) -> Dict:
        return {
            "credential_abuse": {
                "name": "Credential Abuse Hunting",
                "description": "Hunt for signs of credential compromise and abuse",
                "mitre_tactics": ["Credential Access", "Lateral Movement"],
                "queries": [
                    {
                        "platform": "entraid",
                        "cql": "event.outcome = success | user.risk_level = high | groupBy(user.name, source.ip)"
                    }
                ]
            },
            "data_exfiltration": {
                "name": "Data Exfiltration Hunting",
                "description": "Hunt for unusual data transfer patterns",
                "mitre_tactics": ["Exfiltration"],
                "queries": [
                    {
                        "platform": "paloalto",
                        "cql": "bytes.sent > 1000000000 | groupBy(source.ip, destination.ip)"
                    }
                ]
            }
        }
    
    def get_hunt_templates(self) -> List[Dict]:
        return [
            {
                "id": key,
                "name": template["name"],
                "description": template["description"],
                "mitre_tactics": template["mitre_tactics"]
            }
            for key, template in self.hunt_templates.items()
        ]
    
    def create_hunt(self, hunt_data: Dict) -> Dict:
        hunt = {
            "id": f"HUNT-{uuid.uuid4().hex[:8].upper()}",
            "name": hunt_data.get("name"),
            "description": hunt_data.get("description"),
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        }
        return hunt
