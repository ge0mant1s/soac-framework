
# Operational Models

This directory contains operational model definitions for threat detection.

## Overview

Operational models define multi-phase detection patterns for complex security threats. Each model describes:

- **Attack phases**: Stages of the attack lifecycle
- **Data sources**: Security tools that provide telemetry
- **Correlation logic**: How to connect events across phases
- **Response playbooks**: Automated response actions

## Pre-Built Models

The SOaC Framework includes the following pre-built operational models:

### 1. Ransomware Detection
**File**: `ransomware_model.json`

Detects ransomware attacks through the full kill chain:
- **Phase 1**: Delivery (email attachments, malicious links)
- **Phase 2**: Execution (PowerShell, suspicious processes)
- **Phase 3**: Encryption (mass file renaming, backup deletion)
- **Phase 4**: Impact (service disruption, ransom note)

**Sources**: Proofpoint, Falcon EDR, PAN-OS, File Integrity Monitoring

### 2. Data Theft/Exfiltration
**File**: `data_theft_model.json`

Detects unauthorized data movement:
- **Phase 1**: Collection (local file staging)
- **Phase 2**: Staging (archive creation, compression)
- **Phase 3**: Exfiltration (outbound network transfer)
- **Phase 4**: Cloud Upload (S3, Azure Blob, etc.)

**Sources**: Falcon EDR, PAN-OS, Umbrella DNS, AWS CloudTrail

### 3. Intrusion Detection
**File**: `intrusion_model.json`

Detects active intrusion attempts:
- **Phase 1**: Initial Foothold (suspicious execution)
- **Phase 2**: Privilege Abuse (credential access)
- **Phase 3**: Lateral Movement (SMB, RDP, WMI)
- **Phase 4**: Persistence (scheduled tasks, services)

**Sources**: Falcon EDR, Entra ID, Active Directory, PAN-OS

### 4. Financial Fraud
**File**: `fraud_model.json`

Detects fraudulent financial activity:
- **Phase 1**: Account Compromise (suspicious login)
- **Phase 2**: Transaction Manipulation (unauthorized payments)
- **Phase 3**: Data Exfiltration (financial records)
- **Phase 4**: Cover-up (log deletion)

**Sources**: Entra ID, ERP logs, Falcon EDR, CloudTrail

### 5. Denial of Service (DoS/DDoS)
**File**: `dos_model.json`

Detects availability attacks:
- **Phase 1**: Network Flood (high-volume traffic)
- **Phase 2**: Service Degradation (CPU/memory exhaustion)
- **Phase 3**: Authentication Exhaustion (failed login floods)
- **Phase 4**: Mitigation (WAF activation, rate limiting)

**Sources**: PAN-OS, Umbrella DNS, Entra ID, CloudWatch

### Additional Models

6. **Malware Infection** - `malware_model.json`
7. **Supply Chain Attack** - `supply_chain_model.json`
8. **Insider Threat** - `insider_threat_model.json`
9. **Credential Abuse** - `credential_abuse_model.json`
10. **Misconfiguration** - `misconfiguration_model.json`

## Model Structure

Each operational model is a JSON file with the following structure:

```json
{
  "name": "Model Name",
  "description": "Description of the threat",
  "use_case": "threat_type",
  "mitre_tactics": ["TA0001", "TA0002"],
  "severity": "critical|high|medium|low",
  "phases": [
    {
      "name": "phase_name",
      "description": "Phase description",
      "mitre_techniques": ["T1566.001"],
      "sources": ["device_type"],
      "queries": [
        {
          "source": "device_name",
          "query": "detection logic",
          "fields": ["field1", "field2"]
        }
      ]
    }
  ],
  "correlation": {
    "entity_fields": ["user", "computer", "ip"],
    "time_window": 3600,
    "min_phases": 3,
    "confidence_weights": {
      "phase_count": 0.4,
      "source_diversity": 0.3,
      "temporal_proximity": 0.3
    }
  },
  "playbooks": [
    {
      "name": "Containment Playbook",
      "trigger_conditions": {
        "min_phases": 3,
        "confidence": "high"
      },
      "actions": [...]
    }
  ]
}
```

## Creating Custom Models

To create a custom operational model:

### 1. Create Model File

Create a new JSON file in this directory:

```bash
touch custom_threat_model.json
```

### 2. Define Model Structure

```json
{
  "name": "Custom Threat Detection",
  "description": "Detect custom threat pattern",
  "use_case": "custom_threat",
  "severity": "high",
  "phases": [
    {
      "name": "initial_access",
      "description": "Unauthorized access attempt",
      "sources": ["entraid"],
      "queries": [
        {
          "source": "entraid",
          "query": "SignInLogs | where ResultType != 0",
          "fields": ["UserPrincipalName", "IPAddress", "ResultType"]
        }
      ]
    },
    {
      "name": "execution",
      "description": "Code execution",
      "sources": ["falcon"],
      "queries": [
        {
          "source": "falcon",
          "query": "ProcessRollup2 | where CommandLine contains 'powershell'",
          "fields": ["UserName", "ComputerName", "CommandLine"]
        }
      ]
    }
  ],
  "correlation": {
    "entity_fields": ["user", "computer"],
    "time_window": 1800,
    "min_phases": 2
  }
}
```

