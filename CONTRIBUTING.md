
# Contributing to SOaC Framework

Thank you for your interest in contributing to the SOaC Framework! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers have the right to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that do not align with this Code of Conduct.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/ge0mant1s/soac-framework/issues) to avoid duplicates.

**When submitting a bug report, please include:**
- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** (if applicable)
- **Environment details**:
  - OS and version
  - Python version
  - Node.js version
  - Docker version (if applicable)
  - Deployment method (Docker Compose, K8s, etc.)
- **Error messages and logs**

**Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 22.04]
 - Python: [e.g. 3.11.5]
 - Docker: [e.g. 24.0.7]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When suggesting an enhancement, please include:**
- **Clear title and description**
- **Use case**: Why is this enhancement needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**
- **Additional context**: Mockups, examples, etc.

### Contributing Code

We love code contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Write tests** for your changes
5. **Ensure all tests pass**
6. **Commit your changes** (see [commit guidelines](#commit-guidelines))
7. **Push to your fork** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Contributing Documentation

Documentation improvements are always welcome!

- Fix typos and errors
- Improve clarity
- Add examples
- Create tutorials
- Translate documentation

Documentation is located in the `docs/` directory and uses Markdown format.

---

## Development Setup

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **Docker & Docker Compose** (optional, but recommended)
- **Git**

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup database
createdb soac_dev_db

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run development server
npm run dev
```

### Docker Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/ge0mant1s/soac-framework.git
cd soac-framework

# Start all services
docker-compose up --build
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**: `pytest` (backend), `npm test` (frontend)
4. **Run linters**:
   - Backend: `black app/`, `flake8 app/`, `mypy app/`
   - Frontend: `npm run lint`
5. **Update CHANGELOG.md** with your changes
6. **Rebase on latest main** branch

### Pull Request Guidelines

**Title**: Use a clear, descriptive title
- Good: "Add CrowdStrike Falcon connector"
- Bad: "Fix bug"

**Description**: Include:
- What changes you made
- Why you made these changes
- Related issue number (if applicable)
- Testing performed
- Screenshots (for UI changes)

**Template:**
```markdown
## Description
Brief description of changes

## Related Issue
Fixes #123

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] All tests pass

## Screenshots (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review performed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. At least one maintainer must approve
2. All CI checks must pass
3. No merge conflicts
4. Documentation is complete
5. Tests have good coverage

### After Merge

- Your changes will be included in the next release
- You'll be added to the contributors list
- Thank you! 🎉

---

## Coding Standards

### Python (Backend)

**Style Guide**: Follow [PEP 8](https://pep8.org/)

**Tools**:
- **Black**: Code formatter (line length: 120)
- **Flake8**: Linter
- **mypy**: Type checking

**Examples**:

```python
# Good
def process_event(event: Dict[str, Any]) -> Incident:
    """Process security event and create incident if needed.
    
    Args:
        event: Security event dictionary
        
    Returns:
        Incident object if created, None otherwise
    """
    # Implementation
    pass

# Bad
def process_event(event):
    # No docstring, no type hints
    pass
```

**Best Practices**:
- Use type hints everywhere
- Write docstrings for all public functions/classes
- Keep functions small and focused
- Use meaningful variable names
- Handle errors explicitly
- Log important operations

### TypeScript (Frontend)

**Style Guide**: Follow [TypeScript best practices](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)

**Tools**:
- **ESLint**: Linter
- **Prettier**: Code formatter

**Examples**:

```typescript
// Good
interface Device {
  id: string;
  name: string;
  type: DeviceType;
  status: DeviceStatus;
}

const fetchDevices = async (): Promise<Device[]> => {
  const response = await api.get<Device[]>('/devices');
  return response.data;
};

// Bad
const fetchDevices = async () => {
  const response = await api.get('/devices');
  return response.data;  // No type safety
};
```

**Best Practices**:
- Use TypeScript interfaces for data structures
- Avoid `any` type
- Use functional components with hooks
- Keep components small and reusable
- Use proper error handling
- Write meaningful component names

### Git Commit Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/)

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Examples**:

```bash
# Good
git commit -m "feat(detector): add ransomware detection model"
git commit -m "fix(api): resolve CORS issue for production"
git commit -m "docs(readme): update installation instructions"

# Bad
git commit -m "fix bug"
git commit -m "update stuff"
git commit -m "WIP"
```

**Multi-line commits**:
```bash
feat(soar): add endpoint containment playbook

- Implement Falcon EDR isolation
- Add rollback functionality
- Update decision matrix

Closes #42
```

---

## Testing Guidelines

### Backend Testing

**Framework**: pytest

**Test Structure**:
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   ├── test_connectors.py
│   └── test_correlation.py
└── conftest.py
```

**Running Tests**:
```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_models.py

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/unit/test_models.py::test_create_device
```

**Writing Tests**:

```python
import pytest
from app.models import Device

def test_create_device():
    """Test device creation"""
    device = Device(
        name="Test Device",
        type="paloalto",
        config={"hostname": "test.com"}
    )
    assert device.name == "Test Device"
    assert device.type == "paloalto"

@pytest.mark.asyncio
async def test_device_connector():
    """Test device connection"""
    connector = PaloAltoConnector(config)
    result = await connector.test_connection()
    assert result["status"] == "success"
```

**Coverage Target**: Aim for 80%+ code coverage

### Frontend Testing

**Framework**: Vitest + React Testing Library

**Test Structure**:
```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx
├── pages/
│   ├── Dashboard.tsx
│   └── Dashboard.test.tsx
└── services/
    ├── api.ts
    └── api.test.ts
```

**Running Tests**:
```bash
# All tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

**Writing Tests**:

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Integration Testing

Test API endpoints, database operations, and device connectors:

```python
def test_api_create_device(client, auth_headers):
    """Test device creation via API"""
    response = client.post(
        "/api/v1/devices",
        json={
            "name": "Test Device",
            "type": "paloalto",
            "config": {...}
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Device"
```

---

## Documentation

### Documentation Standards

- Use **Markdown** format
- Keep language **clear and concise**
- Include **code examples**
- Add **screenshots** for UI documentation
- Use **proper headings** hierarchy
- Link to related documentation

### Docstring Format (Python)

Use **Google style** docstrings:

```python
def correlate_events(events: List[Event], time_window: int) -> List[Incident]:
    """Correlate events to detect multi-phase attacks.
    
    Args:
        events: List of security events to correlate
        time_window: Time window in seconds for correlation
        
    Returns:
        List of detected incidents
        
    Raises:
        ValueError: If time_window is negative
        
    Example:
        >>> events = fetch_events()
        >>> incidents = correlate_events(events, 3600)
        >>> print(f"Found {len(incidents)} incidents")
    """
    pass
```

### JSDoc Format (TypeScript)

```typescript
/**
 * Fetch devices from the API
 * @param filters - Optional filters for device query
 * @returns Promise resolving to array of devices
 * @throws {ApiError} If API request fails
 * @example
 * ```typescript
 * const devices = await fetchDevices({ type: 'paloalto' });
 * ```
 */
async function fetchDevices(filters?: DeviceFilters): Promise<Device[]> {
  // Implementation
}
```

---

## Community

### Get Help

- **Documentation**: [docs/](./docs/)
- **GitHub Discussions**: [Ask questions](https://github.com/ge0mant1s/soac-framework/discussions)
- **GitHub Issues**: [Report bugs](https://github.com/ge0mant1s/soac-framework/issues)

### Stay Updated

- ⭐ **Star the repository** to show your support
- 👀 **Watch releases** for updates
- 🐦 **Follow us** (coming soon)

### Recognition

Contributors will be:
- Listed in [CONTRIBUTORS.md](./CONTRIBUTORS.md)
- Mentioned in release notes
- Recognized in the community

---

## License

By contributing to SOaC Framework, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

If you have questions about contributing, please:
1. Check the [documentation](./docs/)
2. Search [existing issues](https://github.com/ge0mant1s/soac-framework/issues)
3. Ask in [GitHub Discussions](https://github.com/ge0mant1s/soac-framework/discussions)
4. Contact the maintainers (coming soon)

---

**Thank you for contributing to SOaC Framework! 🙏**

---

*Last updated: November 14, 2025*
