# Threat Landscape

## Overview

This document provides comprehensive threat intelligence for the SOaC Framework, including threat actor profiles, motivations, tactics, techniques, and procedures (TTPs).

---

## Tracked Threat Actors

### Cybercriminal Groups

#### 1. LockBit

**Type**: Cybercriminal Syndicate  
**Geography**: Global  
**Severity**: ★★★★★ (Critical)

**Motivation**: Purely financial - ransomware-as-a-service (RaaS) operator

**Techniques & Tactics**:
- Double and triple extortion
- Lateral movement using RDP, PSExec
- Use of automation for faster encryption

**Impact**: Encryption of critical systems, threatening operations

**MITRE Tactics**: Initial Access, Execution, Lateral Movement, Impact  
**MITRE Techniques**: T1486, T1021.001, T1059

---

#### 2. Clop

**Type**: Cybercriminal Group  
**Geography**: Global  
**Severity**: ★★★★☆ (High)

**Motivation**: Financial (data exfiltration/extortion campaigns)

**Techniques & Tactics**:
- Targeting of MOVEit and other managed file transfer systems
- Data leak extortion websites

**Impact**: Massive data exposure of sensitive records

**MITRE Tactics**: Initial Access, Collection, Exfiltration  
**MITRE Techniques**: T1190, T1005, T1567

---

#### 3. FIN12

**Type**: Cybercriminal Group  
**Geography**: Global  
**Severity**: ★★★☆☆ (Medium-High)

**Motivation**: Healthcare-focused ransomware deployment

**Techniques & Tactics**:
- Fast deployment of malware post-access
- Prefers high-value targets with low tolerance for downtime

**Impact**: Attacks on critical infrastructure; urgent ransom demands

**MITRE Tactics**: Execution, Persistence, Impact  
**MITRE Techniques**: T1486, T1059, T1053

---

### Nation-State Actors

#### 4. APT29 (Cozy Bear)

**Type**: Nation-State (Russia)  
**Geography**: Russia  
**Severity**: ★★★☆☆ (High)

**Motivation**: Espionage; known to target healthcare and pharmaceutical sectors

**Techniques & Tactics**:
- Spear-phishing for credential access
- Supply chain exploitation
- Stealthy persistence (e.g., WellMess, WellMail)

**Impact**: Theft of research data, surveillance on health policy strategies

**MITRE Tactics**: Initial Access, Execution, Persistence, Collection  
**MITRE Techniques**: T1566.001, T1195, T1059, T1005

---

#### 5. APT41

**Type**: Nation-State (China)  
**Geography**: China  
**Severity**: ★★★☆☆ (High)

**Motivation**: IP theft for state-sponsored industrial gain; hybrid criminal-political activity

**Techniques & Tactics**:
- Web shell deployments
- Exploiting VPN and Citrix vulnerabilities
- Living-off-the-land tactics

**Impact**: Exfiltration of device schematics, medical AI models, datasets

**MITRE Tactics**: Initial Access, Persistence, Privilege Escalation, Collection  
**MITRE Techniques**: T1190, T1505.003, T1068, T1005

---

#### 6. Lazarus Group

**Type**: Nation-State (North Korea)  
**Geography**: North Korea  
**Severity**: ★★★☆☆ (Critical)

**Motivation**: Financial theft, sabotage, geopolitical disruption

**Techniques & Tactics**:
- Custom ransomware (e.g., WannaCry)
- Banking Trojan delivery
- Attacks on pharmaceutical payment systems

**Impact**: Major ransomware campaigns impacting critical infrastructure

**MITRE Tactics**: Initial Access, Execution, Impact  
**MITRE Techniques**: T1486, T1204, T1499

---

### Hacktivists

#### 7. KillNet / Anonymous

**Type**: Hacktivist Group  
**Geography**: Global  
**Severity**: ★★★☆☆ (Medium)

**Motivation**: Ideologically driven, especially around geopolitical health policies

**Techniques & Tactics**:
- DDoS attacks on critical portals
- Website defacement
- Public data exposure via Telegram or dark web

**Impact**: Operational disruption, reputation damage, misinformation campaigns

**MITRE Tactics**: Impact, Collection, Exfiltration  
**MITRE Techniques**: T1499, T1005, T1567

---

#### 8. GhostSec

**Type**: Hacktivist / Vigilante  
**Geography**: Global  
**Severity**: ★★☆☆☆ (Medium)

**Motivation**: Political or anti-corporate messaging

**Techniques & Tactics**:
- Data doxxing
- Exploiting misconfigured cloud services

