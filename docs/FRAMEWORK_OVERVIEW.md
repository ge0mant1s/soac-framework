
# SOaC Framework Overview

## Strategic Layer

### Unified Threat-Centric Correlation Model

**Strategic Objective**: Build a unified, intelligence-driven detection and response framework that integrates identity, endpoint, network, cloud, and application telemetry into a single, correlated defense fabric — detecting behaviors across the full attack lifecycle rather than isolated events.

This model moves beyond siloed detections toward a threat-chain-centric architecture, focusing on relationships between events, entity pivots, and kill chain sequencing.

### Conceptual Flow

```
Use Case → Threat Chain → Telemetry → Correlation Nodes
```

## Core Correlation Nodes

| Use Case | Threat Chain Stage | Primary Telemetry Sources | Key Fields |
|----------|-------------------|---------------------------|------------|
| 1. Ransomware | Initial Access → Execution → Collection → Exfiltration → Impact | Proofpoint TAP, Falcon Endpoint, PAN-OS, Umbrella, CloudTrail | UserName, ComputerName, SHA256HashData, aip |
| 2. Data Theft / Exfiltration | Collection → Exfiltration → Impact | Falcon, Umbrella, CloudTrail, Azure Activity | UserName, ComputerName, TargetFileName, RemoteAddressIP4 |
| 3. Credential Access / Abuse | Credential Access → Privilege Escalation | EntraID, Infoblox, Falcon Identity, AD | UserPrincipalName, ComputerName, aip, TargetServiceAccessIdentifier |
| 4. Supply Chain Attack | Initial Access → Execution → Persistence | Proofpoint, Falcon, CloudTrail, Azure Activity | UserName, SHA256HashData, aws.eventName, TaskName |
| 5. Misconfigurations | Persistence → Defense Evasion | CloudTrail, Azure Activity, EntraID, Falcon Spotlight | aws.eventName, UserPrincipalName, ComputerName |
| 6. Insider Threat | Collection → Exfiltration → Impact | Falcon Endpoint, Proofpoint, EntraID | UserName, aip, TargetFileName |
| 7. Command & Control | Command & Control → Exfiltration | Falcon Cloud, Umbrella, PAN-OS | ComputerName, RemoteAddressIP4, url.domain |
| 8. Intrusion / Lateral Movement | Execution → Privilege Escalation → Discovery | Falcon, Infoblox, PAN-OS, EntraID | UserName, ComputerName, TargetServiceAccessIdentifier, aip |
| 9. Persistence / Defense Evasion | Persistence → Privilege Escalation | Azure Activity, Falcon Endpoint, EntraID | UserName, ComputerName, TaskName, RegistryKey |
| 10. Financial Fraud / Theft | Credential Access → Manipulation → Exfiltration | ERP / Finance Logs, EntraID, CloudTrail, Falcon | UserName, TransactionID, aip, AccountNumber |

## Strategic Correlation Map

### Horizontal Layers (Attack Phases)

**5. Impact / Exfiltration** ← Data Loss, Encryption, Fraud  
Sources: Falcon, Proofpoint, CloudTrail, ERP

**4. Lateral Movement / C2** ← Internal Movement, Beaconing  
Sources: Falcon Cloud, PAN-OS, Umbrella

**3. Persistence / Escalation** ← Privilege Gain, Tasks, Misconfigs  
Sources: Azure Activity, EntraID, CloudTrail, AD

**2. Execution / Credential Access** ← Code Execution, Privilege Use  
Sources: Falcon, EntraID, Infoblox, AD

**1. Initial Access / Recon / Delivery** ← Email, Vendor, Supply Chain, Cloud  
Sources: Proofpoint, Falcon Identity, Umbrella, CloudTrail

Each layer corresponds to a MITRE ATT&CK tactic, allowing direct mapping between telemetry, attacker behaviors, and detection controls.

### Vertical Corridors (Entity Pivots)

