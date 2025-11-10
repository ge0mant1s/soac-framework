# Contributing to SOaC Framework

First off, thank you for considering contributing to the Security Operations as Code (SOaC) Framework! 🎉

It's people like you that make SOaC such a great tool for the security community.

## Table of Contents

* [Code of Conduct](#code-of-conduct)

* [How Can I Contribute?](#how-can-i-contribute)

  * [Reporting Bugs](#reporting-bugs)

  * [Suggesting Enhancements](#suggesting-enhancements)

  * [Contributing Detection Rules](#contributing-detection-rules)

  * [Contributing Code](#contributing-code)

  * [Improving Documentation](#improving-documentation)

* [Development Setup](#development-setup)

* [Pull Request Process](#pull-request-process)

* [Style Guidelines](#style-guidelines)

* [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to fostering an open and welcoming environment. By participating, you are expected to uphold this code:

* **Be respectful** and inclusive

* **Be collaborative** and constructive

* **Focus on what is best** for the community

* **Show empathy** towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Use this template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Ubuntu 22.04]
 - Python Version: [e.g. 3.9.7]
 - SOaC Version: [e.g. 0.1.0]
 - Platform: [e.g. Splunk, Sentinel]

**Additional context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

* **Clear title** and description

* **Use case** - Why is this enhancement needed?

* **Proposed solution** - How should it work?

* **Alternatives considered** - What other solutions did you consider?

* **Additional context** - Screenshots, mockups, examples

### Contributing Detection Rules

Detection rules are the heart of SOaC! We welcome contributions of:

* **New detection rules** in CQL format

* **Platform-specific translations** for existing rules

* **Rule improvements** and optimizations

* **MITRE ATT&CK mappings**

**Detection Rule Contribution Guidelines:**

1. **Use CQL format** for universal compatibility

2. **Include metadata:**

  * Title and description

  * MITRE ATT&CK technique(s)

  * Severity level

  * Use case category (Intrusion, Malware, Data Theft, etc.)

  * False positive considerations

3. **Provide test cases** when possible

4. **Document response actions**

5. **Include platform translations** for at least 2 platforms

**Example structure:**

```markdown
# Rule: [Rule Name]

## Metadata
- **ID**: RULE-XXX
- **Severity**: High
- **MITRE ATT&CK**: T1110 (Brute Force)
- **Use Case**: Intrusion
- **Author**: Your Name
- **Date**: 2025-01-15

## CQL Query
```cql
#event.category = authentication
event.outcome = failure
groupBy([user.name, source.ip], function=count(as="failures"))
failures >= 10
```

## Description

Detects potential brute force attacks...

## Response Actions

1. Investigate source IP

2. Check for successful logins

3. Consider blocking IP

4. Reset credentials if compromised

## False Positives

* Legitimate users with forgotten passwords

* Automated systems with misconfigured credentials

## Platform Translations

### Splunk

```spl
...
```

### Azure Sentinel

```kql
...
```

```

Place your rule in: `examples/detection_rules/[category]/[rule-name].md`

### Contributing Code

We love code contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Write or update tests**
5. **Ensure all tests pass** (`pytest`)
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to your branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

**What to contribute:**

- 🐛 Bug fixes
- ✨ New features
- 🔌 Platform integrations
- 🧪 Test coverage improvements
- 📊 Performance optimizations
- 🔒 Security enhancements

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or clarify existing docs
- Add examples and tutorials
- Translate documentation
- Create video tutorials
- Write blog posts about SOaC

## Development Setup

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Git
- Node.js 16+ (for Web UI development)

### Local Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/soac-framework.git
cd soac-framework

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# 4. Install pre-commit hooks
pre-commit install

# 5. Copy configuration
cp config/config.example.yaml config/config.yaml

# 6. Run tests
pytest

# 7. Start development server
python api/app.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov=api --cov-report=html

# Run specific test file
pytest tests/test_cql_engine.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Format code with Black
black core/ api/ ai_assistant/

# Lint with flake8
flake8 core/ api/ ai_assistant/

# Type checking with mypy
mypy core/ api/

# Run all checks
make lint  # If Makefile is available
```

## Pull Request Process

1. **Update documentation** - Ensure [README.md](http://README.md) and relevant docs are updated

2. **Add tests** - New features should include tests

3. **Update CHANGELOG** - Add your changes to [CHANGELOG.md](http://CHANGELOG.md) (if exists)

4. **Follow style guidelines** - Use Black for Python, ESLint for JavaScript

5. **One feature per PR** - Keep PRs focused and manageable

6. **Write clear commit messages** - Use conventional commits format

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

* `feat`: New feature

* `fix`: Bug fix

* `docs`: Documentation changes

* `style`: Code style changes (formatting, etc.)

* `refactor`: Code refactoring

* `test`: Adding or updating tests

* `chore`: Maintenance tasks

**Examples:**

```
feat(cql): add support for Chronicle platform

fix(incident): resolve SLA calculation bug

docs(readme): update installation instructions

test(api): add integration tests for incident endpoints
```

### PR Title Format

```
[Type] Brief description of changes
```

Examples:

* `[Feature] Add support for Fortinet FortiGate integration`

* `[Fix] Resolve CQL parsing error for nested groupBy`

* `[Docs] Add tutorial for custom detection rules`

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## How Has This Been Tested?
Describe the tests you ran and how to reproduce them.

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Screenshots (if applicable)
Add screenshots to help explain your changes.
```

## Style Guidelines

### Python Style Guide

* Follow [PEP 8](https://pep8.org/)

* Use [Black](https://black.readthedocs.io/) for code formatting (line length: 100)

* Use type hints for function signatures

* Write docstrings for all public functions/classes (Google style)

* Keep functions focused and small (< 50 lines ideally)

**Example:**

```python
def create_incident(
    self, 
    title: str, 
    severity: str, 
    use_case: str, 
    **kwargs
) -> Incident:
    """
    Create a new security incident.
    
    Args:
        title: Brief description of the incident
        severity: Severity level (critical, high, medium, low)
        use_case: Use case category (Intrusion, Malware, etc.)
        **kwargs: Additional incident attributes
        
    Returns:
        Incident: The created incident object
        
    Raises:
        ValueError: If severity is invalid
        
    Example:
        >>> incident = manager.create_incident(
        ...     title="Brute Force Detected",
        ...     severity="high",
        ...     use_case="Intrusion"
        ... )
    """
    # Implementation
```

### JavaScript/React Style Guide

* Use ES6+ syntax

* Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

* Use functional components with hooks

* Use ESLint and Prettier

* Write JSDoc comments for complex functions

### CQL Style Guide

* Use lowercase for keywords

* Indent nested expressions

* One condition per line

* Use meaningful field names

* Add comments for complex logic

```cql
# Good
#event.category = authentication
event.outcome = failure
groupBy([user.name, source.ip], function=count(as="failures"))
failures >= 10

# Avoid
#event.category=authentication event.outcome=failure groupBy([user.name,source.ip],function=count(as="failures")) failures>=10
```

## Platform Integration Guidelines

When adding a new platform integration:

1. **Create connector class** in `core/integrations/platforms/`

2. **Implement required methods:**

  * `authenticate()` - Handle authentication

  * `execute_query()` - Execute translated queries

  * `deploy_rule()` - Deploy detection rules

  * `get_events()` - Retrieve events

  * `health_check()` - Check platform connectivity

3. **Add CQL translator** in `core/engines/cql_engine.py`

4. **Write tests** in `tests/integrations/`

5. **Update documentation** in `docs/integrations/`

6. **Add example** in `examples/`

## Testing Guidelines

* **Write tests for all new features**

* **Maintain test coverage above 80%**

* **Use pytest fixtures** for common setup

* **Mock external API calls**

* **Test edge cases and error conditions**

```python
# Example test
def test_create_incident():
    """Test incident creation with valid data."""
    manager = IncidentManager()
    incident = manager.create_incident(
        title="Test Incident",
        severity="high",
        use_case="Intrusion"
    )
    
    assert incident.title == "Test Incident"
    assert incident.severity == "high"
    assert incident.status == "new"
```

## Documentation Guidelines

* Use **Markdown** for all documentation

* Include **code examples** where applicable

* Add **screenshots** for UI features

* Keep language **clear and concise**

* Update **table of contents** when adding sections

* Link to **related documentation**

## Community

### Getting Help

* 💬 **GitHub Discussions** - Ask questions and share ideas

* 🐛 **GitHub Issues** - Report bugs and request features

* 💼 **Discord** - Join our community chat

* 📧 **Email** - [support@soacframe.io](mailto:support@soacframe.io)

### Recognition

Contributors will be recognized in:

* **[README.md](http://README.md)** - Contributors section

* **Release notes** - Feature credits

* **Hall of Fame** - Top contributors page (coming soon)

### Contributor License Agreement

By contributing to SOaC Framework, you agree that your contributions will be licensed under the same license as the project (Apache 2.0 for Community Edition).

## Questions?

Don't hesitate to ask! We're here to help:

* Open a [GitHub Discussion](https://github.com/ge0mant1s/soac-framework/discussions)

* Join our [Discord community](https://discord.gg/soac)

* Email us at [support@soacframe.io](mailto:support@soacframe.io)

---

## Thank You! 🙏

Your contributions make SOaC better for everyone. We appreciate your time and effort!

**Happy Contributing!** 🚀

---

_Last updated: 2025-01-15_