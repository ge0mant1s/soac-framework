# Sample GitHub Issues for SOaC Framework

This document contains sample issues you can create to populate your GitHub repository and demonstrate the issue templates.

---

## 🐛 Sample Bug Issues

### Issue #1: CQL Parser Fails on Nested GroupBy

**Title**: `[BUG] CQL parser fails when using nested groupBy functions`

**Labels**: `bug`, `cql-engine`, `high-priority`

**Description**:

```markdown
## 🐛 Bug Description
The CQL parser throws a syntax error when attempting to use nested groupBy functions with multiple aggregations.

## 📋 To Reproduce
1. Create a CQL query with nested groupBy:
```cql
#event.category = network
groupBy([source.ip], function=count(as="connections"))
groupBy([destination.port], function=sum(connections, as="total"))
```

1. Execute via API: `POST /api/cql/translate`

2. See error: `SyntaxError: Unexpected token 'groupBy'`

## ✅ Expected Behavior

The parser should support nested groupBy operations for complex aggregations.

## ❌ Actual Behavior

Parser throws syntax error and fails to translate the query.

## 🖥️ Environment

* OS: Ubuntu 22.04

* Python Version: 3.9.7

* SOaC Version: 0.1.0

* Deployment Method: Docker

## 📝 Logs

```
ERROR: CQL Parser failed at line 3
SyntaxError: Unexpected token 'groupBy' at position 45
```

## 🤔 Possible Solution

Modify the parser to support recursive groupBy parsing or implement a multi-stage aggregation approach.

```

---

### Issue #2: Docker Compose Fails on ARM Architecture

**Title**: `[BUG] Docker Compose fails to start on ARM64/Apple Silicon`

**Labels**: `bug`, `docker`, `deployment`

**Description**:
```markdown
## 🐛 Bug Description
Docker Compose fails to build images on ARM64 architecture (Apple Silicon M1/M2).

## 📋 To Reproduce
1. Clone repository on Mac with M1/M2 chip
2. Run `docker-compose up -d`
3. See build errors for PostgreSQL and Redis images

## ✅ Expected Behavior
Docker Compose should build and run successfully on ARM64 architecture.

## 🖥️ Environment
- OS: macOS 13.0 (Ventura)
- Architecture: ARM64 (Apple M1)
- Docker Version: 24.0.6
- SOaC Version: 0.1.0

## 🤔 Possible Solution
Use multi-architecture base images or add platform-specific Dockerfiles.
```

---

## ✨ Sample Feature Request Issues

### Issue #3: Add Support for SIGMA Rule Import

**Title**: `[FEATURE] Add SIGMA rule converter to import existing detection rules`

**Labels**: `enhancement`, `detection-rules`, `high-priority`

**Description**:

```markdown
## 🚀 Feature Description
Add ability to import and convert SIGMA detection rules to CQL format.

## 💡 Problem Statement
Many organizations already have detection rules in SIGMA format. Converting them manually to CQL is time-consuming and error-prone.

## 🎯 Proposed Solution
Implement a SIGMA-to-CQL converter that:
- Parses SIGMA YAML files
- Maps SIGMA fields to ECS/OCSF fields
- Generates equivalent CQL queries
- Preserves metadata (MITRE ATT&CK, severity, etc.)

## 📊 Use Case
As a detection engineer,
I want to import my existing SIGMA rules,
So that I can quickly migrate to SOaC without rewriting all rules.

## 🎨 Example

**Input (SIGMA)**:
```yaml
title: Brute Force Attack
logsource:
  category: authentication
detection:
  selection:
    event.outcome: failure
  condition: selection | count(by=[user.name, source.ip]) > 10
```

**Output (CQL)**:

```cql
#event.category = authentication
event.outcome = failure
groupBy([user.name, source.ip], function=count(as="failures"))
failures > 10
```

## 🏷️ Category

* \[x\] Detection Rules

* \[x\] CQL Engine

## 📈 Priority

* \[x\] High - Would significantly improve my workflow

## 🌍 Impact

* \[x\] Detection engineers

* \[x\] All users

```

---

### Issue #4: Real-time Dashboard with WebSocket Support

**Title**: `[FEATURE] Add real-time incident updates via WebSocket`

**Labels**: `enhancement`, `web-ui`, `websocket`

