# Contributing to Gmail Self-Mail Tool

Thank you for your interest in contributing to the Gmail Self-Mail Tool! This document provides guidelines and steps for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue with:
   - A clear title and description
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

1. Check if the enhancement has been suggested in the Issues section
2. If not, create a new issue with:
   - A clear title and description
   - Use case or problem you're trying to solve
   - Proposed solution
   - Alternatives considered

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-fix-name
   ```
3. Make your changes
4. Write/update tests if necessary
5. Update documentation if necessary
6. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a Pull Request

### Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/gmail-self-mail-tool.git
   cd gmail-self-mail-tool
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run tests:
   ```bash
   python -m pytest
   ```

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Write clear commit messages

### Testing

- Write tests for new features
- Update tests for bug fixes
- Ensure all tests pass before submitting PR
- Include test coverage information

### Documentation

- Update README.md if necessary
- Add/update docstrings
- Update API documentation
- Add comments for complex logic

## Review Process

1. All PRs will be reviewed by maintainers
2. Address any feedback and make requested changes
3. Once approved, your PR will be merged

## Questions?

If you have any questions, feel free to:
- Open an issue
- Contact the maintainers
- Join our community discussions

Thank you for contributing! 