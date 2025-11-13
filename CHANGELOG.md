# Changelog

All notable changes to the SOaC Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-13

### Added
- Initial release of SOaC Framework
- Multi-source correlation engine for threat detection
- 10 comprehensive security use cases (Ransomware, Data Theft, DoS, Supply Chain, Intrusion, Malware, Misconfiguration, Social Engineering, Information Manipulation, Financial Fraud)
- SOAR playbook manager with 6 pre-built playbooks
- Threat intelligence module with 10+ threat actor profiles
- Configuration processor for EntraID and PaloAlto NGFW rules
- Use case manager implementing MAGMA framework
- MITRE ATT&CK mapping for all use cases
- Comprehensive documentation (Framework Overview, Use Cases, Threat Landscape)
- Sample data and mock events for testing
- Unit tests for core components
- Setup script for easy installation
- Configuration templates for all integrations

### Security
- Secure credential management through environment variables
- API authentication for CrowdStrike Falcon, Microsoft EntraID, PaloAlto
- Data privacy features compliant with GDPR/HIPAA guidelines

### Documentation
- Comprehensive README with quick start guide
- Detailed framework overview (Strategic and Tactical layers)
- Use case specifications with MAGMA framework alignment
- Threat landscape documentation
- API reference for all modules
- Quick start guide for new users

### Integrations
- CrowdStrike Falcon EDR
- Microsoft EntraID (Identity and Access Management)
- Palo Alto Networks NGFW
- Cisco Umbrella (DNS Security)
- AWS CloudTrail
- Azure Activity Logs
- ServiceNow (ITSM)

## [Unreleased]

### Planned for v1.1
- Machine learning-based anomaly detection
- REST API for external integrations
- Web-based dashboard for visualization
- Additional threat actor profiles (Maze, Ryuk, etc.)
- Enhanced SIGMA rule generation

### Planned for v1.2
- Automated threat hunting capabilities
- Enhanced SOAR orchestration with more integrations
- Multi-tenancy support
- Cloud-native deployment (Docker/Kubernetes)
- Real-time streaming analytics

---

**Note**: This is the initial release. All references to "Straumann" in source documents have been replaced with "SOaC Framework Team" for generic deployment.