**Description**:
```markdown
## 🚀 Feature Description
Add WebSocket support to the Web UI for real-time incident and alert updates without page refresh.

## 💡 Problem Statement
Currently, users must manually refresh the dashboard to see new incidents and alerts, which delays response time.

## 🎯 Proposed Solution
Implement WebSocket connection between API and Web UI:
- Push new incidents to dashboard in real-time
- Update incident status changes live
- Show real-time alert counts
- Display live platform health status

## 📊 Use Case
As a SOC analyst,
I want to see new incidents immediately,
So that I can respond faster to security threats.

## 🏷️ Category
- [x] Web UI
- [x] API

## 📈 Priority
- [x] High - Would significantly improve my workflow
```

---

## 🔌 Sample Platform Integration Issues

### Issue #5: Add Support for Wazuh SIEM

**Title**: `[INTEGRATION] Add support for Wazuh SIEM`

**Labels**: `integration`, `enhancement`, `siem`

**Description**:

```markdown
## 🔌 Platform Information

**Platform Name**: Wazuh

**Platform Type**:
- [x] SIEM
- [x] EDR/XDR

**Vendor**: Wazuh, Inc.

**Platform Website**: https://wazuh.com

**API Documentation**: https://documentation.wazuh.com/current/user-manual/api/reference.html

## 📊 Platform Popularity
- Open-source SIEM with 10M+ downloads
- Growing adoption in enterprise and SMB
- Active community with 15k+ GitHub stars

## 🎯 Use Case
I want to deploy CQL detection rules to Wazuh so that I can maintain consistent detection logic across my open-source and commercial security tools.

## 🔧 Technical Details

**API Type**:
- [x] REST API

**Authentication Method**:
- [x] API Key
- [x] Basic Auth

**Query Language**: Custom Wazuh Query Language (similar to Elastic)

**Rate Limits**: 300 requests/minute

## 📋 Required Capabilities
- [x] Query Translation (CQL → Wazuh Query)
- [x] Detection Rule Deployment
- [x] Event Retrieval
- [x] Alert Management
- [x] Health Monitoring

## 📚 Resources

**Do you have access to this platform?**
- [x] Yes, I can help test

**Can you provide:**
- [x] Sample queries in platform's native language
- [x] Documentation or examples
- [x] Test data or sandbox environment

## 🤝 Contribution
- [x] Yes, I can help with testing
- [x] Yes, I can provide documentation
```

---

### Issue #6: Add Support for Datadog Security Monitoring

**Title**: `[INTEGRATION] Add support for Datadog Security Monitoring`

**Labels**: `integration`, `enhancement`, `cloud-security`

**Description**:

```markdown
## 🔌 Platform Information

**Platform Name**: Datadog Security Monitoring

**Platform Type**:
- [x] SIEM
- [x] Cloud Security

**Vendor**: Datadog

**Platform Website**: https://www.datadoghq.com/product/security-platform/

**API Documentation**: https://docs.datadoghq.com/api/latest/security-monitoring/

## 📊 Platform Popularity
- Used by 25,000+ organizations
- Strong presence in cloud-native environments
- Integrated with major cloud providers

## 🎯 Use Case
Deploy SOaC detection rules to Datadog Security Monitoring for unified cloud security monitoring.

## 🔧 Technical Details

**API Type**:
- [x] REST API

**Authentication Method**:
- [x] API Key

**Query Language**: Datadog Query Language (DQL)

## 📋 Required Capabilities
- [x] Query Translation (CQL → DQL)
- [x] Detection Rule Deployment
- [x] Event Retrieval
- [x] Alert Management
```

---

## 🎯 Sample Detection Rule Issues

### Issue #7: Detection Rule - Suspicious PowerShell Execution

**Title**: `[RULE] Suspicious PowerShell Execution with Encoded Commands`

**Labels**: `detection-rule`, `contribution`, `malware`

**Description**:

