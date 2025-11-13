
"""
Use Case Manager - Manage security use cases and their lifecycle
Implements the MAGMA framework for use case management
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json

logger = logging.getLogger(__name__)


class UseCaseStatus(Enum):
    """Use case lifecycle statuses"""
    DRAFT = "draft"
    TESTING = "testing"
    ACTIVE = "active"
    TUNING = "tuning"
    RETIRED = "retired"


class UseCaseManager:
    """
    Manage security use cases throughout their lifecycle
    Based on the MAGMA framework:
    - Mission: Strategic goals
    - Activity: Cyber threat types
    - Goals: Detection & protection goals
    - Mitigation: Tools and controls
    - Actions: Implementation tasks
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the use case manager
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.use_cases = {}
        self._load_default_use_cases()
        logger.info("Use Case Manager initialized")
    
    def _load_default_use_cases(self):
        """Load default use cases from the SOaC Framework"""
        default_use_cases = [
            {
                'id': 'UC-001-RANSOMWARE',
                'title': 'Ransomware Detection and Response',
                'mission': 'Ensure continuity of services and data access',
                'activity': 'Encryption of files, backup deletion, extortion',
                'goals': [
                    'Detect ransomware encryption tools',
                    'Detect backup modification commands',
                    'Detect lateral movement'
                ],
                'mitigation': ['EDR', 'Immutable backups', 'Network segmentation'],
                'mitre_techniques': ['T1486', 'T1059.001', 'T1027'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'Critical',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-002-DATA-THEFT',
                'title': 'Attack Against Data / Exfiltration',
                'mission': 'Protect sensitive data against exfiltration',
                'activity': 'Data harvesting, cloud exfiltration, USB copying',
                'goals': [
                    'Detect rclone, aws s3 cp usage',
                    'Monitor access to confidential folders'
                ],
                'mitigation': ['DLP', 'CASB', 'CloudTrail', 'Audit Logs'],
                'mitre_techniques': ['T1567.002', 'T1005'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'High',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-003-DOS',
                'title': 'Denial of Service',
                'mission': 'Maintain uptime of critical services',
                'activity': 'Application or volumetric DoS',
                'goals': [
                    'Detect HTTP 503/504 spikes',
                    'Detect UDP/SYN floods'
                ],
                'mitigation': ['WAF', 'Cloud-based DDoS protection'],
                'mitre_techniques': ['T1499'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'High',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-004-SUPPLY-CHAIN',
                'title': 'Supply Chain Attack',
                'mission': 'Secure 3rd party software and code dependencies',
                'activity': 'Malicious package deployment, code tampering',
                'goals': [
                    'Detect installs from unverified repos',
                    'Detect tampering with system binaries'
                ],
                'mitigation': ['SBOM', 'SCA', 'EDR file integrity'],
                'mitre_techniques': ['T1195.002'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'High',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-005-INTRUSION',
                'title': 'Intrusion Detection',
                'mission': 'Prevent unauthorized access to infrastructure',
                'activity': 'Lateral movement, password reuse, exploit usage',
                'goals': [
                    'Detect PsExec/WMI calls',
                    'Detect brute-force or spray attacks'
                ],
                'mitigation': ['MFA', 'Network segmentation', 'PAM'],
                'mitre_techniques': ['T1021.001'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'Critical',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-006-MALWARE',
                'title': 'Malware Detection',
                'mission': 'Detect and remove malicious implants before impact',
                'activity': 'Initial infection, obfuscation, payload deployment',
                'goals': [
                    'Detect registry run keys',
                    'Detect code injection attempts'
                ],
                'mitigation': ['EDR', 'Application Control'],
                'mitre_techniques': ['T1055.001'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'High',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-007-MISCONFIGURATION',
                'title': 'Misconfiguration / Poor Security',
                'mission': 'Minimize human error and weak settings',
                'activity': 'Public S3 buckets, admin rights abuse, no MFA',
                'goals': [
                    'Detect world-writable shares',
                    'Alert on excessive admin rights granted'
                ],
                'mitigation': ['CSPM', 'GPO auditing', 'Least privilege policies'],
                'mitre_techniques': ['T1552', 'T1078.003'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'Medium',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-008-SOCIAL-ENGINEERING',
                'title': 'Social Engineering',
                'mission': 'Protect users from phishing, spoofing, and trickery',
                'activity': 'Email spoofing, MFA fatigue, fake login portals',
                'goals': [
                    'Detect lookalike domains and QR phishing',
                    'Alert on multiple MFA denies'
                ],
                'mitigation': ['Email security gateway', 'Adaptive MFA'],
                'mitre_techniques': ['T1566.002', 'T1110.003'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'High',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-009-INFO-MANIPULATION',
                'title': 'Information Manipulation',
                'mission': 'Ensure trust in records',
                'activity': 'Tampering with logs, reports, clinical data',
                'goals': [
                    'Detect deletion of audit logs',
                    'Detect unauthorized report generation'
                ],
                'mitigation': ['Immutable storage', 'FIM', 'Approval workflows'],
                'mitre_techniques': ['T1565.001', 'T1557'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'Medium',
                'owner': 'SOaC Framework Team'
            },
            {
                'id': 'UC-010-FINANCIAL-FRAUD',
                'title': 'Financial Theft & Fraud',
                'mission': 'Prevent unauthorized access to funds or billing',
                'activity': 'Payroll rerouting, wire fraud, invoice tampering',
                'goals': [
                    'Detect off-hours ERP transactions',
                    'Alert on bank account changes + transfers'
                ],
                'mitigation': ['Transaction fraud monitoring', 'Dual authorization'],
                'mitre_techniques': ['T1110', 'T1589.002', 'T1539'],
                'status': UseCaseStatus.ACTIVE,
                'severity': 'Critical',
                'owner': 'SOaC Framework Team'
            }
        ]
        
        for uc in default_use_cases:
            uc['created_date'] = datetime.now().isoformat()
            uc['last_updated'] = datetime.now().isoformat()
            uc['review_frequency'] = 'Monthly'
            self.use_cases[uc['id']] = uc
    
    def get_use_case(self, use_case_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific use case by ID"""
        return self.use_cases.get(use_case_id)
    
    def list_use_cases(self, status: Optional[UseCaseStatus] = None) -> List[Dict[str, Any]]:
        """
        List all use cases, optionally filtered by status
        
        Args:
            status: Filter by use case status
            
        Returns:
            List of use cases
        """
        if status:
            return [uc for uc in self.use_cases.values() if uc['status'] == status]
        return list(self.use_cases.values())
    
    def update_use_case_status(self, use_case_id: str, new_status: UseCaseStatus):
        """Update the status of a use case"""
        if use_case_id in self.use_cases:
            self.use_cases[use_case_id]['status'] = new_status
            self.use_cases[use_case_id]['last_updated'] = datetime.now().isoformat()
            logger.info(f"Use case {use_case_id} status updated to {new_status.value}")
        else:
            logger.error(f"Use case {use_case_id} not found")
    
    def get_coverage_report(self) -> Dict[str, Any]:
        """
        Generate a coverage report showing MITRE ATT&CK coverage
        
        Returns:
            Coverage report dictionary
        """
        all_techniques = []
        for uc in self.use_cases.values():
            all_techniques.extend(uc.get('mitre_techniques', []))
        
        unique_techniques = set(all_techniques)
        
        report = {
            'total_use_cases': len(self.use_cases),
            'active_use_cases': len([uc for uc in self.use_cases.values() if uc['status'] == UseCaseStatus.ACTIVE]),
            'unique_techniques_covered': len(unique_techniques),
            'techniques': list(unique_techniques),
            'coverage_by_severity': self._count_by_severity(),
            'coverage_by_status': self._count_by_status()
        }
        
        return report
    
    def _count_by_severity(self) -> Dict[str, int]:
        """Count use cases by severity"""
        severity_counts = {}
        for uc in self.use_cases.values():
            severity = uc.get('severity', 'Unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        return severity_counts
    
    def _count_by_status(self) -> Dict[str, int]:
        """Count use cases by status"""
        status_counts = {}
        for uc in self.use_cases.values():
            status = uc['status'].value
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def export_use_cases(self, file_path: str):
        """Export all use cases to a JSON file"""
        with open(file_path, 'w') as f:
            # Convert enum to string for JSON serialization
            export_data = {}
            for uc_id, uc in self.use_cases.items():
                uc_copy = uc.copy()
                uc_copy['status'] = uc_copy['status'].value
                export_data[uc_id] = uc_copy
            json.dump(export_data, f, indent=2)
        logger.info(f"Exported {len(self.use_cases)} use cases to {file_path}")


def main():
    """Main function for testing"""
    manager = UseCaseManager(config={})
    
    # List all use cases
    print("=== All Use Cases ===")
    for uc in manager.list_use_cases():
        print(f"{uc['id']}: {uc['title']} - {uc['status'].value}")
    
    # Generate coverage report
    print("\n=== Coverage Report ===")
    report = manager.get_coverage_report()
    print(json.dumps(report, indent=2))
    
    # Export use cases
    manager.export_use_cases('config/use_cases.json')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