**Impact**: Public image threats, leaking of research datasets

**MITRE Tactics**: Collection, Exfiltration  
**MITRE Techniques**: T1530, T1567

---

### Insider Threats

#### 9. Malicious Insider

**Type**: Insider Threat  
**Geography**: Global  
**Severity**: ★★★☆☆ (High)

**Motivation**: Personal gain (selling data, credentials), ideological motives, human error

**Techniques & Tactics**:
- Unauthorized database queries
- USB malware introduction
- Policy circumvention or phishing propagation

**Impact**: Credential compromise, data leakage, unauthorized IP access

**MITRE Tactics**: Collection, Exfiltration, Impact  
**MITRE Techniques**: T1005, T1052, T1567

---

### Supply Chain Adversaries

#### 10. UNC Groups (e.g., UNC2447, UNC3944)

**Type**: Supply Chain Adversary  
**Geography**: Global  
**Severity**: ★★★☆☆ (High)

**Motivation**: Targeting via trusted vendors

**Techniques & Tactics**:
- Exploiting vulnerabilities in widely-used medical platforms
- Tainted patches or SDKs

**Impact**: Backdoor access via signed components, affecting device integrity and compliance

**MITRE Tactics**: Initial Access, Persistence, Defense Evasion  
**MITRE Techniques**: T1195, T1078, T1036

---

## MITRE ATT&CK Techniques to Monitor

### Initial Access

- Drive-by Compromise
- Exploit Public-Facing Application
- Phishing, Supply Chain Compromise
- Valid Accounts
- Trusted Relationship

### Execution

- Cloud Administration Command
- Command and Scripting Interpreter
- Container Administration Command
- Windows Management Instrumentation
- Exploitation for Client Execution

### Persistence

- Cloud Application Integration
- Create Account
- Modify Registry
- Scheduled Task/Job
- Access Token Manipulation

### Privilege Escalation

- Abuse Elevation Control Mechanism
- Escape to Host
- Process Injection
- Access Token Manipulation

### Defense Evasion

- Exploitation for Defense Evasion
- Deobfuscate/Decode Files or Information
- Virtualization/Sandbox Evasion

### Credential Access

- Exploitation for Credential Access
- Unsecured Credentials
- Steal or Forge Kerberos Tickets
- Input Capture

### Discovery

- Cloud Service Discovery
- Container and Resource Discovery
- Network Service Discovery
- Network Sniffing
- Remote System Discovery

### Lateral Movement

- Exploitation of Remote Services
- Remote Services
- Software Deployment Tools
- Lateral Tool Transfer

### Collection

- Data from Cloud Storage
- Data from Configuration Repository
- Data from Information Repositories
- Data from Local System
- Data from Network Shared Drive
- Data from Removable Media

### Impact

- Data Encrypted for Impact
- Data Destruction
- Service Stop
- Financial Theft
- Theft of Operational Information

---

## Detection and Mitigation Matrix

| Use Case | Mitigation Devices / Systems | Detection Devices / Systems |
|----------|----------------------------|---------------------------|
| Ransomware | Backup Appliances (immutable), NGFW, Network Segmentation | EDR, SIEM, File Integrity Monitoring, Network TAPs |
| Data Theft | DLP Gateways, Rights Management Services | DLP, CASB, SIEM, Cloud Logging Agents |
| DoS | DDoS Protection Gateways, Load Balancers | NIDS/NIPS, WAF Logs, Performance Monitors |
| Supply Chain | Secure Code Signing Infrastructure, Application Control | Code Repo Monitors, DevOps Audit Logs, SBOM Validators |
| Intrusion | MFA Appliances, Firewalls, Deception Systems | SIEM, EDR, Network Sensor, PAM Logging |
| Malware | Application Whitelisting, Network Isolation, USB Control | Antivirus, EDR, Sandboxes, Network Threat Analytics |
| Misconfiguration | Configuration Management Systems, Access Policy Engines | CSPM, CWPP, Vulnerability Scanners, SIEM |
| Social Engineering | MFA Devices, Phishing Simulators, Conditional Access | Email Gateways, UEBA, Identity Providers, SIEM |
| Info Manipulation | Immutable Storage Devices, Workflow Automation | Log Monitoring Tools, Database Activity Monitors |
| Financial Fraud | Transaction Authorization Systems, Geofencing, Secure Finance Appliances | ERP Audit Logs, SOAR, Fraud Detection AI Models |

---

**SOaC Framework Team** | Version 1.0.0