```markdown
## 🎯 Rule Information

**Rule Name**: Suspicious PowerShell Execution with Encoded Commands

**Rule ID**: MAL-001

**MITRE ATT&CK Technique(s)**:
- Tactic: Execution
- Technique: T1059.001 - PowerShell
- Sub-technique: T1027 - Obfuscated Files or Information

**Severity**:
- [x] High

**Use Case Category**:
- [x] Malware
- [x] Intrusion

## 📝 Rule Description
Detects PowerShell execution with encoded commands, which is commonly used by malware and attackers to evade detection and hide malicious payloads.

## 🔍 CQL Query

```cql
#event.category = process
process.name = powershell.exe
process.command_line contains "-enc" OR process.command_line contains "-encodedcommand"
groupBy([host.name, user.name], function=count(as="executions"))
executions >= 1
```

## 🔧 Platform Translations

### Splunk (SPL)

```spl
index=windows EventCode=4688 
(CommandLine="*-enc*" OR CommandLine="*-encodedcommand*") 
Image="*powershell.exe"
| stats count as executions by ComputerName, User
| where executions >= 1
```

### Azure Sentinel (KQL)

```kql
SecurityEvent
| where EventID == 4688
| where Process has "powershell.exe"
| where CommandLine has_any ("-enc", "-encodedcommand")
| summarize executions=count() by Computer, Account
| where executions >= 1
```

## 🚨 Response Actions

1. **Immediate Actions**:

* \[x\] Isolate affected endpoint

* \[x\] Capture memory dump

* \[x\] Review PowerShell logs

1. **Containment**:

* \[x\] Kill suspicious PowerShell processes

* \[x\] Block malicious IPs/domains

* \[x\] Disable compromised accounts

1. **Eradication**:

* \[x\] Remove malware artifacts

* \[x\] Scan for persistence mechanisms

## ⚠️ False Positives

* Legitimate administrative scripts using encoding

* Software deployment tools

* Security tools using PowerShell

**Tuning Recommendations**:

* Whitelist known administrative scripts

* Exclude trusted service accounts

* Add parent process context

## 📋 Data Sources

* \[x\] Endpoint logs

* \[x\] Windows Security Event ID 4688

* \[x\] Sysmon Event ID 1

```

---

## 📚 Sample Documentation Issues

### Issue #8: Missing API Authentication Examples

**Title**: `[DOCS] Add API authentication examples for all methods`

**Labels**: `documentation`, `api`

**Description**:
```markdown
## 📚 Documentation Type
- [x] Missing documentation

## 📍 Location
**File/Page**: docs/api_reference.md
**Section**: "Authentication" section

## 🐛 Issue Description
The API documentation mentions JWT authentication but doesn't provide complete examples for all authentication methods.

**Current State**:
```

Authentication is required for all API endpoints.

```

**Expected State**:
```

Authentication is required for all API endpoints.

### JWT Authentication

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:5000/api/incidents
```

### API Key Authentication

```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  http://localhost:5000/api/incidents
```

```

## 💡 Suggested Improvement
Add complete examples for:
- JWT token authentication
- API key authentication
- OAuth 2.0 flow (if supported)
- Token refresh process

## 🎯 Impact
- [x] New users
- [x] All users
```

---

## 🚀 How to Create These Issues

1. **Go to your repository**: [https://github.com/ge0mant1s/soac-framework/issues](https://github.com/ge0mant1s/soac-framework/issues)

2. **Click "New Issue"**

3. **Select the appropriate template**:

* Bug Report

* Feature Request

* Platform Integration Request

* Detection Rule Contribution

* Documentation Issue

1. **Fill in the template** with the sample content above

2. **Add appropriate labels** (bug, enhancement, documentation, etc.)

3. **Submit the issue**

---

## 📊 Recommended Initial Issues

Create these issues first to demonstrate your project's roadmap:

### High Priority

1. ✅ SIGMA rule converter (Feature)

2. ✅ Wazuh integration (Platform)

3. ✅ WebSocket support (Feature)

4. ✅ ARM64 Docker support (Bug)

### Medium Priority

1. ✅ Datadog integration (Platform)

2. ✅ PowerShell detection rule (Rule)

3. ✅ API documentation (Docs)

### Community Engagement

1. Create a "Good First Issue" label

2. Create a "Help Wanted" label

3. Pin important issues to the top

---

## 🏷️ Recommended Labels

Create these labels in your repository:

**Type Labels**:

* `bug` (red) - Something isn't working

* `enhancement` (blue) - New feature or request

* `documentation` (green) - Documentation improvements

* `detection-rule` (purple) - Detection rule contribution

* `integration` (orange) - Platform integration

**Priority Labels**:

* `critical` (dark red) - Critical priority

* `high-priority` (red) - High priority

* `medium-priority` (yellow) - Medium priority

* `low-priority` (gray) - Low priority

**Status Labels**:

* `in-progress` (yellow) - Work in progress

* `needs-review` (orange) - Needs review

* `blocked` (red) - Blocked by dependencies

* `help-wanted` (green) - Community help wanted

* `good-first-issue` (light green) - Good for newcomers

**Component Labels**:

* `cql-engine` - CQL Engine component

* `web-ui` - Web UI component

* `api` - API component

* `ai-assistant` - AI Assistant component

* `incident-management` - Incident Management

---

**Ready to populate your GitHub Issues!** 🎉