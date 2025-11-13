
"""
Initialize database with sample data
"""
import sys
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import User, Device, Rule, Incident, PlaybookExecution
from .auth import get_password_hash
from datetime import datetime, timedelta
import uuid


def init_db():
    """Initialize database with sample data"""
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create admin user
        print("Creating admin user...")
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@soac.local",
                password_hash=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            print("✓ Admin user created (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")
        
        # Create sample analyst user
        analyst_user = db.query(User).filter(User.username == "analyst").first()
        if not analyst_user:
            analyst_user = User(
                username="analyst",
                email="analyst@soac.local",
                password_hash=get_password_hash("analyst123"),
                role="analyst",
                is_active=True
            )
            db.add(analyst_user)
            print("✓ Analyst user created (username: analyst, password: analyst123)")
        
        db.commit()
        
        # Create sample devices
        print("\nCreating sample devices...")
        
        # PaloAlto NGFW devices
        paloalto_devices = [
            {
                "name": "PaloAlto NGFW - Main Firewall",
                "type": "paloalto",
                "config": {
                    "api_url": "https://firewall-main.company.com/api",
                    "api_key": "LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBOWl6TGM9bXcwM3JHUGVhRlNiY0dCR0srNnB4Zz09",
                    "verify_ssl": True,
                    "timeout": 30
                },
                "connection_status": "connected",
                "last_tested": datetime.utcnow() - timedelta(minutes=5)
            },
            {
                "name": "PaloAlto NGFW - Regional Firewall",
                "type": "paloalto",
                "config": {
                    "api_url": "https://firewall-regional.company.com/api",
                    "api_key": "REGIONAL123456789ABCDEF",
                    "verify_ssl": True,
                    "timeout": 30
                },
                "connection_status": "connected",
                "last_tested": datetime.utcnow() - timedelta(minutes=10)
            }
        ]
        
        # EntraID devices
        entraid_devices = [
            {
                "name": "Microsoft EntraID - Primary Tenant",
                "type": "entraid",
                "config": {
                    "tenant_id": "12345678-1234-1234-1234-123456789abc",
                    "client_id": "87654321-4321-4321-4321-cba987654321",
                    "client_secret": "EntraIDSecretKey12345",
                    "graph_api_endpoint": "https://graph.microsoft.com/v1.0"
                },
                "connection_status": "connected",
                "last_tested": datetime.utcnow() - timedelta(minutes=3)
            },
            {
                "name": "Microsoft EntraID - Dev Tenant",
                "type": "entraid",
                "config": {
                    "tenant_id": "aaaabbbb-cccc-dddd-eeee-ffff00001111",
                    "client_id": "11112222-3333-4444-5555-666677778888",
                    "client_secret": "DevTenantSecret",
                    "graph_api_endpoint": "https://graph.microsoft.com/v1.0"
                },
                "connection_status": "disconnected",
                "last_tested": datetime.utcnow() - timedelta(hours=2)
            }
        ]
        
        # SIEM devices
        siem_devices = [
            {
                "name": "Elastic SIEM - Production",
                "type": "siem",
                "config": {
                    "api_url": "https://siem.company.com:9200",
                    "username": "elastic",
                    "password": "elastic_password",
                    "index_pattern": "logs-*",
                    "verify_ssl": True
                },
                "connection_status": "connected",
                "last_tested": datetime.utcnow() - timedelta(minutes=1)
            },
            {
                "name": "Splunk SIEM - Secondary",
                "type": "siem",
                "config": {
                    "api_url": "https://splunk.company.com:8089",
                    "username": "admin",
                    "password": "splunk_password",
                    "search_head": "splunk-sh-01"
                },
                "connection_status": "error",
                "last_tested": datetime.utcnow() - timedelta(hours=1)
            }
        ]
        
        all_devices = paloalto_devices + entraid_devices + siem_devices
        
        for device_data in all_devices:
            existing_device = db.query(Device).filter(Device.name == device_data["name"]).first()
            if not existing_device:
                device = Device(**device_data)
                db.add(device)
                print(f"✓ Created device: {device_data['name']}")
        
        db.commit()
        
        # Create sample rules
        print("\nCreating sample rules...")
        
        # Get devices for rule creation
        paloalto_device = db.query(Device).filter(Device.type == "paloalto").first()
        entraid_device = db.query(Device).filter(Device.type == "entraid").first()
        siem_device = db.query(Device).filter(Device.type == "siem").first()
        
        # Sample EntraID rules
        entraid_rules = [
            {
                "id": "ENTRAID-001",
                "device_id": entraid_device.id,
                "use_case_id": "UC-005-INTRUSION",
                "name": "Brute Force Detection",
                "description": "Many authentication failures per account (possible brute-force or credential stuffing)",
                "incident_rule": "Burst from same IP and subsequent success; correlate with Umbrella/PAN EDR",
                "severity": "High",
                "mitre_tactic": "Credential Access",
                "mitre_technique": "T1110",
                "category": "Account Abuse",
                "query": "#event.module=entraid | event.dataset = entraid.signin | event.outcome = failure",
                "enabled": True,
                "status": "active",
                "detection_count": 127
            },
            {
                "id": "ENTRAID-002",
                "device_id": entraid_device.id,
                "use_case_id": "UC-005-INTRUSION",
                "name": "Password Spraying Detection",
                "description": "One IP failing across many users (password spraying)",
                "incident_rule": "≥10 users and ≥30 total fails from one IP in a window",
                "severity": "High",
                "mitre_tactic": "Credential Access",
                "mitre_technique": "T1110.003",
                "category": "Account Abuse",
                "query": "#event.module=entraid | event.dataset = entraid.signin | event.outcome = failure",
                "enabled": True,
                "status": "active",
                "detection_count": 89
            },
            {
                "id": "ENTRAID-003",
                "device_id": entraid_device.id,
                "use_case_id": "UC-005-INTRUSION",
                "name": "Geo-Velocity Anomaly",
                "description": "User signs in from multiple countries too quickly (geo-velocity)",
                "incident_rule": "Two or more distinct countries for the same user in a short time window",
                "severity": "High",
                "mitre_tactic": "Credential Access",
                "mitre_technique": "T1110",
                "category": "Geo Anomaly",
                "query": "#event.module=entraid | event.dataset = entraid.signin | event.outcome = success",
                "enabled": True,
                "status": "active",
                "detection_count": 34
            }
        ]
        
        # Sample PaloAlto rules
        paloalto_rules = [
            {
                "id": "PALOALTO-001",
                "device_id": paloalto_device.id,
                "use_case_id": "UC-005-INTRUSION",
                "name": "C2 Beaconing Detection",
                "description": "Hosts repeatedly connecting to the same external IP (possible beaconing/C2)",
                "incident_rule": "Pattern sustained across multiple hosts or windows; verify with EDR/DNS intel",
                "severity": "High",
                "mitre_tactic": "Command and Control",
                "mitre_technique": "T1071.001",
                "category": "Beaconing",
                "query": "#repo = paloalto | event.panw.panos.action = allow",
                "enabled": True,
                "status": "active",
                "detection_count": 45
            },
            {
                "id": "PALOALTO-002",
                "device_id": paloalto_device.id,
                "use_case_id": "UC-002-DATA-THEFT",
                "name": "Data Exfiltration Detection",
                "description": "Large outbound bytes to the same external ASN or domain group (exfiltration risk)",
                "incident_rule": ">= 1 GB to non-corporate ASN or many destinations; align with DLP alerts",
                "severity": "High",
                "mitre_tactic": "Exfiltration",
                "mitre_technique": "T1041",
                "category": "Data Exfiltration",
                "query": "#repo = paloalto | event.panw.panos.action = allow",
                "enabled": True,
                "status": "active",
                "detection_count": 23
            },
            {
                "id": "PALOALTO-003",
                "device_id": paloalto_device.id,
                "use_case_id": "UC-006-MALWARE",
                "name": "Malware Traffic Detection",
                "description": "Application characteristics include 'used-by-malware' but traffic is allowed",
                "incident_rule": "Multiple sources or large byte totals; correlate with endpoint alerts",
                "severity": "High",
                "mitre_tactic": "Command and Control",
                "mitre_technique": "T1071",
                "category": "Malicious App Traits",
                "query": "#repo = paloalto | event.panw.panos.action = allow",
                "enabled": True,
                "status": "active",
                "detection_count": 67
            }
        ]
        
        # Sample SIEM rules
        siem_rules = [
            {
                "id": "SIEM-001",
                "device_id": siem_device.id,
                "use_case_id": "UC-006-MALWARE",
                "name": "Suspicious Process Execution",
                "description": "Detection of suspicious process execution patterns",
                "incident_rule": "Multiple occurrences across different hosts",
                "severity": "Medium",
                "mitre_tactic": "Execution",
                "mitre_technique": "T1059",
                "category": "Process Execution",
                "query": "event.category:process AND event.type:start",
                "enabled": True,
                "status": "active",
                "detection_count": 156
            },
            {
                "id": "SIEM-002",
                "device_id": siem_device.id,
                "use_case_id": "UC-005-INTRUSION",
                "name": "Lateral Movement Detection",
                "description": "Detection of potential lateral movement activities",
                "incident_rule": "Remote service connections from suspicious sources",
                "severity": "High",
                "mitre_tactic": "Lateral Movement",
                "mitre_technique": "T1021",
                "category": "Lateral Movement",
                "query": "event.category:network AND event.action:connection",
                "enabled": True,
                "status": "testing",
                "detection_count": 78
            }
        ]
        
        all_rules = entraid_rules + paloalto_rules + siem_rules
        
        for rule_data in all_rules:
            existing_rule = db.query(Rule).filter(Rule.id == rule_data["id"]).first()
            if not existing_rule:
                rule = Rule(**rule_data)
                db.add(rule)
                print(f"✓ Created rule: {rule_data['id']} - {rule_data['name']}")
        
        db.commit()
        
        # Create sample incidents
        print("\nCreating sample incidents...")
        
        sample_incidents = [
            {
                "incident_id": "INC-IN1-20251113090000",
                "pattern_id": "IN1",
                "pattern_name": "Intrusion Chain",
                "entity_key": "user:jdoe|computer:DESKTOP-001",
                "phases_matched": ["Initial Access", "Credential Access", "Lateral Movement"],
                "confidence_level": "High",
                "event_count": 12,
                "events": [],
                "severity": "High",
                "status": "investigating",
                "assigned_to": "analyst@soac.local"
            },
            {
                "incident_id": "INC-D1-20251113080000",
                "pattern_id": "D1",
                "pattern_name": "Data Exfiltration",
                "entity_key": "user:asmith|computer:LAPTOP-042",
                "phases_matched": ["Collection", "Exfiltration"],
                "confidence_level": "Medium",
                "event_count": 8,
                "events": [],
                "severity": "Medium",
                "status": "open",
                "assigned_to": None
            },
            {
                "incident_id": "INC-R1-20251112150000",
                "pattern_id": "R1",
                "pattern_name": "Ransomware Chain",
                "entity_key": "user:system|computer:SERVER-005",
                "phases_matched": ["Initial Access", "Execution", "Impact"],
                "confidence_level": "Critical",
                "event_count": 15,
                "events": [],
                "severity": "Critical",
                "status": "contained",
                "assigned_to": "admin@soac.local"
            }
        ]
        
        for incident_data in sample_incidents:
            existing_incident = db.query(Incident).filter(
                Incident.incident_id == incident_data["incident_id"]
            ).first()
            if not existing_incident:
                incident = Incident(**incident_data)
                db.add(incident)
                print(f"✓ Created incident: {incident_data['incident_id']}")
        
        db.commit()
        
        # Create sample playbook executions
        print("\nCreating sample playbook executions...")
        
        sample_executions = [
            {
                "execution_id": "EXEC-PB-R1-001",
                "incident_id": "INC-R1-20251112150000",
                "playbook_id": "PB-R1-RANSOMWARE",
                "playbook_name": "Ransomware Containment and Recovery",
                "status": "completed",
                "steps_completed": 5,
                "steps_total": 5,
                "start_time": datetime.utcnow() - timedelta(hours=2),
                "end_time": datetime.utcnow() - timedelta(hours=1, minutes=57)
            }
        ]
        
        for execution_data in sample_executions:
            existing_execution = db.query(PlaybookExecution).filter(
                PlaybookExecution.execution_id == execution_data["execution_id"]
            ).first()
            if not existing_execution:
                execution = PlaybookExecution(**execution_data)
                db.add(execution)
                print(f"✓ Created playbook execution: {execution_data['execution_id']}")
        
        db.commit()
        
        print("\n" + "="*60)
        print("✅ Database initialized successfully!")
        print("="*60)
        print("\nDefault credentials:")
        print("  Admin: username=admin, password=admin123")
        print("  Analyst: username=analyst, password=analyst123")
        print("\nSample data created:")
        print(f"  - Users: 2")
        print(f"  - Devices: {len(all_devices)}")
        print(f"  - Rules: {len(all_rules)}")
        print(f"  - Incidents: {len(sample_incidents)}")
        print(f"  - Playbook Executions: {len(sample_executions)}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