### 3. Load Model

Reload operational models via API:

```bash
curl -X POST http://localhost:8000/api/v1/operational-models/reload \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Or restart the backend service.

### 4. Test Model

Submit test events and verify detection:

```bash
curl -X POST http://localhost:8000/api/v1/detection/test-model \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "custom_threat",
    "test_events": [...]
  }'
```

## Model Best Practices

### Detection Logic

1. **Use multiple phases**: Minimum 2-3 phases for high confidence
2. **Diverse sources**: Combine endpoint, network, identity, cloud telemetry
3. **Entity correlation**: Always correlate on entities (user, host, IP)
4. **Temporal windows**: Match window to attack speed (fast: 5-15 min, slow: hours)

### Correlation Settings

- **Time Window**:
  - Fast attacks (ransomware, DoS): 5-30 minutes
  - Moderate attacks (intrusion): 30-90 minutes
  - Slow attacks (fraud, insider): 2-24 hours

- **Minimum Phases**:
  - High confidence: 3+ phases
  - Medium confidence: 2 phases
  - Low confidence: 1 phase (alert only)

- **Confidence Weights**:
  - `phase_count`: Weight for number of matched phases (0.4)
  - `source_diversity`: Weight for different data sources (0.3)
  - `temporal_proximity`: Weight for events close in time (0.3)

### Query Guidelines

- Use standardized field names (see schema)
- Test queries individually before combining
- Consider performance for high-volume sources
- Use appropriate time ranges
- Handle edge cases (null values, missing fields)

## Schema Reference

### Standard Field Names

```json
{
  "identity": {
    "user": "UserName | UserPrincipalName",
    "user_id": "UserId | ObjectId",
    "domain": "UserDomain"
  },
  "endpoint": {
    "computer": "ComputerName | HostName",
    "aid": "AgentId",
    "os": "OSVersion"
  },
  "network": {
    "src_ip": "LocalAddressIP4 | SourceIP",
    "dst_ip": "RemoteAddressIP4 | DestinationIP",
    "port": "RemotePort | DestinationPort",
    "protocol": "Protocol"
  },
  "process": {
    "name": "FileName | ProcessName",
    "path": "ImageFileName | FilePath",
    "command_line": "CommandLine",
    "hash": "SHA256HashData | FileHash"
  },
  "file": {
    "name": "TargetFileName",
    "path": "TargetFilePath",
    "hash": "MD5HashData | SHA256HashData"
  }
}
```

## Testing Models

### Unit Testing

Test individual phases:

```python
from app.services.correlation_engine import test_phase

events = [...]  # Sample events
result = test_phase("ransomware", "delivery", events)
assert result["matched"] == True
```

### Integration Testing

Test full correlation:

```python
from app.services.correlation_engine import correlate_events

events = load_test_events("ransomware_test.json")
incidents = correlate_events(events, operational_model="ransomware")
assert len(incidents) == 1
assert incidents[0].confidence == "high"
```

### Live Testing

Use mock mode or test devices:

1. Enable mock mode: `MOCK_MODE=true`
2. Submit test events via API
3. Verify incident creation
4. Check playbook execution

## Troubleshooting

### Model Not Loading

- Check JSON syntax: `jq . model.json`
- Verify all required fields are present
- Check backend logs: `docker-compose logs backend`

### No Incidents Created

- Verify events are being collected
- Check correlation settings (time window, min phases)
- Review query syntax for each phase
- Test individual queries
- Check entity field mappings

### False Positives

- Adjust confidence thresholds
- Refine query logic (add exclusions)
- Increase minimum phases required
- Adjust time windows
- Add whitelisting

### Performance Issues

- Optimize query logic
- Reduce time window
- Limit result sets
- Add indexes to database
- Use caching where appropriate

## Documentation

For more information, see:

- [Operational Models Guide](../../docs/OPERATIONAL_MODELS.md)
- [Detection Engine Documentation](../../docs/ARCHITECTURE.md#detection-layer)
- [SOAR Playbooks Guide](../../docs/SOAR_PLAYBOOKS.md)
- [API Reference](../../docs/API_REFERENCE.md)

## Support

For questions or issues:
- GitHub Issues: https://github.com/ge0mant1s/soac-framework/issues
- GitHub Discussions: https://github.com/ge0mant1s/soac-framework/discussions
- Documentation: https://github.com/ge0mant1s/soac-framework/docs

---

*Last updated: November 14, 2025 by SOaC Framework Team*
