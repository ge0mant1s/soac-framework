# SOaC Framework Architecture Overview

## Introduction

Security Operations as Code (SOaC) is a paradigm shift in how security operations are designed, deployed, and managed. By treating security operations as code, we enable:

- **Version Control**: Track changes to detection rules and playbooks
- **Automation**: Deploy and update rules across multiple platforms simultaneously
- **Consistency**: Ensure uniform security posture across all environments
- **Collaboration**: Enable security teams to work together using modern DevOps practices
- **Scalability**: Manage thousands of detection rules efficiently

## Core Principles

### 1. Write Once, Deploy Everywhere
Use CQL (Common Query Language) to write detection rules once and deploy them across 21+ security platforms.

### 2. Infrastructure as Code
Define your entire security operations infrastructure in code, including:
- Detection rules
- Incident response playbooks
- Integration configurations
- SLA policies
- Escalation procedures

### 3. Continuous Integration/Continuous Deployment (CI/CD)
Integrate SOaC into your CI/CD pipeline to automatically test and deploy security controls.

### 4. Observability & Metrics
Track the effectiveness of your security operations with built-in metrics and dashboards.

## Architecture Layers

### Layer 1: Data Ingestion
- Platform connectors
- Normalized data models (ECS, OCSF)
- Real-time streaming

### Layer 2: Detection & Correlation
- CQL Engine
- Cross-platform correlation
- Threat intelligence enrichment

### Layer 3: Incident Management
- Automated incident creation
- SLA tracking
- Evidence collection
- Timeline reconstruction

### Layer 4: Response & Orchestration
- Automated playbooks
- Multi-platform actions
- Approval workflows

### Layer 5: User Interface
- Web dashboard
- AI assistant
- REST API
- CLI tools

## Key Components

### CQL Engine
The heart of SOaC, translating universal queries to platform-specific languages.

**Supported Platforms:**
- SIEM: Splunk, Elastic, Sentinel, QRadar, Chronicle, LogRhythm
- EDR: CrowdStrike, SentinelOne, Defender, Carbon Black, Cortex XDR
- Network: Palo Alto, Cisco, Fortinet, Zscaler
- Cloud: AWS Security Hub, Azure Security, GCP SCC
- Identity: Okta, Entra ID, Ping Identity
- TI: MISP, ThreatConnect, Anomali, VirusTotal

### Incident Manager
Complete lifecycle management for security incidents with:
- Dynamic severity scoring
- SLA tracking and alerting
- Evidence collection and preservation
- Integration with ticketing systems (Jira, ServiceNow)

### Deployment Manager
Centralized configuration and deployment:
- Multi-platform rule deployment
- Version control integration
- Rollback capabilities
- Health monitoring

### AI Assistant
Natural language interface for security operations:
- Query generation from natural language
- Incident analysis and recommendations
- Threat intelligence lookups
- Playbook suggestions

## Data Flow

```
External Events → Platform Connectors → Normalization → CQL Engine
                                                            ↓
                                                    Detection Rules
                                                            ↓
                                                    Correlation Engine
                                                            ↓
                                                    Incident Manager
                                                            ↓
                                                    Response Orchestrator
                                                            ↓
                                                    Platform Actions
```

## Security Considerations

### Authentication & Authorization
- JWT-based API authentication
- Role-based access control (RBAC)
- Multi-factor authentication support
- API key management

### Data Protection
- Encryption at rest and in transit
- Secure credential storage (HashiCorp Vault integration)
- Audit logging
- Data retention policies

### Compliance
- SOC 2 Type II ready
- GDPR compliant
- HIPAA compatible
- ISO 27001 aligned

## Scalability

SOaC is designed to scale from small teams to enterprise deployments:

- **Small Team** (1-10 analysts): Single Docker Compose deployment
- **Medium Team** (10-50 analysts): Kubernetes cluster with HA
- **Enterprise** (50+ analysts): Multi-region, multi-tenant deployment

## Integration Patterns

### Push Model
SOaC pushes detection rules to platforms via APIs.

### Pull Model
Platforms query SOaC for updated rules on a schedule.

### Hybrid Model
Combination of push and pull based on platform capabilities.

## Extensibility

### Custom Platforms
Add support for new platforms by implementing the Platform Connector interface.

### Custom Playbooks
Write response playbooks in Python or YAML.

### Custom Enrichments
Integrate additional threat intelligence sources.

### Plugins
Extend functionality with community or commercial plugins.

## Roadmap

### v0.2.0 (Q2 2025)
- SOAR playbook automation
- Advanced ML-based anomaly detection
- Mobile app
- Kubernetes operator

### v0.3.0 (Q3 2025)
- Multi-tenancy
- Compliance reporting
- Custom dashboard builder
- Threat hunting workbench

### v1.0.0 (Q4 2025)
- Full enterprise features
- Advanced AI capabilities
- Marketplace for rules and playbooks
- Professional services

## Getting Help

- Documentation: https://docs.soac.io
- Community Forum: https://community.soac.io
- Discord: https://discord.gg/soac
- Email: support@soac.io

---

**Next**: [CQL Language Reference](cql_reference.md)
