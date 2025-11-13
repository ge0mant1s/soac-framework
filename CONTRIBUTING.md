
# Contributing to SOaC Framework

Thank you for considering contributing to the SOaC Framework! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in [GitHub Issues](https://github.com/ge0mant1s/soac-framework/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Node version, etc.)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/soac-framework.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, maintainable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Backend
   cd backend && npm test
   
   # Frontend
   cd frontend && npm test
   ```

5. **Commit your changes**
   ```bash
   git commit -m "feat: add new feature description"
   ```
   
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes
   - `refactor:` - Code refactoring
   - `test:` - Test updates
   - `chore:` - Build/config changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference related issues
   - Include screenshots (if UI changes)

## Development Guidelines

### Code Style

- Use consistent indentation (2 spaces)
- Use meaningful variable and function names
- Keep functions small and focused
- Add JSDoc comments for functions
- Follow ESLint rules (when configured)

### Commit Messages

Good commit messages:
```
feat: add user authentication to dashboard
fix: resolve CORS issue in device API
docs: update setup guide with Docker instructions
```

Bad commit messages:
```
update
fixed stuff
changes
```

### Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for high code coverage

### Documentation

- Update README.md for major changes
- Add inline code comments
- Update API documentation
- Include setup instructions

## Code Review Process

1. All PRs require review
2. Address reviewer feedback
3. Maintain clean commit history
4. Squash commits if requested

## Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow code of conduct

## Getting Help

- Check [Documentation](docs/)
- Review [Issues](https://github.com/ge0mant1s/soac-framework/issues)
- Ask questions in discussions
- Contact: support@soacframe.io

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to SOaC Framework!**

SOaC Framework Team © 2025
