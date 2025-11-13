
# Use Case Management - MAGMA Framework

## Overview

This document structures the complete security use case library using the **MAGMA Framework**, ensuring alignment from strategic objectives to operational implementation across all 10 defined threat use cases.

## MAGMA Levels

| Layer | Description |
|-------|-------------|
| **M** - Mission | Strategic goals aligned with business and regulatory objectives |
| **A** - Activity | Specific cyber threat types and high-level categories |
| **G** - Goals | Detection & protection goals tied to adversarial behavior |
| **M** - Mitigation | Tools, processes, and controls to detect/prevent/respond |
| **A** - Actions | Engineering and operational tasks for implementation |

## MAGMA Framework Application

| Phase | Description |
|-------|-------------|
| **Mission** | Defend infrastructure against ransomware, exfiltration, fraud, and system integrity threats |
| **Activity** | Identify threat behaviors aligned to MITRE ATT&CK based on current threat intel |
| **Goals** | Ensure continuous detection, response, and visibility across endpoints, identity, cloud, network, and email |
| **Mitigation** | Operationalize response through SOAR, EDR, SIEM, DLP, and user training aligned to each detection |
| **Action** | Deploy, test, tune, review, and retire detection rules on a lifecycle basis |

---

## Use Case Lifecycle Phases

| Phase | Activities | Tools |
|-------|-----------|-------|
| 1. Initiation | Align with MAGMA strategy, identify threat scenarios, assess relevance via threat intel | Threat intel feeds, ATT&CK |
| 2. Design | Create SIGMA rules aligned to tactics, techniques, and actor behavior | YAML authoring, Git |
| 3. Testing | Validate detection efficacy using test datasets, red team, and malware emulation | Atomic Red Team, Sigma CLI |
| 4. Deployment | Convert to SIEM/EDR-native formats (KQL, CQL), apply to detection engines, create dashboards | Falcon, Sentinel, Splunk |
| 5. Operations | Monitor alerts, investigate incidents, tune rule thresholds | SIEM, SOAR, XDR Console |
| 6. Review | Analyze false positives, actor evasion trends, and use case coverage gaps every 30–90 days | Jupyter, Excel, Reporting |
| 7. Retirement | Decommission unused or obsolete use cases and archive documentation | Wiki, Confluence |

---

## Complete Use Case Breakdown

### 1. Ransomware

**Mission**: Ensure continuity of services and data access

**Activity**: Encryption of files, backup deletion, extortion

**Goals**:
- Detect ransomware encryption tools (e.g., LockBit, ALPHV)
- Detect backup modification commands (vssadmin, wbadmin)
- Detect lateral movement (PsExec, SMB)

**Mitigation**:
- EDR, Immutable backups, Network segmentation

**Actions**:
- Build YARA rules for ransomware variants
- Configure immutable backups in backup systems
- Deploy SIEM correlation for mass file renames

**MITRE Techniques**: T1486, T1059.001, T1027

---

### 2. Attack Against Data

**Mission**: Protect sensitive data against exfiltration

**Activity**: Data harvesting, cloud exfiltration, USB copying

**Goals**:
- Detect rclone, aws s3 cp usage
- Monitor access to confidential, research, or finance folders

**Mitigation**:
- DLP, CASB, CloudTrail, Audit Logs

**Actions**:
- Integrate with AWS CloudTrail
- Tag files with sensitivity labels in EDR
- Create alerts on downloads >100MB from sensitive buckets

**MITRE Techniques**: T1567.002, T1005

---

### 3. Denial of Service

**Mission**: Maintain uptime of critical services

**Activity**: Application or volumetric DoS

**Goals**:
- Detect HTTP 503/504 spikes
- Detect UDP/SYN floods

**Mitigation**:
- WAF, Cloud-based DDoS protection (Cloudflare, Akamai)

**Actions**:
- Deploy NetFlow/IPFIX analysis
- Set WAF rules for request thresholds
- Alert on >5000 req/min from same IP

**MITRE Techniques**: T1499

---

### 4. Supply Chain Attack

**Mission**: Secure 3rd party software and code dependencies

**Activity**: Malicious package deployment, code tampering

**Goals**:
- Detect installs from unverified repos
- Detect tampering with system binaries

**Mitigation**:
- SBOM, SCA (Software Composition Analysis), EDR file integrity

**Actions**:
- Enable code signing validation
- Monitor GitOps audit logs for CI/CD

**MITRE Techniques**: T1195.002

---

### 5. Intrusion