| Entity Type | Shared Fields | Cross-Source Role |
|-------------|---------------|-------------------|
| User Identity | UserName, UserPrincipalName, UserSid | Binds identity activity across AD, EntraID, and endpoints |
| Host / Endpoint | ComputerName, aid, cid | Connects process activity to network sessions and cloud actions |
| Network / IP | LocalAddressIP4, RemoteAddressIP4, aip | Tracks traffic between endpoint and cloud or external IPs |
| File / Process | SHA256HashData, FileName, CommandLine | Links file execution to delivery and malware detections |
| Service / Resource | TaskName, ResourceName, aws.eventName | Connects persistence artifacts and cloud changes |
| Transaction / Record | TransactionID, VendorID, Amount | Used in Financial Fraud to correlate SOC and finance data |

### Cross-Domain Integration

| Layer Link | Primary Connection | Purpose |
|------------|-------------------|---------|
| Endpoint ↔ Identity | Falcon + EntraID | Detect credential misuse leading to code execution |
| Endpoint ↔ Network | Falcon + PAN-OS + Umbrella | Detect malware, ransomware, or beacon traffic |
| Identity ↔ Cloud | EntraID + CloudTrail + Azure | Detect IAM and policy abuse across tenants |
| Network ↔ Cloud | PAN-OS + CloudTrail | Detect data exfiltration or command tunneling |
| Endpoint ↔ Finance / SaaS | Falcon + ERP / Finance Logs | Detect fraudulent actions via compromised sessions |

## Strategic Correlation Flow

```
[Delivery / Access]
        ↓
[Execution / Credential Use]
        ↓
[Lateral Movement / Persistence]
        ↓
[Impact / Exfiltration / Fraud]
```

Each phase forms part of a behavioral chain, correlated through shared entities. When **3 or more stages** align within the defined time window, SOAR containment is triggered automatically.

## Strategic Validation Principles

| Principle | Purpose |
|-----------|---------|
| Behavioral Correlation | Focus on sequences of actions, not single events |
| Cross-Source Confirmation | Require two or more independent sources to confirm an event |
| Entity Context | All detections tied to identity, host, IP, or transaction nodes |
| Adaptive Confidence Scoring | Weight sources by reliability (Falcon > Umbrella > Proofpoint) |
| Full Lifecycle Mapping | Every use case covers multiple MITRE ATT&CK tactics |

## Strategic Outcome

A Unified Correlation & Response Fabric that:
- ✅ Detects multi-phase adversary behavior early
- ✅ Correlates identity, endpoint, and cloud activity in real time
- ✅ Enables automated containment through SOAR
- ✅ Provides risk-based visibility for leadership dashboards

---

## Tactical Layer

### Tactical Correlation Pattern Library

**Purpose**: The Tactical Layer operationalizes the strategy — defining pattern logic, correlation timing, and cross-source joins that transform the conceptual model into live detections, rules, and automation triggers.

Each pattern below is reusable across multiple use cases and mapped to MITRE ATT&CK tactics.

### Correlation Patterns

| Pattern ID | Name | Tactics Covered | Window | Key Sources |
|-----------|------|-----------------|--------|-------------|
| R1 | Ransomware Chain | Initial Access → Execution → Impact | 30 min | Proofpoint, Falcon, PAN-OS |
| D1 | Data Exfiltration | Collection → Exfiltration | 60 min | Falcon, PAN-OS, CloudTrail, Umbrella |
| C1 | Credential Abuse | Credential Access → Privilege Escalation | 10 min | EntraID, AD, Infoblox, Falcon Identity |
| S1 | Supply Chain Compromise | Initial Access → Execution → Persistence | 2 hrs | Proofpoint, Falcon, CloudTrail, Azure |
| M1 | Misconfiguration Drift | Persistence → Defense Evasion | 24 hrs | CloudTrail, EntraID, Falcon |
| I1 | Insider Threat | Collection → Exfiltration → Impact | 8 hrs | Falcon, Proofpoint, Umbrella, EntraID |
| X1 | Command & Control | C2 → Exfiltration → Impact | 15 min | Falcon Cloud, Umbrella, PAN-OS |
| P1 | Persistence / Evasion | Persistence → Defense Evasion → Escalation | 30 min | Falcon, Azure, EntraID |
| IN1 | Intrusion Chain | Execution → Lateral Movement → Persistence | 90 min | Falcon, Infoblox, PAN-OS, EntraID |
| FF1 | Financial Fraud | Credential Abuse → Manipulation → Exfiltration → Impact | 6 hrs | EntraID, Finance Logs, Falcon, CloudTrail |
| DOS1 | Denial of Service | Availability → Impact | 15 min | PAN-OS, Umbrella, CloudTrail, EntraID |

