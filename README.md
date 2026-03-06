# 🛡️ Aegis – AI Powered Cybersecurity MCP Framework

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](#contributing)

> A professional, modular cybersecurity automation framework built with Python. Aegis leverages the Model Context Protocol (MCP) to expose security tools to AI agents and CLI interfaces with enterprise-grade architecture.

**[Documentation](#-usage) • [Contributing](#-contributing) • [Roadmap](#-roadmap) • [Support](#-support)**

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [API Documentation](#-api-documentation)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Support](#-support)
- [License](#-license)

---

## ⚡ Features

- **🏗️ Modular Architecture** - Clean separation between CLI, MCP server, tools, and AI agent layers
- **🔌 MCP Server** - Central orchestrator for tool registration, request routing, and result formatting
- **📡 Nmap Integration** - Professional port scanning with service detection and XML parsing
- **🤖 AI Agent** - Intelligent tool orchestration with automatic risk analysis and recommendations
- **💅 Rich CLI** - Beautiful, formatted command-line output with colors and tables
- **📝 Type Hints** - Full type annotation for code clarity and IDE support
- **🧩 Extensible Design** - Easy-to-follow patterns for adding new security tools
- **⚙️ Production Ready** - Comprehensive error handling, validation, and logging
- **🔒 Security Focused** - Built for cybersecurity professionals with security best practices
- **📚 Well Documented** - Complete documentation with examples and troubleshooting guides

---

## 🚀 Quick Start

### Basic Scanning

```bash
# List available tools
python3 -m cli.main tools

# Standard port scan
python3 -m cli.main scan example.com

# Aggressive scan with service detection
python3 -m cli.main scan example.com --aggressive
```

### Python API

```python
from ai_agent.agent import agent_scan

# Orchestrated scan with risk analysis
results = agent_scan("example.com", aggressive=False)
print(results)
```

---

## 📦 Installation

### Prerequisites

| Requirement | Version |
|------------|---------|
| Python | 3.11+ |
| pip | Latest |
| nmap | 7.0+ |

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/amarjit-singh/Aegis.git
cd Aegis
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Upgrade pip (recommended)
pip install --upgrade pip
```

#### 4. Install System Tools

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install nmap

# macOS
brew install nmap

# Fedora/RHEL
sudo dnf install nmap

# Arch Linux
sudo pacman -S nmap
```

#### 5. Verify Installation

```bash
# Test CLI
python3 -m cli.main --help

# Test scanning
python3 -m cli.main scan localhost
```

### Docker Installation (Coming Soon)

```bash
docker build -t aegis:latest .
docker run -it aegis:latest scan example.com
```

---

## 📖 Usage

### CLI Commands

#### Scan Targets

```bash
# Basic scan
python3 -m cli.main scan example.com

# Aggressive scan (includes OS detection)
python3 -m cli.main scan example.com --aggressive

# Display help
python3 -m cli.main scan --help
```

#### List Tools

```bash
# Show all available tools
python3 -m cli.main tools

# Example output:
# Available Tools
#   • nmap_scan: Port scanning and service detection
```

### Example Output

```
Target: localhost
Scan Type: standard

Risk Assessment
Risk Level: CRITICAL
Open Ports: 5

Open Ports
                               Port Details                                
┏━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Port ┃ Protocol ┃ Service     ┃ Product       ┃ Version             ┃
┡━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 80   │ tcp      │ http        │ Apache httpd  │ 2.4.58              │
│ 3306 │ tcp      │ mysql       │ MySQL         │ 8.0.45              │
│ 5432 │ tcp      │ postgresql  │ PostgreSQL DB │ 9.6.0 or later      │
└──────┴──────────┴─────────────┴───────────────┴─────────────────────┘

Security Recommendations
  1. Database ports exposed - restrict access immediately
```

---

## 🏛️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│                        CLI Layer                         │
│              (Command Parsing & Formatting)              │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   MCP Server                            │
│         (Tool Registration & Request Routing)           │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Nmap Tool    │  │ WHOIS Tool   │  │ Amass Tool   │
│  (Wrapper)   │  │  (Wrapper)   │  │  (Wrapper)   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   Core Command Runner          │
        │  (Subprocess Management)        │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   System Commands               │
        │  (nmap, whois, amass, etc.)    │
        └─────────────────────────────────┘
```

### Project Structure

```
Aegis/
├── ai_agent/
│   ├── __init__.py
│   └── agent.py                    # AI orchestration & risk analysis
│
├── cli/
│   └── main.py                     # CLI interface with argparse
│
├── core/
│   ├── __init__.py
│   └── command_runner.py           # Reusable command execution
│
├── mcp_server/
│   ├── __init__.py
│   └── server.py                   # MCP server & tool router
│
├── tools/
│   ├── __init__.py
│   ├── nmap_scanner.py             # Port scanning wrapper
│   ├── whois_lookup.py             # Domain lookup (planned)
│   └── amass_enum.py               # Subdomain enumeration (planned)
│
├── .gitignore
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── INSTRUCTIONS.md                 # Tool development guide
├── CONTRIBUTING.md                 # Contributing guidelines
├── CODE_OF_CONDUCT.md              # Community guidelines
└── LICENSE                         # MIT License
```

### Component Responsibilities

| Component | File | Responsibility |
|-----------|------|-----------------|
| **CLI** | `cli/main.py` | Argument parsing, command routing, formatted output |
| **MCP Server** | `mcp_server/server.py` | Tool registration, request routing, result formatting |
| **Core** | `core/command_runner.py` | System command execution with error handling |
| **Tools** | `tools/*.py` | Security tool wrappers (nmap, whois, amass, etc.) |
| **AI Agent** | `ai_agent/agent.py` | Tool orchestration, risk analysis, recommendations |

---

## 🔌 API Documentation

### MCP Server API

#### `run_tool(tool_name, **kwargs)`

Execute a registered tool through the MCP server.

**Parameters:**
- `tool_name` (str): Name of the tool to execute
- `**kwargs`: Tool-specific parameters

**Returns:**
- Dict with keys: `success`, `tool`, `data` or `error`

**Example:**
```python
from mcp_server.server import run_tool

result = run_tool("nmap_scan", target="example.com")
if result["success"]:
    print(result["data"])
else:
    print(f"Error: {result['error']}")
```

#### `list_tools()`

List all available tools with descriptions.

**Returns:**
- Dict mapping tool names to descriptions

**Example:**
```python
from mcp_server.server import get_server

server = get_server()
tools = server.list_tools()
for name, desc in tools.items():
    print(f"{name}: {desc}")
```

### AI Agent API

#### `agent_scan(target, aggressive=False)`

Orchestrated scan with risk analysis.

**Parameters:**
- `target` (str): Target hostname or IP address
- `aggressive` (bool): Use aggressive scanning options

**Returns:**
- Dict with scan results, risk assessment, and recommendations

**Example:**
```python
from ai_agent.agent import agent_scan

results = agent_scan("example.com", aggressive=True)
print(f"Risk Level: {results['analysis']['risk_level']}")
print(f"Recommendations: {results['analysis']['recommendations']}")
```

### Command Runner API

#### `run_command(cmd, timeout=300)`

Execute a system command with error handling.

**Parameters:**
- `cmd` (list): Command and arguments as list
- `timeout` (int): Timeout in seconds (default: 300)

**Returns:**
- Tuple of (stdout, stderr, return_code)

**Raises:**
- `RuntimeError`: If command fails or times out

**Example:**
```python
from core.command_runner import run_command

stdout, stderr, rc = run_command(["nmap", "-h"])
if rc == 0:
    print("Nmap installed")
```

---

## 💡 Examples

### Example 1: Simple Port Scan

```bash
python3 -m cli.main scan scanme.nmap.org
```

### Example 2: Python Integration

```python
from ai_agent.agent import agent_scan

# Scan target
results = agent_scan("192.168.1.1")

# Access results
target = results['target']
ports = results['scan_results']['ports']
risk = results['analysis']['risk_level']

print(f"Target: {target}")
print(f"Open Ports: {len(ports)}")
print(f"Risk: {risk}")

# Print recommendations
for rec in results['analysis']['recommendations']:
    print(f"  - {rec}")
```

### Example 3: MCP Server Integration

```python
from mcp_server.server import run_tool, get_server

# List available tools
server = get_server()
print("Available tools:", list(server.list_tools().keys()))

# Run a scan
result = run_tool("nmap_scan", target="192.168.1.1", aggressive=True)

if result['success']:
    data = result['data']
    for port in data['ports']:
        print(f"Port {port['port']}: {port['service']}")
```

### Example 4: Add New Tool (Custom Extension)

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for complete guide.

```python
# tools/custom_tool.py
from typing import Dict, Any
from core.command_runner import run_command

def my_scan(target: str) -> Dict[str, Any]:
    """Custom scan implementation."""
    cmd = ["my-tool", target]
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode != 0:
        raise RuntimeError(f"Scan failed: {stderr}")
    
    return {
        "target": target,
        "results": parse_output(stdout)
    }
```

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### Getting Started with Development

#### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/Aegis.git
cd Aegis
```

#### 2. Create Feature Branch

```bash
git checkout -b feature/amazing-feature
```

#### 3. Set Up Development Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pylint black mypy pytest
```

#### 4. Make Your Changes

- Follow [code standards](#code-standards)
- Add type hints
- Write docstrings
- Test your changes

#### 5. Commit and Push

```bash
git add .
git commit -m "feat: add amazing feature"
git push origin feature/amazing-feature
```

#### 6. Create Pull Request

- Describe your changes clearly
- Link related issues
- Ensure CI passes

### Contribution Types

#### 🐛 Bug Reports

```bash
# Before reporting, check:
# 1. Search existing issues
# 2. Reproduce the issue
# 3. Collect error logs

# When reporting, include:
# - Python version
# - System (Linux/macOS/Windows)
# - Steps to reproduce
# - Expected vs actual behavior
```

#### ✨ Feature Requests

```bash
# Describe the feature
# Explain the use case
# Suggest implementation approach
```

#### 📝 Documentation

- Improve README
- Add examples
- Fix typos
- Add docstrings

#### 🔧 Code Improvements

- Add new tools
- Optimize existing code
- Improve error handling
- Add tests

### Pull Request Guidelines

- **One feature per PR** - Keep changes focused
- **Clear description** - Explain what and why
- **Tests included** - Add tests for new features
- **No breaking changes** - Maintain backward compatibility
- **Updated docs** - Update README if needed
- **Clean commit history** - Rebase if needed

### Code Standards

#### Type Hints (Required)

```python
def scan_target(target: str, timeout: int = 300) -> Dict[str, Any]:
    """Scan target with optional timeout."""
    pass
```

#### Docstrings (Required)

```python
def function(param: str) -> str:
    """
    Brief description.
    
    Args:
        param: Parameter description
    
    Returns:
        Return value description
    
    Raises:
        ValueError: When error occurs
    
    Example:
        >>> function("test")
        'result'
    """
    pass
```

#### Code Style

```bash
# Format code with black
black .

# Check types with mypy
mypy .

# Lint with pylint
pylint **/*.py
```

#### Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=. tests/
```

---

## 🛠️ Development

### Running Tests

```bash
# Unit tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html

# Specific test
pytest tests/test_nmap_scanner.py::test_parse_output
```

### Code Quality Checks

```bash
# Type checking
mypy .

# Linting
pylint ai_agent/ cli/ core/ mcp_server/ tools/

# Code formatting
black --check .

# Security scanning
bandit -r .
```

### Building Documentation

```bash
# Generate documentation (if using Sphinx)
cd docs/
make html
```

### Running Locally

```bash
# Activate venv
source .venv/bin/activate

# Run CLI
python3 -m cli.main scan localhost

# Run tests
pytest

# Run specific module
python3 -c "from mcp_server.server import run_tool; print(run_tool('nmap_scan', target='localhost'))"
```

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Nmap integration
- ✅ MCP server core
- ✅ CLI interface
- ✅ AI agent with risk analysis
- ✅ Documentation

### Version 1.1 (Q2 2026)
- 📋 WHOIS lookup tool
- 📋 DNS enumeration (dig/nslookup)
- 📋 Configuration file support
- 📋 JSON output format

### Version 1.2 (Q3 2026)
- 📋 Amass subdomain enumeration
- 📋 SSL/TLS certificate analysis
- 📋 Web vulnerability scanning (Nikto)
- 📋 Directory brute forcing (Dirb)

### Version 2.0 (Q4 2026)
- 📋 Web UI dashboard
- 📋 Reporting engine
- 📋 Scheduling and automation
- 📋 Multi-target scanning
- 📋 Result export (PDF, HTML, JSON)

### Version 2.1+ (2027)
- 📋 Integration with threat intelligence feeds
- 📋 Machine learning-based risk prediction
- 📋 Kubernetes deployment support
- 📋 GraphQL API
- 📋 Real-time collaboration features

---

## 💬 Support

### Getting Help

- 📖 **Documentation**: Read [README.md](./README.md) and [INSTRUCTIONS.md](./INSTRUCTIONS.md)
- 💬 **Discussions**: Ask questions in [GitHub Discussions](https://github.com/amarjit-singh/Aegis/discussions)
- 🐛 **Issues**: Report bugs in [GitHub Issues](https://github.com/amarjit-singh/Aegis/issues)
- 📧 **Email**: Contact maintainers at `support@aegis-framework.dev`

### Troubleshooting

#### "Command not found: nmap"

```bash
# Install nmap
sudo apt-get install nmap      # Debian/Ubuntu
brew install nmap               # macOS
sudo dnf install nmap           # Fedora
```

#### "ModuleNotFoundError"

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### "Permission denied"

```bash
# Some nmap options require root
sudo python3 -m cli.main scan example.com --aggressive
```

For more help, see [Troubleshooting Guide](./TROUBLESHOOTING.md) (coming soon).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

### Summary

- ✅ Free for commercial use
- ✅ Modify and distribute
- ❌ No warranty or liability
- ✅ Include original license and copyright

---

## 👥 Authors

- **Amarjit Singh** - *Project Lead & Creator* - [GitHub](https://github.com/amarjit-singh)

### Contributors

- Thanks to all contributors who have helped improve Aegis!

---

## 🙏 Acknowledgments

- [Nmap](https://nmap.org) - Network scanning tool
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- [Python](https://www.python.org/) - The Python community
- All contributors and testers

---

## 📞 Contact & Community

- **GitHub Issues**: [Report bugs](https://github.com/amarjit-singh/Aegis/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/amarjit-singh/Aegis/discussions)
- **Security Issues**: Email `security@aegis-framework.dev` (do NOT use issues)
- **Email**: `contact@aegis-framework.dev`

---

## 📚 Additional Resources

- [Security Best Practices](./docs/SECURITY.md)
- [API Documentation](./docs/API.md)
- [Tool Development Guide](./INSTRUCTIONS.md)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Changelog](./CHANGELOG.md)

---

## ⭐ Show Your Support

If you find Aegis useful, please consider:
- ⭐ Starring the repository
- 🔗 Sharing with colleagues
- 🐛 Reporting issues
- 🤝 Contributing code
- 💬 Providing feedback

---

<div align="center">

**[Back to Top](#-aegis--ai-powered-cybersecurity-mcp-framework)**

Made with ❤️ by the Aegis Community

</div>
