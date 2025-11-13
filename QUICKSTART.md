
# Quick Start Guide

Get up and running with SOaC Framework in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- pip
- Git

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/soac-framework.git
cd soac-framework

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Activate virtual environment
source venv/bin/activate
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/soac-framework.git
cd soac-framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p logs config

# Copy configuration template
cp config/config_template.json config/config.json
```

## Configuration

Edit `config/config.json` with your API credentials:

```json
{
  "integrations": {
    "falcon": {
      "client_id": "YOUR_FALCON_CLIENT_ID",
      "client_secret": "YOUR_FALCON_CLIENT_SECRET"
    },
    "entraid": {
      "tenant_id": "YOUR_TENANT_ID",
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    }
  }
}
```

## Running the Framework

### Run the demo

```bash
python app.py
```

This will:
1. Load configuration
2. Process security rules
3. Generate reports
4. Run a demonstration of threat detection and response

### Run individual modules

```bash
# Test correlation engine
python src/correlation_engine.py

# View use cases
python src/use_case_manager.py

# View threat intelligence
python src/threat_intelligence.py

# Test SOAR playbooks
python src/soar_playbooks.py
```

### Run tests

```bash
pytest tests/ -v
```

## Quick Examples

### Example 1: Correlate Events

```python
from correlation_engine import CorrelationEngine

config = {'confidence_threshold': 3}
engine = CorrelationEngine(config)

# Sample events
events = [
    {
        'event_type': 'ProcessRollup2',
        'source': 'Falcon',
        'UserName': 'john.doe',
        'ComputerName': 'LAPTOP-001',
        'CommandLine': 'powershell.exe -enc ABC123'
    },
    # ... more events
]

# Correlate for ransomware pattern
incidents = engine.correlate_events(events, pattern_id='R1')
print(f"Detected {len(incidents)} incidents")
```

### Example 2: List Use Cases

```python
from use_case_manager import UseCaseManager

manager = UseCaseManager(config={})

# List all active use cases
for uc in manager.list_use_cases():
    print(f"{uc['id']}: {uc['title']}")

# Generate coverage report
report = manager.get_coverage_report()
print(f"MITRE Techniques Covered: {report['unique_techniques_covered']}")
```

### Example 3: Execute SOAR Playbook

```python
from soar_playbooks import SOARPlaybookManager

soar = SOARPlaybookManager(config={})

# Sample incident
incident = {
    'incident_id': 'INC-001',
    'pattern_id': 'R1',
    'entity_key': 'user:john.doe|computer:LAPTOP-001'
}

# Execute ransomware response playbook
result = soar.execute_playbook('PB-R1-RANSOMWARE', incident)
print(f"Playbook Status: {result['status'].value}")
```

## What's Next?

1. **Read the Documentation**: Check out the [docs/](docs/) folder for detailed information
2. **Configure Integrations**: Set up your security tool integrations
3. **Customize Use Cases**: Adapt the use cases to your environment
4. **Deploy to Production**: Follow the deployment guide in the documentation

## Troubleshooting

### Virtual environment not activating
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Module not found errors
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

### Permission denied on setup.sh
```bash
chmod +x scripts/setup.sh
```

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/soac-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/soac-framework/discussions)

---

**Happy Hunting! 🎯**

*SOaC Framework Team*
