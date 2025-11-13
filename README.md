# SOaC Framework - Security Operations as Code

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**A comprehensive, threat-centric security operations framework for modern enterprises**

## 🎯 Overview

The SOaC (Security Operations as Code) Framework is a production-ready security operations platform that implements a unified, intelligence-driven detection and response architecture. It integrates identity, endpoint, network, cloud, and application telemetry into a single, correlated defense fabric.

### Key Features

- **🔗 Multi-Source Correlation**: Correlate events across Falcon EDR, EntraID, PaloAlto NGFW, Umbrella, CloudTrail, and more
- **🎭 Threat Intelligence Integration**: Pre-loaded profiles for LockBit, Clop, APT29, APT41, and other major threat actors
- **🤖 Automated Response (SOAR)**: 6+ pre-built playbooks for ransomware, data exfiltration, intrusion, fraud, malware, and DoS
- **📊 10 Security Use Cases**: Complete coverage from ransomware to financial fraud
- **🎯 MITRE ATT&CK Mapping**: Full tactical alignment with ATT&CK framework
- **📈 MAGMA Framework**: Structured use case management from mission to action

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   SOaC Framework Core                       │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ Correlation  │  │  Use Case    │  │   Threat Intel  │    │
│  │   Engine     │  │  Manager     │  │    Module       │    │
│  └──────────────┘  └──────────────┘  └─────────────────┘    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │    SOAR      │  │    Config    │  │    Detection    │    │
│  │  Playbooks   │  │  Processor   │  │     Rules       │    │
│  └──────────────┘  └──────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │                    │                    │
    ┌────┴────┐          ┌────┴────┐         ┌────┴────┐
    │ Falcon  │          │ EntraID │         │PaloAlto │
    │   EDR   │          │   IAM   │         │  NGFW   │
    └─────────┘          └─────────┘         └─────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/soac-framework.git
cd soac-framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Copy and configure settings
cp config/config_template.json config/config.json
# Edit config/config.json with your API credentials
```

### Running the Framework

```bash
# Run the main application
python app.py

# Run specific tests
python -m pytest tests/

# Run individual modules
python src/correlation_engine.py
python src/use_case_manager.py
python src/threat_intelligence.py
```

## 📁 Project Structure

```
soac-framework/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── correlation_engine.py  # Multi-source event correlation
│   ├── config_processor.py    # Process EntraID/PaloAlto configs
│   ├── use_case_manager.py    # MAGMA framework implementation
│   ├── soar_playbooks.py      # Automated response playbooks
│   └── threat_intelligence.py # Threat actor profiles & IOCs
│
├── config/                     # Configuration files
│   ├── config_template.json   # Configuration template
│   ├── entraid_rules.json     # Generated EntraID rules
│   ├── paloalto_rules.json    # Generated PaloAlto rules
│   ├── use_cases.json         # Use case definitions
│   └── threat_actors.json     # Threat actor database
│
├── data/                       # Data files
│   ├── EntraID_Authentication_Rules.xlsx
│   ├── PaloAlto_NGFW_Rules.xlsx
│   └── samples/               # Sample data for testing
│       ├── entraid_rules_sample.xlsx
│       └── paloalto_rules_sample.xlsx
│
├── docs/                       # Documentation
│   ├── FRAMEWORK_OVERVIEW.md
│   ├── USE_CASES.md
│   ├── OPERATIONAL_MODELS.md
│   ├── THREAT_LANDSCAPE.md
│   └── API_REFERENCE.md
│
├── playbooks/                  # SOAR playbook definitions
│   ├── ransomware_response.md
│   ├── data_exfiltration.md
│   ├── intrusion_response.md
│   └── fraud_response.md
│
├── sigma_rules/                # SIGMA detection rules
│   └── (Generated from use cases)
│
├── scripts/                    # Utility scripts
│   ├── setup.sh
│   └── generate_reports.py
│
├── tests/                      # Unit and integration tests
│   ├── test_correlation_engine.py
│   ├── test_use_case_manager.py
│   └── test_soar_playbooks.py
│
└── logs/                       # Application logs
    └── soac_framework.log
```

## 🎯 Core Components

### 1. Correlation Engine

Multi-source event correlation based on the strategic correlation model:

```python
from correlation_engine import CorrelationEngine

engine = CorrelationEngine(config)
incidents = engine.correlate_events(events, pattern_id='R1')
```

**Correlation Patterns:**
- `R1`: Ransomware Chain
- `D1`: Data Exfiltration
- `C1`: Credential Abuse
- `IN1`: Intrusion Chain
- `FF1`: Financial Fraud
- `M2`: Malware Infection
- `DOS1`: Denial of Service

### 2. Use Case Manager

Manages 10 security use cases through the MAGMA framework:

```python
from use_case_manager import UseCaseManager

manager = UseCaseManager(config)
coverage = manager.get_coverage_report()
```

**Use Cases:**
1. Ransomware
2. Data Theft / Exfiltration
3. Denial of Service
4. Supply Chain Attack
5. Intrusion / Lateral Movement
6. Malware
7. Misconfiguration / Poor Security
8. Social Engineering
9. Information Manipulation
10. Financial Theft & Fraud

### 3. SOAR Playbook Manager

Automated response playbooks for each threat scenario:

```python
from soar_playbooks import SOARPlaybookManager

