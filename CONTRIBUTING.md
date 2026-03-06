# Contributing to Aegis

First off, thank you for considering contributing to Aegis! It's people like you that make Aegis such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (Python version, OS, nmap version)

### ✨ Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### 🔧 Pull Requests

* Fill in the required template
* Follow the Python/code styleguides
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- Virtual environment

### Installation for Development

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Aegis.git
cd Aegis

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black mypy pylint pytest pytest-cov bandit
```

### Making Changes

1. Create a new branch for your feature
```bash
git checkout -b feature/amazing-feature
```

2. Make your changes with:
   - Clear commit messages
   - Type hints for all functions
   - Docstrings for all modules/functions
   - Tests for new features

3. Run quality checks:
```bash
# Format code
black .

# Type checking
mypy .

# Linting
pylint ai_agent/ cli/ core/ mcp_server/ tools/

# Run tests
pytest

# Security check
bandit -r .
```

4. Push to your fork and create a Pull Request

## Styleguides

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with the following additions:

* Use type hints for all functions
* Maximum line length: 100 characters
* Use Black for formatting
* Use meaningful variable names
* Write docstrings for all public functions/classes

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Follow conventional commits:
  - `feat:` A new feature
  - `fix:` A bug fix
  - `docs:` Documentation only changes
  - `style:` Changes that don't affect code meaning
  - `refactor:` Code change that neither fixes a bug nor adds a feature
  - `perf:` Code change that improves performance
  - `test:` Adding missing tests

Example:
```
feat: add subdomain enumeration tool

- Implement amass wrapper
- Add to MCP server
- Include risk analysis
- Closes #123
```

### Documentation

* Use Markdown for all documentation
* Include code examples
* Update README.md if needed
* Add docstrings to all public functions
* Use type hints in examples

## Testing

### Writing Tests

```python
# tests/test_nmap_scanner.py
import pytest
from tools.nmap_scanner import scan_ports

def test_scan_ports_valid_target():
    """Test scanning a valid target."""
    result = scan_ports("localhost")
    
    assert result is not None
    assert "target" in result
    assert "ports" in result

def test_scan_ports_invalid_target():
    """Test error handling with invalid target."""
    with pytest.raises(RuntimeError):
        scan_ports("invalid@target")
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_nmap_scanner.py::test_scan_ports_valid_target
```

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - This will not be worked on

### Project Structure Guidelines

When adding new tools:

1. Create file: `tools/tool_name.py`
2. Implement wrapper function with type hints
3. Register in `mcp_server/server.py`
4. Update AI agent if needed in `ai_agent/agent.py`
5. Add CLI command if needed in `cli/main.py`
6. Update documentation

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for detailed guide.

## Recognition

Contributors will be recognized in:
- [README.md](./README.md) contributors section
- Release notes
- Hall of fame (coming soon)

## Questions?

* Check existing [discussions](https://github.com/amarjit-singh/Aegis/discussions)
* Create a new discussion for questions
* Email: `support@aegis-framework.dev`

Thank you for contributing! 🎉