### Cross-Correlation Mechanics

#### 1. Event Sequence Correlation
- Match events by shared entities within defined time windows
- Require phase progression (Initial → Execution → Impact)

#### 2. Entity-Based Joins
Joins on:
- UserName / UserPrincipalName
- ComputerName / aid
- aip / RemoteAddressIP4
- SHA256HashData (binary linkage)
- TransactionID (finance linkage)

#### 3. Temporal Windows
- **Real-time (5-15 min)**: Attacks in motion (R1, X1, DOS1)
- **Short-term (30-90 min)**: Lateral movement, privilege abuse (IN1, C1)
- **Long-term (6-24 hrs)**: Drift or fraud (M1, FF1)

#### 4. Correlation Confidence Matrix

| Phase Match | Sources Matched | Confidence Level |
|-------------|-----------------|------------------|
| Single-source alert | 1 | Low |
| Multi-source same entity | 2 | Medium |
| Multi-phase chain (≥3) | 3+ | High |
| Full lifecycle match | 4-5 | Critical (trigger SOAR) |

### Common Pattern Components

Each correlation pattern uses the same modular structure:

```python
join(
  queryX=Phase1,
  queryY=Phase2,
  queryZ=Phase3,
  on=[UserName, ComputerName, aip],
  within=<time_window>
)
| groupBy([UserName, ComputerName], function=count(), limit=10000)
| _count >= 3
```

This design provides standardization across all analytic rules, simplifying deployment, versioning, and continuous improvement.

### Tactical Playbook Integration

Each pattern maps directly to SOAR response groups:

| Pattern | SOAR Response Group | Actions |
|---------|-------------------|---------|
| R1 | Containment & Recovery | Isolate host, disable user, block C2 |
| D1 | Exfiltration Stop | Quarantine endpoint, suspend cloud uploads |
| C1 | Credential Reset | Disable account, reset MFA, audit logins |
| S1 | Vendor Engagement | Quarantine binary, notify vendor, rollback IAM |
| M1 | Config Enforcement | Rollback drift, reapply baseline |
| I1 | Insider Mitigation | Suspend access, notify HR/legal |
| X1 | Network Containment | Block domain/IP, terminate session |
| P1 | Persistence Eradication | Remove task/service, revoke policy changes |
| IN1 | Active Intrusion | Contain host, block movement, forensic dump |
| FF1 | Transaction Freeze | Hold payment, lock account, reverse funds |
| DOS1 | Resilience Response | Block source IPs, trigger autoscale, activate WAF |

### Tactical Principles

| Principle | Purpose |
|-----------|---------|
| Standardized Patterns | Every detection follows the same join-logic and entity model |
| Dynamic Windowing | Detection time adapts to attack velocity |
| SOAR Integration Ready | Each rule maps directly to response playbooks |
| Feedback-Driven Optimization | Each detection feeds IOCs into Threat Intel & GRC layers |
| Defense-in-Depth Verification | Endpoint + Identity + Cloud correlation required before escalation |

## Tactical Outcome

✅ A library of reusable detection patterns standardized across all use cases  
✅ Real-time correlation of telemetry from 10+ sources using unified fields  
✅ Consistent integration with SOAR playbooks and automated containment actions  
✅ Enables threat hunting, adversary emulation, and KPI measurement with full coverage visibility

---

**SOaC Framework Team** | Version 1.0.0
