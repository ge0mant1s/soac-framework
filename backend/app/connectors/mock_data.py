
"""
Mock Data Generator for Testing
Generates realistic test events for different device types
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid


class MockDataGenerator:
    """Generate mock security events for testing"""
    
    # Sample data pools
    USERS = [
        "john.doe@straumann.com",
        "jane.smith@straumann.com",
        "bob.wilson@straumann.com",
        "alice.johnson@straumann.com",
        "mike.brown@straumann.com",
        "sarah.davis@straumann.com",
        "admin@straumann.com",
        "service.account@straumann.com"
    ]
    
    IPS = [
        "192.168.1.10", "192.168.1.25", "10.0.1.50", "10.0.2.100",
        "172.16.0.10", "185.45.67.89", "203.113.45.22", "91.198.174.192"
    ]
    
    EXTERNAL_IPS = [
        "185.45.67.89", "203.113.45.22", "91.198.174.192", 
        "104.28.16.10", "142.250.185.46", "52.96.136.42"
    ]
    
    COUNTRIES = ["Switzerland", "Germany", "United States", "France", "United Kingdom"]
    
    APPLICATIONS = [
        "Microsoft 365", "Microsoft Teams", "Office 365 SharePoint Online",
        "Exchange Online", "Azure Portal", "Power BI", "OneDrive"
    ]
    
    THREAT_TYPES = [
        "virus", "spyware", "vulnerability", "url-filtering",
        "wildfire", "data-filtering", "file-blocking"
    ]
    
    THREAT_NAMES = [
        "Suspicious PowerShell Command",
        "Malicious File Download",
        "SQL Injection Attempt",
        "XSS Attack",
        "Brute Force Attack",
        "Port Scan Detected",
        "Data Exfiltration Attempt"
    ]
    
    @staticmethod
    def generate_entraid_events(count: int = 10, hours_back: int = 24) -> List[Dict[str, Any]]:
        """Generate mock Entra ID authentication events"""
        events = []
        
        for i in range(count):
            timestamp = datetime.utcnow() - timedelta(
                hours=random.uniform(0, hours_back),
                minutes=random.randint(0, 59)
            )
            
            # 80% success, 20% failures
            is_success = random.random() < 0.8
            user = random.choice(MockDataGenerator.USERS)
            ip = random.choice(MockDataGenerator.IPS)
            
            # Some events from external IPs
            if random.random() < 0.2:
                ip = random.choice(MockDataGenerator.EXTERNAL_IPS)
            
            event = {
                "id": str(uuid.uuid4()),
                "createdDateTime": timestamp.isoformat() + "Z",
                "userPrincipalName": user,
                "userId": str(uuid.uuid4()),
                "appDisplayName": random.choice(MockDataGenerator.APPLICATIONS),
                "ipAddress": ip,
                "location": {
                    "city": random.choice(["Zurich", "Basel", "Geneva", "New York", "London"]),
                    "state": random.choice(["ZH", "BS", "GE", "NY", "GB"]),
                    "countryOrRegion": random.choice(MockDataGenerator.COUNTRIES)
                },
                "status": {
                    "errorCode": 0 if is_success else random.choice([50126, 50053, 50055, 50057]),
                    "failureReason": None if is_success else "Invalid username or password"
                },
                "deviceDetail": {
                    "deviceId": str(uuid.uuid4()) if random.random() < 0.8 else None,
                    "displayName": f"DESKTOP-{random.choice(['WIN', 'MAC', 'LIN'])}-{random.randint(1000, 9999)}",
                    "operatingSystem": random.choice(["Windows 11", "macOS", "iOS", "Android"]),
                    "browser": random.choice(["Edge", "Chrome", "Safari", "Firefox"]),
                    "trustType": random.choice(["Azure AD joined", "Hybrid Azure AD joined", ""])
                },
                "riskLevelDuringSignIn": random.choice(["none", "none", "none", "low", "medium"]),
                "conditionalAccessStatus": "success" if is_success else random.choice(["success", "failure"]),
                "clientAppUsed": random.choice(["Browser", "Mobile Apps and Desktop clients", "Exchange ActiveSync"])
            }
            
            events.append(event)
        
        return events
    
    @staticmethod
    def generate_paloalto_events(count: int = 10, hours_back: int = 24) -> List[Dict[str, Any]]:
        """Generate mock Palo Alto firewall events"""
        events = []
        
        for i in range(count):
            timestamp = datetime.utcnow() - timedelta(
                hours=random.uniform(0, hours_back),
                minutes=random.randint(0, 59)
            )
            
            src_ip = random.choice(MockDataGenerator.IPS)
            dst_ip = random.choice(MockDataGenerator.EXTERNAL_IPS)
            
            event_type = random.choice(["threat", "traffic", "url"])
            
            if event_type == "threat":
                event = {
                    "receive_time": timestamp.isoformat() + "Z",
                    "serial": "PA-VM-0123456789",
                    "type": "THREAT",
                    "subtype": random.choice(MockDataGenerator.THREAT_TYPES),
                    "time_generated": timestamp.isoformat() + "Z",
                    "src": src_ip,
                    "dst": dst_ip,
                    "natsrc": src_ip,
                    "natdst": dst_ip,
                    "rule": f"rule-{random.randint(1, 50)}",
                    "srcuser": random.choice(MockDataGenerator.USERS),
                    "dstuser": "",
                    "app": random.choice(["web-browsing", "ssl", "ms-update", "office365"]),
                    "vsys": "vsys1",
                    "from": "trust",
                    "to": "untrust",
                    "inbound_if": "ethernet1/1",
                    "outbound_if": "ethernet1/2",
                    "action": random.choice(["alert", "block", "allow"]),
                    "threatid": random.choice(MockDataGenerator.THREAT_NAMES),
                    "category": random.choice(["malware", "command-and-control", "phishing"]),
                    "severity": random.choice(["informational", "low", "medium", "high", "critical"]),
                    "direction": "client-to-server",
                    "seqno": str(random.randint(100000, 999999))
                }
            else:
                event = {
                    "receive_time": timestamp.isoformat() + "Z",
                    "serial": "PA-VM-0123456789",
                    "type": "TRAFFIC",
                    "subtype": random.choice(["start", "end"]),
                    "time_generated": timestamp.isoformat() + "Z",
                    "src": src_ip,
                    "dst": dst_ip,
                    "natsrc": src_ip,
                    "natdst": dst_ip,
                    "rule": f"rule-{random.randint(1, 50)}",
                    "srcuser": random.choice(MockDataGenerator.USERS),
                    "dstuser": "",
                    "app": random.choice(["web-browsing", "ssl", "ms-update", "office365"]),
                    "vsys": "vsys1",
                    "from": "trust",
                    "to": "untrust",
                    "inbound_if": "ethernet1/1",
                    "outbound_if": "ethernet1/2",
                    "action": random.choice(["allow", "deny"]),
                    "bytes": random.randint(1000, 1000000),
                    "bytes_sent": random.randint(500, 50000),
                    "bytes_received": random.randint(500, 950000),
                    "packets": random.randint(10, 1000),
                    "proto": random.choice(["tcp", "udp", "icmp"]),
                    "sport": random.randint(1024, 65535),
                    "dport": random.choice([80, 443, 8080, 3389, 22, 21])
                }
            
            events.append(event)
        
        return events
    
    @staticmethod
    def generate_siem_events(count: int = 10, hours_back: int = 24) -> List[Dict[str, Any]]:
        """Generate mock SIEM events"""
        events = []
        
        event_types = ["security_alert", "system_event", "network_event", "authentication"]
        
        for i in range(count):
            timestamp = datetime.utcnow() - timedelta(
                hours=random.uniform(0, hours_back),
                minutes=random.randint(0, 59)
            )
            
            event = {
                "@timestamp": timestamp.isoformat() + "Z",
                "event_type": random.choice(event_types),
                "host": f"host-{random.randint(1, 100)}",
                "source": random.choice(["windows", "linux", "network", "cloud"]),
                "severity": random.choice(["info", "low", "medium", "high", "critical"]),
                "user": random.choice(MockDataGenerator.USERS),
                "source_ip": random.choice(MockDataGenerator.IPS),
                "destination_ip": random.choice(MockDataGenerator.EXTERNAL_IPS),
                "message": random.choice([
                    "Suspicious process execution detected",
                    "Unauthorized access attempt",
                    "Configuration change detected",
                    "High volume of failed login attempts",
                    "Suspicious network connection",
                    "File integrity check failed"
                ]),
                "tags": random.sample(["security", "compliance", "threat", "anomaly"], k=2),
                "source_system": random.choice(["Splunk", "Elasticsearch", "QRadar"])
            }
            
            events.append(event)
        
        return events
