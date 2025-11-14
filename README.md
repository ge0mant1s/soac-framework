# SOaC Framework v1.0

<div align="center">

![SOaC Framework](./docs/images/soac-logo.png)

**Security Operations as Code Framework**

*Automate, Correlate, and Respond to Security Threats with Intelligence*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Features](#-features) •
[Deployment](#-deployment-options) •
[Architecture](#-architecture)

</div>

---

## 📖 What is SOaC Framework?

The **Security Operations as Code (SOaC) Framework** is a comprehensive, open-source platform that transforms traditional security operations into automated, version-controlled, and intelligence-driven workflows. Built for modern security teams, SOaC enables you to:

- **Detect Complex Threats**: Multi-phase attack detection across the entire kill chain
- **Automate Response**: Execute intelligent playbooks based on threat patterns
- **Integrate Everything**: Connect with your existing security infrastructure (SIEM, EDR, NGFW, IdP)
- **Manage as Code**: Version control your security operations like you manage your infrastructure

### The Problem We Solve

Traditional security operations face critical challenges:
- 🚨 **Alert Fatigue**: Too many isolated alerts, not enough actionable incidents
- 🔍 **Lack of Correlation**: Events from different sources aren't connected
- ⏱️ **Slow Response**: Manual investigation and response takes too long
- 📊 **No Visibility**: Hard to understand the full attack story
- 🔧 **Configuration Drift**: Security rules and policies are inconsistent across platforms

### How SOaC Framework Helps

SOaC Framework provides a unified platform that:

1. **Correlates Events** across multiple security tools (endpoint, network, identity, cloud)
2. **Detects Behavioral Chains** rather than just isolated events
3. **Automates Response** with configurable SOAR playbooks
4. **Provides Intelligence** with built-in threat models and MITRE ATT&CK mapping
5. **Enables Operations as Code** - version control, testing, and deployment of security operations

---

## ✨ Features

### Core Capabilities

#### 🎯 Multi-Phase Threat Detection
- **Behavioral Correlation**: Detect attacks across multiple stages (Initial Access → Execution → Impact)
- **Entity Tracking**: Follow users, hosts, IPs, and files across time and data sources
- **Confidence Scoring**: High/Medium/Low confidence based on correlated evidence
- **10 Pre-Built Use Cases**: Ransomware, Data Theft, Intrusion, Fraud, DoS, and more

#### 🔌 Universal Device Integration
- **Palo Alto Networks NGFW**: Security rules, threat logs, device health
- **Microsoft Entra ID**: Sign-in logs, user activity, conditional access policies
- **SIEM Platforms**: Splunk, Elasticsearch integration
- **Extensible Architecture**: Add new connectors with simple Python classes

#### 🤖 Automated Response (SOAR)
- **Intelligent Playbooks**: Context-aware response actions
- **Decision Matrix**: Execute playbooks based on threat patterns and confidence
- **Multi-Platform Actions**: Isolate endpoints, disable accounts, block IPs/domains, generate tickets
- **Manual Override**: Review and approve actions before execution

#### 📊 Operational Intelligence
- **Real-Time Dashboard**: Device health, incident trends, event statistics
- **MITRE ATT&CK Mapping**: All detections mapped to tactics and techniques
- **Threat Landscape**: Pre-loaded threat actor profiles and IOCs
- **Incident Timeline**: Full event chain visualization for investigations

#### 🔒 Enterprise-Grade Security
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Admin, Analyst, Viewer roles
- **Encrypted Credentials**: Secure storage for device credentials
- **Audit Logging**: Complete audit trail of all actions

#### 💻 Developer-Friendly
- **RESTful API**: Comprehensive FastAPI backend with OpenAPI/Swagger docs
- **Infrastructure as Code**: Docker, Kubernetes, Terraform support
- **Version Control**: Manage detection rules and playbooks in Git
- **Extensible**: Plugin architecture for custom integrations

---

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (recommended)
- OR **Python 3.11+** and **Node.js 18+** for local development
- **PostgreSQL 14+** (included in Docker Compose)

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

**Default Credentials:**
- **Admin**: `admin` / `admin123`
- **Analyst**: `analyst` / `analyst123`

⚠️ **Change default passwords in production!**

### Option 2: Cloud Deployment (Railway, AWS, Azure)

**Railway.app (Free Tier Available)**
```bash
# One-click deploy to Railway
./deploy-to-railway.sh
```

**AWS (CloudFormation)**
```bash
# Deploy to AWS with CloudFormation
./scripts/deploy-aws.sh
```

**See detailed deployment guides:** [Deployment Documentation](./docs/DEPLOYMENT.md)

---

## 📚 Documentation

### Getting Started
- [Quick Start Guide](./QUICKSTART.md) - Get up and running in 10 minutes
- [Installation Guide](./docs/INSTALLATION.md) - Detailed installation instructions
- [Configuration Guide](./docs/CONFIGURATION.md) - Environment variables and settings

### Core Concepts
- [Architecture Overview](./docs/ARCHITECTURE.md) - System design and components
- [Framework Overview](./docs/FRAMEWORK_OVERVIEW.md) - SOaC methodology and principles
- [Threat Detection Model](./docs/THREAT_DETECTION.md) - How detection works

### Feature Guides
- [Device Integration](./docs/DEVICE_INTEGRATION.md) - Connect security devices
- [Operational Models](./docs/OPERATIONAL_MODELS.md) - Detection patterns and use cases
- [SOAR Playbooks](./docs/SOAR_PLAYBOOKS.md) - Automated response actions
- [API Reference](./docs/API_REFERENCE.md) - Complete API documentation

### Operational Use Cases
- [Ransomware Detection](./docs/use-cases/RANSOMWARE.md)
- [Data Theft/Exfiltration](./docs/use-cases/DATA_THEFT.md)
- [Intrusion Detection](./docs/use-cases/INTRUSION.md)
- [Financial Fraud](./docs/use-cases/FRAUD.md)
- [Denial of Service](./docs/use-cases/DOS.md)

### Deployment & Operations
- [Docker Deployment](./docs/deployment/DOCKER.md)
- [Kubernetes Deployment](./docs/deployment/KUBERNETES.md)
- [AWS Deployment](./docs/deployment/AWS.md)
- [Azure Deployment](./docs/deployment/AZURE.md)
- [Monitoring & Logging](./docs/MONITORING.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)

### Developer Guides
- [Contributing Guide](./CONTRIBUTING.md)
- [Development Setup](./docs/DEVELOPMENT.md)
- [API Development](./docs/API_DEVELOPMENT.md)
- [Custom Connectors](./docs/CUSTOM_CONNECTORS.md)
- [Testing Guide](./docs/TESTING.md)

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Security Devices                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Palo Alto│  │ Entra ID │  │   SIEM   │  │  Falcon  │  ...   │
│  │   NGFW   │  │  (Azure) │  │ (Splunk) │  │   EDR    │        │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘        │
└────────┼─────────────┼─────────────┼─────────────┼──────────────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Device Connectors       │
         │  (API Integration Layer)  │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Event Ingestion         │
         │  & Normalization          │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Correlation Engine      │
         │  - Multi-phase detection  │
         │  - Entity tracking        │
         │  - Confidence scoring     │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Incident Management     │
         │  - Case creation          │
         │  - Enrichment             │
         │  - Assignment             │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   SOAR Playbook Engine    │
         │  - Response automation    │
         │  - Multi-device actions   │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   REST API & UI           │
         │  - Dashboard              │
         │  - Investigation tools    │
         │  - Configuration          │
         └───────────────────────────┘
```

### Technology Stack

**Backend**
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary data store
- **Celery** - Background task processing
- **Redis** - Task queue and caching

**Frontend**
- **React 18** - UI library
- **TypeScript** - Type safety
- **Material-UI (MUI)** - Component library
- **Recharts** - Data visualization
- **Axios** - HTTP client

**Infrastructure**
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Kubernetes** - Production orchestration
- **Terraform** - Infrastructure as Code
- **GitHub Actions** - CI/CD

---

## 🎯 Key Components

### 1. Device Connectors
Integrate with security infrastructure to collect events and execute actions.

**Supported Platforms:**
- Palo Alto Networks NGFW
- Microsoft Entra ID (Azure AD)
- Splunk Enterprise
- Elasticsearch SIEM
- CrowdStrike Falcon (coming soon)
- More via plugin architecture

### 2. Correlation Engine
Multi-phase attack detection engine that connects events across time and systems.

**Features:**
- Entity-based correlation (user, host, IP, file)
- Temporal windowing (5 min - 24 hours)
- Confidence scoring
- MITRE ATT&CK alignment

### 3. Operational Models
Pre-built detection patterns for common attack scenarios.

**Included Models:**
1. **Ransomware** - Delivery → Execution → Encryption → Impact
2. **Data Theft** - Collection → Staging → Exfiltration → Cloud Upload
3. **Intrusion** - Foothold → Privilege Abuse → Lateral Movement → Persistence
4. **Financial Fraud** - Compromise → Transaction → Exfiltration → Impact
5. **Denial of Service** - Flood → Degradation → Exhaustion → Mitigation
6. **Malware** - Delivery → Execution → C2 → Propagation → Persistence
7. **Supply Chain** - Vendor Entry → Execution → Persistence → Impact
8. **Insider Threat** - Access → Collection → Exfiltration → Impact
9. **Credential Abuse** - Access → Escalation → Persistence → Lateral Movement
10. **Misconfiguration** - Drift → Exposure → Exploitation → Impact

### 4. SOAR Playbooks
Automated response actions based on detected threats.

**Playbook Types:**
- **Endpoint Containment** - Isolate hosts, kill processes, capture forensics
- **Identity Lockdown** - Disable accounts, revoke sessions, reset MFA
- **Network Containment** - Block IPs/domains, enable PCAP, rate limit
- **Cloud Mitigation** - Revoke keys, lock resources, snapshot for forensics
- **Notification** - Create tickets, alert teams, escalate to leadership

---

## 🚢 Deployment Options

SOaC Framework supports multiple deployment scenarios:

### 🐳 Docker Compose (Development & Small Production)
Perfect for testing, small teams, or single-server deployments.

```bash
docker-compose up --build
```

**Pros:** Simple, self-contained, easy to manage
**Best for:** Development, POC, small teams (<10 users)

### ☁️ Railway.app (Free Cloud Hosting)
One-click deployment with free PostgreSQL included.

```bash
./deploy-to-railway.sh
```

**Pros:** Free tier, automatic HTTPS, managed database
**Best for:** Testing, demos, small production deployments

### ☁️ AWS (Production)
Full production deployment with CloudFormation or Terraform.

```bash
./scripts/deploy-aws.sh
```

**Includes:**
- ECS/Fargate for containers
- RDS PostgreSQL for database
- Application Load Balancer
- CloudWatch monitoring
- Auto-scaling

**Best for:** Enterprise production, high availability

### ☁️ Azure (Production)
Deploy to Azure with ARM templates or Terraform.

**Includes:**
- Azure Container Instances
- Azure Database for PostgreSQL
- Application Gateway
- Azure Monitor

**Best for:** Microsoft-centric organizations

### ☸️ Kubernetes (Production)
Deploy to any Kubernetes cluster (EKS, AKS, GKE, on-premises).

```bash
kubectl apply -f k8s/
```

**Best for:** Large scale, multi-tenant, complex environments

**See:** [Complete Deployment Guide](./docs/DEPLOYMENT.md)

---

## 📁 Project Structure

```
soac-framework/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── connectors/        # Device API clients
│   │   │   ├── base_connector.py
│   │   │   ├── paloalto_connector.py
│   │   │   ├── entraid_connector.py
│   │   │   └── siem_connector.py
│   │   ├── models/            # Database models
│   │   │   ├── device.py
│   │   │   ├── rule.py
│   │   │   ├── event.py
│   │   │   ├── incident.py
│   │   │   └── user.py
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth_routes.py
│   │   │   ├── device_routes.py
│   │   │   ├── rule_routes.py
│   │   │   ├── event_routes.py
│   │   │   ├── incident_routes.py
│   │   │   └── detection_routes.py
│   │   ├── services/          # Business logic
│   │   │   ├── sync_service.py
│   │   │   ├── event_ingestion.py
│   │   │   ├── correlation_engine.py
│   │   │   └── playbook_executor.py
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── main.py            # FastAPI app
│   │   ├── database.py        # Database config
│   │   └── auth.py            # Authentication
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend container
│
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Devices.tsx
│   │   │   ├── Rules.tsx
│   │   │   ├── Events.tsx
│   │   │   ├── Incidents.tsx
│   │   │   └── OperationalModels.tsx
│   │   ├── services/          # API services
│   │   ├── contexts/          # React contexts
│   │   └── types/             # TypeScript types
│   ├── package.json           # Node dependencies
│   └── Dockerfile             # Frontend container
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md
│   ├── DEVICE_INTEGRATION.md
│   ├── OPERATIONAL_MODELS.md
│   ├── SOAR_PLAYBOOKS.md
│   ├── deployment/            # Deployment guides
│   │   ├── DOCKER.md
│   │   ├── KUBERNETES.md
│   │   ├── AWS.md
│   │   └── AZURE.md
│   ├── use-cases/             # Use case documentation
│   │   ├── RANSOMWARE.md
│   │   ├── DATA_THEFT.md
│   │   ├── INTRUSION.md
│   │   ├── FRAUD.md
│   │   └── DOS.md
│   └── images/                # Documentation images
│
├── scripts/                    # Deployment & utility scripts
│   ├── deploy-aws.sh          # AWS CloudFormation deployment
│   ├── deploy-azure.sh        # Azure ARM deployment
│   ├── deploy-k8s.sh          # Kubernetes deployment
│   └── init-db.sh             # Database initialization
│
├── k8s/                        # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── postgres-statefulset.yaml
│   └── ingress.yaml
│
├── terraform/                  # Terraform IaC
│   ├── aws/                   # AWS infrastructure
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── azure/                 # Azure infrastructure
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml             # Continuous Integration
│       ├── cd.yml             # Continuous Deployment
│       ├── test.yml           # Automated testing
│       └── security.yml       # Security scanning
│
├── data/                       # Sample & mock data
│   ├── operational_models/    # Detection models
│   ├── threat_actors/         # Threat intelligence
│   ├── sample_rules/          # Example rules
│   └── mock_events/           # Test events
│
├── tests/                      # Test suites
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── e2e/                   # End-to-end tests
│
├── docker-compose.yml          # Docker Compose config
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
└── README.md                   # This file
```

---

## 🔐 Security Considerations

### Production Deployment Checklist

- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY (64+ characters)
- [ ] Enable HTTPS/TLS for all connections
- [ ] Use managed secrets (AWS Secrets Manager, Azure Key Vault)
- [ ] Configure CORS properly (restrict origins)
- [ ] Enable database encryption at rest
- [ ] Set up backup and disaster recovery
- [ ] Configure network security groups/firewall rules
- [ ] Enable audit logging
- [ ] Implement rate limiting
- [ ] Use non-root containers
- [ ] Regular security updates and patching
- [ ] Implement least privilege access
- [ ] Enable MFA for admin accounts
- [ ] Regular security assessments

**See:** [Security Best Practices](./docs/SECURITY.md)

---

## 🧪 Testing

SOaC Framework includes comprehensive testing:

### Run Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# End-to-end tests
npm run test:e2e
```

### Mock Mode

Test without real device credentials:

```bash
# Enable mock mode
export MOCK_MODE=true

# Start application
docker-compose up
```

Mock mode provides realistic simulated data for all device types.

---

## 🤝 Contributing

We welcome contributions from the community!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Setup

```bash
# Clone repository
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Setup frontend
cd ../frontend
npm install

# Run tests
pytest  # Backend
npm test  # Frontend
```

**See:** [Contributing Guide](./CONTRIBUTING.md)

---

## 📊 Roadmap

### Version 1.1 (Q2 2025)
- [ ] CrowdStrike Falcon EDR integration
- [ ] AWS CloudTrail integration
- [ ] Threat intelligence enrichment (MISP, TAXII)
- [ ] Advanced analytics and ML-based anomaly detection
- [ ] Multi-tenancy support

### Version 1.2 (Q3 2025)
- [ ] ServiceNow ITSM integration
- [ ] Slack/Teams notifications
- [ ] Custom playbook builder UI
- [ ] Advanced threat hunting queries
- [ ] Compliance reporting (SOC 2, ISO 27001)

### Version 2.0 (Q4 2025)
- [ ] AI-powered incident response recommendations
- [ ] Automated threat hunting
- [ ] Advanced behavioral analytics
- [ ] GraphQL API
- [ ] Mobile application

**See full roadmap:** [ROADMAP.md](./ROADMAP.md)

---

## 📝 License

SOaC Framework is licensed under the **MIT License**.

Copyright © 2025 SOaC Framework Team

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

**See:** [LICENSE](./LICENSE) for full text.

---

## 🙏 Acknowledgments

SOaC Framework builds upon best practices from:
- **MITRE ATT&CK Framework** - Threat taxonomy and techniques
- **NIST Cybersecurity Framework** - Security operations methodology
- **OWASP** - Security best practices
- **SIGMA Rules** - Detection rule format inspiration
- **Open-source community** - Libraries and tools

Special thanks to all contributors and the security community.

---

## 📞 Support & Community

### Get Help

- **Documentation**: [docs/](./docs/)
- **GitHub Issues**: [Report bugs or request features](https://github.com/ge0mant1s/soac-framework/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/ge0mant1s/soac-framework/discussions)

### Stay Updated

- ⭐ **Star this repository** to follow updates
- 👀 **Watch releases** for version notifications
- 🐦 **Follow us** (coming soon)

### Commercial Support

For enterprise support, custom development, or consulting:
- Email: support@soacframework.org (coming soon)
- Website: https://soacframework.org (coming soon)

---

## ⚠️ Important Localhost Notice

**This localhost refers to localhost of the computer that I'm using to run the application, not your local machine. To access it locally or remotely, you'll need to deploy the application on your own system.**

Follow the [deployment instructions](#-deployment-options) to run on your infrastructure.

---

<div align="center">

**Built with ❤️ by the SOaC Framework Team**

[Documentation](./docs/) •
[Quick Start](#-quick-start) •
[Deployment](#-deployment-options) •
[Contributing](./CONTRIBUTING.md) •
[License](./LICENSE)

Copyright © 2025 SOaC Framework Team. All rights reserved.

</div>