**Mission**: Prevent unauthorized access to infrastructure

**Activity**: Lateral movement, password reuse, exploit usage

**Goals**:
- Detect PsExec/WMI calls
- Detect brute-force or spray attacks

**Mitigation**:
- MFA, Network segmentation, PAM

**Actions**:
- Apply Falcon Identity Protection policies
- Tune SIEM rules on event 4625, 4624 anomalies

**MITRE Techniques**: T1021.001

---

### 6. Malware

**Mission**: Detect and remove malicious implants before impact

**Activity**: Initial infection, obfuscation, payload deployment

**Goals**:
- Detect registry run keys
- Detect code injection attempts

**Mitigation**:
- EDR, Application Control (AppLocker)

**Actions**:
- Write detection rules for reg.exe add into Run paths
- Enable memory scan modules in Falcon

**MITRE Techniques**: T1055.001

---

### 7. Misconfiguration / Poor Security

**Mission**: Minimize human error and weak settings

**Activity**: Public S3 buckets, admin rights abuse, no MFA

**Goals**:
- Detect world-writable shares
- Alert on excessive admin rights granted

**Mitigation**:
- CSPM, GPO auditing, Least privilege policies

**Actions**:
- Schedule daily CSPM misconfiguration scans
- Monitor AD group membership changes

**MITRE Techniques**: T1552, T1078.003

---

### 8. Social Engineering

**Mission**: Protect users from phishing, spoofing, and trickery

**Activity**: Email spoofing, MFA fatigue, fake login portals

**Goals**:
- Detect lookalike domains and QR phishing
- Alert on multiple MFA denies

**Mitigation**:
- Email security gateway, Adaptive MFA

**Actions**:
- Enable domain impersonation detection in Proofpoint
- Send monthly phishing simulations

**MITRE Techniques**: T1566.002, T1110.003

---

### 9. Information Manipulation

**Mission**: Ensure trust in records

**Activity**: Tampering with logs, reports, critical data

**Goals**:
- Detect deletion of audit logs
- Detect unauthorized report generation

**Mitigation**:
- Immutable storage, FIM, Approval workflows

**Actions**:
- Integrate FIM alerts into SIEM
- Create ACL rules for reporting platforms

**MITRE Techniques**: T1565.001, T1557

---

### 10. Financial Theft & Fraud

**Mission**: Prevent unauthorized access to funds or billing

**Activity**: Payroll rerouting, wire fraud, invoice tampering

**Goals**:
- Detect off-hours ERP transactions
- Alert on bank account changes + transfers

**Mitigation**:
- Transaction fraud monitoring, Dual authorization, Geofencing

**Actions**:
- Ingest ERP logs to SIEM
- Build correlation rule: bank_account + payment within 30 min

**MITRE Techniques**: T1110, T1589.002, T1539

---

## Tooling Stack for Implementation

**Authoring**: Sigma CLI, GitHub  
**Normalization**: Elastic Common Schema, Azure ASIM, CrowdStrike ECS  
**Conversion**: sigmac, Falcon Query Builder, Sentinel wizard  
**Validation**: Atomic Red Team, CALDERA ATT&CK Simulation  
**Deployment**: SIGMA Rules, Falcon IOA uploads, Azure Sentinel Rules API  
**Monitoring**: KQL/CQL dashboards, SOAR incident queues  
**Threat Intelligence**: MISP

---

## Use Case Register Fields

| Field | Description |
|-------|-------------|
| Use Case ID | Unique tag (e.g., UC-RANS-T1486) |
| Title | Descriptive title |
| MITRE ID | e.g. T1055.001, T1566.002 |
| Threat Actor(s) | LockBit, ALPHV, etc. |
| Detection Rule Type | SIGMA, CQL, KQL |
| Logging Required | EDR, AD, DNS, Email, Cloud |
| SIEM Platform | NGSIEM, Sentinel |
| Status | Draft / Active / Retired |
| Review Frequency | Monthly / Quarterly |
| Owner | Security Operations |
| Associated Playbook | SOAR/IR workflow if triggered |

---

## KPI Monitoring Dashboard

| Metric | Target |
|--------|--------|
| % of MITRE TTPs covered | > 85% |
| Mean Time to Detection (MTTD) | < 10 minutes |
| Rule False Positive Rate | < 5% |
| Rule Review Interval | Every 30–90 days |
| Use Cases in Production | ≥ 10 Active per domain |
| Threat Actor Coverage | Top 5 actors updated |

---

**SOaC Framework Team** | Version 1.0.0
