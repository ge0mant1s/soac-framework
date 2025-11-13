
"""
Threat Intelligence Module - Manage threat actor data and IOCs
Provides context for detection and response
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ThreatIntelligence:
    """
    Threat Intelligence manager for SOaC Framework
    Tracks threat actors, TTPs, and IOCs
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize threat intelligence module
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.threat_actors = {}
        self.iocs = []
        self._load_threat_actors()
        logger.info("Threat Intelligence module initialized")
    
    def _load_threat_actors(self):
        """Load threat actor profiles"""
        
        # Cybercriminal groups
        self.threat_actors['LOCKBIT'] = {
            'name': 'LockBit',
            'type': 'Cybercriminal',
            'geography': 'Global',
            'motivation': 'Purely financial - ransomware-as-a-service (RaaS) operator',
            'techniques': [
                'Double and triple extortion',
                'Lateral movement using RDP, PSExec',
                'Use of automation for faster encryption'
            ],
            'impact': 'Encryption of critical systems, threatening operations',
            'mitre_tactics': ['Initial Access', 'Execution', 'Lateral Movement', 'Impact'],
            'mitre_techniques': ['T1486', 'T1021.001', 'T1059'],
            'severity': 'Critical',
            'likelihood': '★★★★★'
        }
        
        self.threat_actors['CLOP'] = {
            'name': 'Clop',
            'type': 'Cybercriminal',
            'geography': 'Global',
            'motivation': 'Financial (data exfiltration/extortion campaigns)',
            'techniques': [
                'Targeting of MOVEit and other managed file transfer systems',
                'Data leak extortion websites'
            ],
            'impact': 'Massive data exposure of sensitive records',
            'mitre_tactics': ['Initial Access', 'Collection', 'Exfiltration'],
            'mitre_techniques': ['T1190', 'T1005', 'T1567'],
            'severity': 'High',
            'likelihood': '★★★★☆'
        }
        
        self.threat_actors['FIN12'] = {
            'name': 'FIN12',
            'type': 'Cybercriminal',
            'geography': 'Global',
            'motivation': 'Healthcare-focused ransomware deployment',
            'techniques': [
                'Fast deployment of malware post-access',
                'Prefers high-value targets with low tolerance for downtime'
            ],
            'impact': 'Attacks on critical infrastructure; urgent ransom demands',
            'mitre_tactics': ['Execution', 'Persistence', 'Impact'],
            'mitre_techniques': ['T1486', 'T1059', 'T1053'],
            'severity': 'High',
            'likelihood': '★★★☆☆'
        }
        
        # Nation-state actors
        self.threat_actors['APT29'] = {
            'name': 'APT29 (Cozy Bear)',
            'type': 'Nation-State',
            'geography': 'Russia',
            'motivation': 'Espionage; known to target healthcare and pharmaceutical sectors',
            'techniques': [
                'Spear-phishing for credential access',
                'Supply chain exploitation',
                'Stealthy persistence (e.g., WellMess, WellMail)'
            ],
            'impact': 'Theft of research data, surveillance on health policy strategies',
            'mitre_tactics': ['Initial Access', 'Execution', 'Persistence', 'Collection'],
            'mitre_techniques': ['T1566.001', 'T1195', 'T1059', 'T1005'],
            'severity': 'High',
            'likelihood': '★★★☆☆'
        }
        
        self.threat_actors['APT41'] = {
            'name': 'APT41',
            'type': 'Nation-State',
            'geography': 'China',
            'motivation': 'IP theft for state-sponsored industrial gain; hybrid criminal-political activity',
            'techniques': [
                'Web shell deployments',
                'Exploiting VPN and Citrix vulnerabilities',
                'Living-off-the-land tactics'
            ],
            'impact': 'Exfiltration of device schematics, medical AI models, patient datasets',
            'mitre_tactics': ['Initial Access', 'Persistence', 'Privilege Escalation', 'Collection'],
            'mitre_techniques': ['T1190', 'T1505.003', 'T1068', 'T1005'],
            'severity': 'High',
            'likelihood': '★★★☆☆'
        }
        
        self.threat_actors['LAZARUS'] = {
            'name': 'Lazarus Group',
            'type': 'Nation-State',
            'geography': 'North Korea',
            'motivation': 'Financial theft, sabotage, geopolitical disruption',
            'techniques': [
                'Custom ransomware (e.g., WannaCry)',
                'Banking Trojan delivery',
                'Attacks on pharmaceutical payment systems'
            ],
            'impact': 'Major ransomware campaigns impacting hospitals and medical devices',
            'mitre_tactics': ['Initial Access', 'Execution', 'Impact'],
            'mitre_techniques': ['T1486', 'T1204', 'T1499'],
            'severity': 'Critical',
            'likelihood': '★★★☆☆'
        }
        
        # Hacktivists
        self.threat_actors['KILLNET'] = {
            'name': 'KillNet/Anonymous',
            'type': 'Hacktivist',
            'geography': 'Global',
            'motivation': 'Ideologically driven, especially around geopolitical health policies or vaccine distribution',
            'techniques': [
                'DDoS attacks on hospital and health portals',
                'Website defacement',
                'Public data exposure via Telegram or dark web'
            ],
            'impact': 'Operational disruption, reputation damage, misinformation campaigns',
            'mitre_tactics': ['Impact', 'Collection', 'Exfiltration'],
            'mitre_techniques': ['T1499', 'T1005', 'T1567'],
            'severity': 'Medium',
            'likelihood': '★★★☆☆'
        }
        
        # Insider threats
        self.threat_actors['MALICIOUS_INSIDER'] = {
            'name': 'Malicious Insider',
            'type': 'Insider Threat',
            'geography': 'Global',
            'motivation': 'Personal gain (selling data, credentials), ideological motives, human error',
            'techniques': [
                'Unauthorized database queries',
                'USB malware introduction',
                'Policy circumvention or phishing propagation'
            ],
            'impact': 'Credential compromise, data leakage, unauthorized IP access',
            'mitre_tactics': ['Collection', 'Exfiltration', 'Impact'],
            'mitre_techniques': ['T1005', 'T1052', 'T1567'],
            'severity': 'High',
            'likelihood': '★★★☆☆'
        }
        
        # Supply chain adversaries
        self.threat_actors['UNC_GROUPS'] = {
            'name': 'UNC Groups (e.g., UNC2447, UNC3944)',
            'type': 'Supply Chain Adversary',
            'geography': 'Global',
            'motivation': 'Targeting via trusted vendors',
            'techniques': [
                'Exploiting vulnerabilities in widely-used medical platforms',
                'Tainted patches or SDKs'
            ],
            'impact': 'Backdoor access via signed components, affecting device integrity and compliance',
            'mitre_tactics': ['Initial Access', 'Persistence', 'Defense Evasion'],
            'mitre_techniques': ['T1195', 'T1078', 'T1036'],
            'severity': 'High',
            'likelihood': '★★★☆☆'
        }
    
    def get_threat_actor(self, actor_name: str) -> Optional[Dict[str, Any]]:
        """Get threat actor profile by name"""
        return self.threat_actors.get(actor_name.upper())
    
    def list_threat_actors(self, actor_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all threat actors, optionally filtered by type
        
        Args:
            actor_type: Filter by type (Cybercriminal, Nation-State, Hacktivist, etc.)
            
        Returns:
            List of threat actor profiles
        """
        if actor_type:
            return [actor for actor in self.threat_actors.values() if actor['type'] == actor_type]
        return list(self.threat_actors.values())
    
    def add_ioc(self, ioc: Dict[str, Any]):
        """
        Add an Indicator of Compromise (IOC)
        
        Args:
            ioc: IOC dictionary with type, value, and context
        """
        ioc['added_date'] = datetime.now().isoformat()
        self.iocs.append(ioc)
        logger.info(f"Added IOC: {ioc['type']} - {ioc['value']}")
    
    def search_iocs(self, ioc_type: Optional[str] = None, 
                   threat_actor: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search IOCs by type or threat actor
        
        Args:
            ioc_type: Type of IOC (ip, domain, hash, etc.)
            threat_actor: Associated threat actor
            
        Returns:
            List of matching IOCs
        """
        results = self.iocs
        
        if ioc_type:
            results = [ioc for ioc in results if ioc.get('type') == ioc_type]
        
        if threat_actor:
            results = [ioc for ioc in results if ioc.get('threat_actor') == threat_actor]
        
        return results
    
    def get_threat_landscape_summary(self) -> Dict[str, Any]:
        """
        Generate a threat landscape summary
        
        Returns:
            Summary dictionary with statistics
        """
        summary = {
            'total_threat_actors': len(self.threat_actors),
            'by_type': {},
            'critical_actors': [],
            'top_techniques': [],
            'total_iocs': len(self.iocs)
        }
        
        # Count by type
        for actor in self.threat_actors.values():
            actor_type = actor['type']
            summary['by_type'][actor_type] = summary['by_type'].get(actor_type, 0) + 1
            
            # Track critical actors
            if actor['severity'] == 'Critical':
                summary['critical_actors'].append(actor['name'])
        
        # Aggregate techniques
        all_techniques = []
        for actor in self.threat_actors.values():
            all_techniques.extend(actor.get('mitre_techniques', []))
        
        from collections import Counter
        technique_counts = Counter(all_techniques)
        summary['top_techniques'] = [
            {'technique': tech, 'count': count}
            for tech, count in technique_counts.most_common(10)
        ]
        
        return summary
    
    def export_threat_actors(self, file_path: str):
        """Export threat actors to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.threat_actors, f, indent=2)
        logger.info(f"Exported {len(self.threat_actors)} threat actors to {file_path}")


def main():
    """Main function for testing"""
    ti = ThreatIntelligence(config={})
    
    # List threat actors by type
    print("=== Cybercriminal Groups ===")
    for actor in ti.list_threat_actors(actor_type='Cybercriminal'):
        print(f"{actor['name']}: {actor['motivation']}")
    
    print("\n=== Nation-State Actors ===")
    for actor in ti.list_threat_actors(actor_type='Nation-State'):
        print(f"{actor['name']}: {actor['motivation']}")
    
    # Get threat landscape summary
    print("\n=== Threat Landscape Summary ===")
    summary = ti.get_threat_landscape_summary()
    print(json.dumps(summary, indent=2))
    
    # Export threat actors
    ti.export_threat_actors('config/threat_actors.json')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