soar = SOARPlaybookManager(config)
result = soar.execute_playbook('PB-R1-RANSOMWARE', incident)
```

**Available Playbooks:**
- `PB-R1-RANSOMWARE`: Ransomware containment (MTTI: 3 min)
- `PB-D1-EXFILTRATION`: Data exfiltration stop (MTTI: 5 min)
- `PB-IN1-INTRUSION`: Intrusion containment (MTTI: 10 min)
- `PB-FF1-FRAUD`: Financial fraud response (MTTI: 5 min)
- `PB-M2-MALWARE`: Malware eradication (MTTI: 3 min)
- `PB-DOS1-DOS`: DoS/DDoS mitigation (MTTI: 5 min)

### 4. Threat Intelligence

Pre-loaded threat actor profiles and IOC management:

```python
from threat_intelligence import ThreatIntelligence

ti = ThreatIntelligence(config)
actors = ti.list_threat_actors(actor_type='Cybercriminal')
```

**Tracked Threat Actors:**
- **Cybercriminals**: LockBit, Clop, FIN12
- **Nation-States**: APT29, APT41, Lazarus Group
- **Hacktivists**: KillNet, Anonymous
- **Insiders**: Malicious Insider profiles
- **Supply Chain**: UNC Groups

### 5. Configuration Processor

Process and convert security rules from Excel to operational formats:

```python
from config_processor import ConfigProcessor

processor = ConfigProcessor(data_dir='data')
entraid_rules = processor.load_entraid_rules('data/EntraID_Authentication_Rules.xlsx')
processor.export_to_json(output_dir='config')
```

## 📊 Use Case Coverage

| Use Case | MITRE Techniques | Severity | Status |
|----------|------------------|----------|--------|
| Ransomware | T1486, T1059.001, T1027 | Critical | ✅ Active |
| Data Theft | T1567.002, T1005 | High | ✅ Active |
| DoS | T1499 | High | ✅ Active |
| Supply Chain | T1195.002 | High | ✅ Active |
| Intrusion | T1021.001 | Critical | ✅ Active |
| Malware | T1055.001 | High | ✅ Active |
| Misconfiguration | T1552, T1078.003 | Medium | ✅ Active |
| Social Engineering | T1566.002, T1110.003 | High | ✅ Active |
| Info Manipulation | T1565.001, T1557 | Medium | ✅ Active |
| Financial Fraud | T1110, T1589.002, T1539 | Critical | ✅ Active |

**Total MITRE ATT&CK Coverage**: 18+ unique techniques across all tactics

## 🔧 Configuration

### Basic Configuration

Edit `config/config.json`:

```json
{
  "framework": {
    "name": "SOaC Framework",
    "organization": "SOaC Framework Team",
    "environment": "production"
  },
  "correlation": {
    "confidence_threshold": 3,
    "time_windows": {
      "real_time": 15,
      "short_term": 90,
      "long_term": 1440
    }
  },
  "integrations": {
    "falcon": {
      "api_url": "https://api.crowdstrike.com",
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    },
    "entraid": {
      "tenant_id": "YOUR_TENANT_ID",
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    }
  }
}
```

### Integration Setup

The framework supports integration with:

- **CrowdStrike Falcon**: EDR and Identity Protection
- **Microsoft EntraID**: Identity and Access Management
- **Palo Alto Networks**: NGFW and threat prevention
- **Cisco Umbrella**: DNS security and cloud firewall
- **AWS CloudTrail**: Cloud activity monitoring
- **Azure Activity Logs**: Azure resource monitoring
- **ServiceNow**: Incident management and ITSM

See `docs/INTEGRATION_GUIDE.md` for detailed setup instructions.

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_correlation_engine.py -v

# Run integration tests
pytest tests/integration/ -v
```

### Test Coverage

The framework includes comprehensive tests for:
- Correlation engine logic
- Use case management
- SOAR playbook execution
- Configuration processing
- Threat intelligence lookups

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Framework Overview](docs/FRAMEWORK_OVERVIEW.md)**: Strategic and tactical layers
- **[Use Cases](docs/USE_CASES.md)**: Detailed use case specifications
- **[Operational Models](docs/OPERATIONAL_MODELS.md)**: Detection and response workflows
- **[Threat Landscape](docs/THREAT_LANDSCAPE.md)**: Threat actors and TTPs
- **[API Reference](docs/API_REFERENCE.md)**: API documentation for all modules

## 🔐 Security Considerations

### Credentials Management

- **Never commit** API credentials to version control
- Use environment variables or secure vaults (e.g., HashiCorp Vault, AWS Secrets Manager)
- Rotate credentials regularly
- Apply principle of least privilege

### Data Privacy

- All sensitive data is excluded from git via `.gitignore`
- Sample data contains no real organizational information
- Follow GDPR/HIPAA guidelines for incident data retention

### Network Security

- Use TLS/SSL for all API communications
- Implement API rate limiting
- Monitor for anomalous API usage

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters
- Write docstrings for all public functions
- Maintain test coverage above 80%

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SOaC Framework Team** - Architecture and development
- **MITRE ATT&CK** - Threat modeling framework
- **SIGMA Project** - Detection rule format
- **CrowdStrike** - EDR integration patterns
- **Microsoft** - EntraID integration guidance

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/soac-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/soac-framework/discussions)

## 🗺️ Roadmap

### Version 0.2 (Planned)
- [ ] Machine learning-based anomaly detection
- [ ] REST API for external integrations
- [ ] Web-based dashboard
- [ ] Additional threat actor profiles

### Version 0.3 (Planned)
- [ ] Automated threat hunting capabilities
- [ ] Enhanced SOAR orchestration
- [ ] Multi-tenancy support
- [ ] Cloud-native deployment (Docker/Kubernetes)

---

**Made with ❤️ by SOaC Framework Team**

*Protecting organizations through intelligent, automated security operations*
