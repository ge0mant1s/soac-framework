
# Changelog

All notable changes to the SOaC Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-14

### 🎉 Initial Release

The first stable release of the **Security Operations as Code (SOaC) Framework**.

### Added

#### Core Features
- **Multi-Phase Threat Detection Engine**: Detect complex attacks across multiple stages
  - Entity-based correlation (user, host, IP, file)
  - Temporal windowing (5 min - 24 hours)
  - Confidence scoring (high/medium/low)
  - 10 pre-built operational models

#### Device Integration
- **Universal Device Connectors**:
  - Palo Alto Networks NGFW (PAN-OS REST API)
  - Microsoft Entra ID (Microsoft Graph API)
  - SIEM platforms (Splunk, Elasticsearch)
  - Extensible connector architecture

#### Event Management
- **Event Ingestion Pipeline**:
  - Automatic background collection (configurable intervals)
  - Event normalization and validation
  - Manual and automatic sync
  - Event enrichment
  - Event retention policies

#### Detection & Response
- **Operational Models** (Pre-built):
  1. Ransomware Detection
  2. Data Theft/Exfiltration
  3. Intrusion Detection
  4. Financial Fraud
  5. Denial of Service (DoS/DDoS)
  6. Malware Infection
  7. Supply Chain Attack
  8. Insider Threat
  9. Credential Abuse
  10. Misconfiguration Detection

- **SOAR Playbooks**:
  - Endpoint Containment
  - Identity Lockdown
  - Network Containment
  - Cloud Mitigation
  - Notification & Ticketing
  - Configurable decision matrix
  - Manual approval workflows

#### Incident Management
- **Complete Incident Lifecycle**:
  - Automatic incident creation
  - Assignment and workflow management
  - Investigation tools
  - Event timeline visualization
  - Status tracking
  - MITRE ATT&CK mapping

#### User Interface
- **React + TypeScript Frontend**:
  - Real-time dashboard
  - Device management
  - Rule management
  - Event browser with filtering
  - Incident investigation
  - Operational models viewer
  - Device health monitoring
  - JWT authentication
  - Role-based access control

#### Backend API
- **FastAPI REST API**:
  - Comprehensive RESTful endpoints
  - OpenAPI/Swagger documentation
  - JWT authentication
  - Role-based access control (Admin, Analyst, Viewer)
  - Rate limiting
  - Audit logging

#### Deployment Options
- **Multiple Deployment Methods**:
  - Docker Compose (development & small production)
  - Kubernetes (production)
  - AWS (ECS/Fargate + RDS + ALB)
  - Azure (Container Instances + PostgreSQL)
  - Railway.app (free tier)
  - One-click deployment scripts

#### Infrastructure as Code
- **Terraform Configurations**:
  - AWS infrastructure (ECS, RDS, ALB, ECR)
  - Azure infrastructure (coming soon)
  - Variables and outputs
  - Auto-scaling configuration

#### CI/CD
- **GitHub Actions Workflows**:
  - Continuous Integration (tests, linting, security scans)
  - Continuous Deployment (AWS, Railway)
  - Automated Docker builds
  - Security vulnerability scanning

#### Documentation
- **Comprehensive Documentation**:
  - Architecture overview
  - Installation guides (Docker, K8s, AWS, Azure)
  - Configuration guide
  - Device integration guide
  - Operational models guide
  - SOAR playbooks guide
  - API reference
  - Troubleshooting guide
  - Security best practices
  - Contributing guidelines

#### Testing & Quality
- **Testing Infrastructure**:
  - Mock mode for testing without real devices
  - Sample data pre-loaded
  - Unit tests
  - Integration tests
  - End-to-end tests
  - Code coverage reporting

#### Security Features
- **Enterprise Security**:
  - JWT token-based authentication
  - Encrypted credential storage
  - CORS configuration
  - Rate limiting
  - Audit logging
  - Security scanning in CI/CD

### Technical Stack

**Backend**:
- FastAPI 0.104+
- SQLAlchemy (ORM)
- PostgreSQL 14+
- Python 3.11+
- Pydantic (validation)
- JWT (authentication)

**Frontend**:
- React 18
- TypeScript
- Material-UI (MUI)
- Vite (build tool)
- Axios (HTTP client)
- React Router

**Infrastructure**:
- Docker & Docker Compose
- Kubernetes
- Terraform
- GitHub Actions
- AWS (ECS, RDS, ALB, ECR)

### Sample Data

Included sample data for immediate testing:
- 6 sample devices (2 NGFW, 2 EntraID, 2 SIEM)
- 8 detection rules
- 3 sample incidents
- 5 operational models
- Threat actor profiles
- MITRE ATT&CK mappings

### Known Limitations

- Multi-tenancy support coming in v1.1
- CrowdStrike Falcon connector coming in v1.1
- AWS CloudTrail integration coming in v1.1
- Advanced ML-based anomaly detection coming in v2.0
- GraphQL API coming in v2.0

### Deprecations

None - this is the initial release.

### Security

No known security vulnerabilities at release. Report security issues to: support@soacframework.org (coming soon)

### Contributors

Created by the SOaC Framework Team © 2025

### Links

- [GitHub Repository](https://github.com/ge0mant1s/soac-framework)
- [Documentation](./docs/)
- [Installation Guide](./docs/INSTALLATION.md)
- [Quick Start](./QUICKSTART.md)

---

## Release Notes Template (for future releases)

### [X.Y.Z] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes to existing features

#### Deprecated
- Features marked for removal

#### Removed
- Removed features

#### Fixed
- Bug fixes

#### Security
- Security patches
