# Contributing to xnLinkFinder-Z

First off, thank you for considering contributing to xnLinkFinder-Z! It's people like you that make xnLinkFinder-Z such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Testing Requirements](#testing-requirements)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed and what behavior you expected**
* **Include screenshots if relevant**
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List some examples of how it would be used**

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8, with Black formatting)
* Include tests for new functionality
* Update documentation as needed
* End all files with a newline

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/xnLinkFinder-Z.git
   cd xnLinkFinder-Z
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"  # Install in development mode with dev dependencies
   ```

4. **Install pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Run tests to verify setup**
   ```bash
   pytest tests/
   ```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   * Write clear, commented code
   * Follow the style guidelines
   * Add tests for new features
   * Update documentation

3. **Run the test suite**
   ```bash
   pytest tests/ -v
   ```

4. **Run code quality checks**
   ```bash
   black xnLinkFinder --check
   isort xnLinkFinder --check-only
   flake8 xnLinkFinder
   mypy xnLinkFinder
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
   
   Use conventional commit messages:
   * `feat:` for new features
   * `fix:` for bug fixes
   * `docs:` for documentation changes
   * `test:` for test additions/modifications
   * `refactor:` for code refactoring
   * `chore:` for maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   * Go to the original repository
   * Click "New Pull Request"
   * Select your branch
   * Fill out the PR template
   * Link any related issues

## Style Guidelines

### Python Code Style

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use [Black](https://github.com/psf/black) for code formatting (line length: 100)
* Use [isort](https://pycqa.github.io/isort/) for import sorting
* Use type hints where appropriate
* Write docstrings for all public modules, functions, classes, and methods
* Keep functions focused and small (ideally < 50 lines)

### Documentation Style

* Use Markdown for documentation files
* Keep line length reasonable (80-100 characters)
* Use code blocks with language specification
* Include examples where relevant

### Commit Message Guidelines

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Testing Requirements

* All new features must include tests
* Bug fixes should include a test that would have caught the bug
* Aim for at least 80% code coverage
* Tests should be fast (< 1 second per test ideally)
* Use pytest fixtures for test data
* Use meaningful test names that describe what is being tested

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=xnLinkFinder --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run tests matching a pattern
pytest -k "test_pattern"

# Run in verbose mode
pytest -v
```

## Code Review Checklist

Before requesting a review, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No unnecessary files are included
- [ ] Code is commented where necessary
- [ ] No debugging code remains
- [ ] PR description is complete

## Questions?

Feel free to open an issue labeled "question" if you need help or clarification on anything!

## License

By contributing to xnLinkFinder-Z, you agree that your contributions will be licensed under the MIT License.
