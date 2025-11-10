# Security Operations as Code (SOaC) Framework v0.1.0

![License](https://img.shields.io/badge/license-Dual%20License-blue)
![Version](https://img.shields.io/badge/version-0.1.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)

## 🚀 Overview

**Security Operations as Code (SOaC)** is a comprehensive framework that transforms security operations into code-driven, automated, and scalable processes. SOaC unifies detection engineering, incident response, threat intelligence, and security orchestration into a single, cohesive platform.

### Key Features

- 🔍 **Universal Detection Engine** - Write once, deploy everywhere with CQL (Common Query Language)
- 🤖 **AI-Powered Assistant** - Intelligent security operations support with natural language processing
- 📊 **Modern Web Dashboard** - Real-time visibility and control over your security operations
- 🔗 **21+ Platform Integrations** - Seamless connectivity with major security tools
- 🎯 **Incident Management** - Complete lifecycle management with SLA tracking
- 🌊 **Real-Time Streaming** - Continuous detection and automated response
- 📈 **Threat Intelligence** - Integrated TI enrichment and correlation
- 🐳 **Docker Ready** - Deploy in minutes with Docker Compose

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web UI Dashboard                        │
│              (React + Modern UI Components)                 │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      REST API Layer                         │
│                   (Flask + Authentication)                  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    AI Assistant Engine                       │
│         (NLP + Context-Aware Security Intelligence)          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Core SOaC Engine                       │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │ CQL Engine   │ Incident Mgmt│ Deployment Manager       │ │
│  ├──────────────┼──────────────┼──────────────────────────┤ │
│  │ Correlation  │ Orchestrator │ Threat Intelligence      │ │
│  ├──────────────┴──────────────┴──────────────────────────┤ │
│  │          Platform Integration Layer (21+ Tools)        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Supported Platforms

### SIEM & Log Management
- Splunk, Elastic, QRadar, LogRhythm, Sumo Logic, Azure Sentinel

### EDR & XDR
- CrowdStrike, SentinelOne, Microsoft Defender, Carbon Black, Cortex XDR

### Network Security
- Palo Alto Networks, Cisco Secure, Fortinet, Zscaler

### Cloud Security
- AWS Security Hub, Azure Security Center, Google Cloud SCC

### Identity & Access
- Okta, Azure AD/Entra ID, Ping Identity

### Threat Intelligence
- MISP, ThreatConnect, Anomali, VirusTotal

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local development)
- Node.js 16+ (for Web UI development)

### Deploy with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/soac-framework.git
cd soac-framework

# Configure your environment
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your platform credentials

# Start all services
docker-compose up -d

# Access the Web UI
open http://localhost:3000

# Access the API
curl http://localhost:5000/api/health
```

### Manual Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Web UI dependencies
cd web_ui
npm install
npm run build
cd ..

# Run the API server
python api/app.py

# In another terminal, run the Web UI
cd web_ui
npm start
```

## 📚 Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [CQL Language Reference](docs/cql_reference.md)
- [Platform Integration Guide](docs/integrations.md)
- [API Documentation](docs/api_reference.md)
- [Operational Models](docs/operational_models/)
- [Use Case Development](docs/use_case_development.md)

## 🎓 Examples

### Example 1: Create a Detection Rule

```python
from core.engines.cql_engine import CQLEngine

cql_query = '''
#event.category = authentication
event.outcome = failure
groupBy([user.name, source.ip], function=count(as="failures"))
failures >= 10
'''

engine = CQLEngine()
results = engine.execute(cql_query, platform="splunk")
```

### Example 2: Deploy Rules Across Platforms

```python
from core.deployment_manager import DeploymentManager

manager = DeploymentManager()
manager.deploy_rule(
    rule_id="AUTH-001",
    platforms=["splunk", "sentinel", "crowdstrike"]
)
```

### Example 3: Create an Incident

```python
from core.incident_manager import IncidentManager

incident_mgr = IncidentManager()
incident = incident_mgr.create_incident(
    title="Brute Force Attack Detected",
    severity="high",
    use_case="Intrusion",
    source_alert={"rule": "AUTH-001", "matches": 150}
)
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Community vs Enterprise

- **Community Edition** (Apache 2.0): Core detection engine, basic integrations, CLI tools
- **Enterprise Edition** (Commercial): Advanced AI, full platform integrations, Web UI, priority support

## 📄 License

This project uses a dual-license model:
- **Community Edition**: Apache License 2.0
- **Enterprise Edition**: Commercial License

See [LICENSE](LICENSE) for details.

## 🛣️ Roadmap

### v0.2.0 (Q4 2025)
- [ ] SOAR playbook automation
- [ ] Advanced ML-based anomaly detection
- [ ] Mobile app for incident management
- [ ] Kubernetes operator

### v0.3.0 (Q1 2026)
- [ ] Multi-tenancy support
- [ ] Compliance reporting (SOC2, ISO27001)
- [ ] Custom dashboard builder
- [ ] Threat hunting workbench

## 💬 Community & Support

- **Documentation**: [https://docs.soacframe.io](https://docs.soacframe.io)
- **Community Forum**: [https://community.soacframe.io](https://community.soacframe.io)
- **Discord**: [Join our Discord](https://discord.gg/JsDBq6fM)
- **Email**: support@soacframe.io

## 🙏 Acknowledgments

Built with modern security operations best practices and inspired by:
- MITRE ATT&CK Framework
- Sigma Detection Rules
- OCSF (Open Cybersecurity Schema Framework)
- Detection-as-Code principles

## ⭐ Star History

If you find SOaC useful, please consider giving us a star! ⭐

---

**Made with ❤️ by the SOaC Community**
