# Adding New Tools to Aegis Framework

## Overview

The Aegis framework is designed to be easily extensible. This guide explains how to add new cybersecurity tools to the MCP server following the existing architecture patterns.

## Architecture Review

### Current Tool Flow

```
CLI → MCP Server → Tool Wrapper → System Command → Result Parser
```

1. **CLI** (cli/main.py): User interface layer
2. **MCP Server** (mcp_server/server.py): Central orchestrator
3. **Tool Wrapper** (tools/*.py): Wrapper around external tools
4. **System Command**: Actual command execution (nmap, amass, etc.)
5. **Result Parser**: Parse and structure output

### File Organization

```
tools/
├── __init__.py
├── nmap_scanner.py          # Existing tool
├── new_tool_wrapper.py      # Your new tool
└── another_tool.py          # Future tools
```

---

## Step-by-Step Guide: Adding a New Tool

### Step 1: Create a New Tool Wrapper File

Create a new file in the `tools/` directory following the naming convention: `tool_name_wrapper.py`

Example: `tools/whois_lookup.py`

```python
"""
WHOIS lookup tool wrapper.
Performs domain WHOIS queries and returns structured data.
"""

from typing import Dict, Any
from core.command_runner import run_command


def whois_lookup(domain: str) -> Dict[str, Any]:
    """
    Perform WHOIS lookup on a domain.
    
    Args:
        domain: Domain name to lookup
    
    Returns:
        Dictionary with WHOIS information
    """
    cmd = ["whois", domain]
    
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode != 0:
        raise RuntimeError(f"WHOIS lookup failed: {stderr}")
    
    # Parse WHOIS output
    whois_data = _parse_whois_output(stdout)
    
    return {
        "domain": domain,
        "registrar": whois_data.get("registrar"),
        "creation_date": whois_data.get("creation_date"),
        "expiration_date": whois_data.get("expiration_date"),
        "nameservers": whois_data.get("nameservers", [])
    }


def _parse_whois_output(whois_text: str) -> Dict[str, Any]:
    """
    Parse WHOIS text output into structured data.
    
    Args:
        whois_text: Raw WHOIS output
    
    Returns:
        Dictionary with parsed WHOIS data
    """
    data = {}
    lines = whois_text.split('\n')
    
    for line in lines:
        if ':' not in line:
            continue
        
        key, value = line.split(':', 1)
        key = key.strip().lower()
        value = value.strip()
        
        if 'registrar' in key and 'registrar' not in data:
            data['registrar'] = value
        elif 'creation date' in key:
            data['creation_date'] = value
        elif 'expiration date' in key or 'expiry' in key:
            data['expiration_date'] = value
        elif 'nameserver' in key:
            if 'nameservers' not in data:
                data['nameservers'] = []
            data['nameservers'].append(value)
    
    return data
```

### Step 2: Register the Tool in MCP Server

Edit [mcp_server/server.py](mcp_server/server.py) and add the import and registration:

```python
from typing import Dict, Any, Callable
from tools.nmap_scanner import scan_ports
from tools.whois_lookup import whois_lookup  # ← Add import


class MCPServer:
    """..."""
    
    def _register_tools(self) -> None:
        """Register all available security tools."""
        self.tools["nmap_scan"] = scan_ports
        self.tools["whois_lookup"] = whois_lookup  # ← Add registration
    
    def list_tools(self) -> Dict[str, str]:
        """..."""
        return {
            "nmap_scan": "Port scanning and service detection",
            "whois_lookup": "Domain WHOIS lookup"  # ← Add description
        }
```

### Step 3: Update the AI Agent (Optional)

If the tool requires special handling or analysis, update [ai_agent/agent.py](ai_agent/agent.py):

```python
def agent_domain_lookup(domain: str) -> Dict[str, Any]:
    """
    AI agent domain lookup with analysis.
    
    Args:
        domain: Domain to lookup
    
    Returns:
        Dictionary with results and analysis
    """
    result = run_tool("whois_lookup", domain=domain)
    
    if not result["success"]:
        return {
            "domain": domain,
            "success": False,
            "error": result.get("error")
        }
    
    whois_data = result["data"]
    
    # Analyze domain age and other factors
    analysis = _analyze_domain(whois_data)
    
    return {
        "domain": domain,
        "success": True,
        "whois_data": whois_data,
        "analysis": analysis
    }
```

### Step 4: Add CLI Command (Optional)

Update [cli/main.py](cli/main.py) to expose the new tool:

```python
def cmd_whois(args: argparse.Namespace) -> int:
    """
    Handle 'whois' command - domain lookup.
    
    Args:
        args: Parsed arguments
    
    Returns:
        Exit code
    """
    try:
        from ai_agent.agent import agent_domain_lookup
        
        results = agent_domain_lookup(args.domain)
        
        console.print(f"\n[cyan]Domain:[/cyan] {results['domain']}")
        console.print(f"[cyan]Registrar:[/cyan] {results['whois_data'].get('registrar', 'N/A')}")
        console.print(f"[cyan]Created:[/cyan] {results['whois_data'].get('creation_date', 'N/A')}")
        console.print(f"[cyan]Expires:[/cyan] {results['whois_data'].get('expiration_date', 'N/A')}")
        
        return 0
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1


# Add to main() function argument parsing:
# whois_parser = subparsers.add_parser("whois", help="Domain WHOIS lookup")
# whois_parser.add_argument("domain", help="Domain name")
# whois_parser.set_defaults(func=cmd_whois)
```

### Step 5: Test Your Tool

```bash
# Test tool directly through MCP server
python3 -c "
from mcp_server.server import run_tool
result = run_tool('whois_lookup', domain='example.com')
print(result)
"

# Test through CLI (if implemented)
python3 -m cli.main whois example.com
```

---

## Tool Development Best Practices

### 1. **Error Handling**
Always wrap system commands with proper error handling:

```python
try:
    stdout, stderr, returncode = run_command(cmd)
    if returncode != 0:
        raise RuntimeError(f"Command failed: {stderr}")
except Exception as e:
    raise RuntimeError(f"Tool execution failed: {str(e)}")
```

### 2. **Type Hints**
Use complete type hints for all functions:

```python
from typing import Dict, List, Any, Tuple, Optional

def tool_function(param: str, optional: Optional[int] = None) -> Dict[str, Any]:
    """Your function."""
    pass
```

### 3. **Documentation**
Include comprehensive docstrings:

```python
def my_tool(target: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Brief description of what the tool does.
    
    Args:
        target: Description of target parameter
        verbose: Enable verbose output
    
    Returns:
        Dictionary with keys: 'target', 'data', 'status'
    
    Raises:
        RuntimeError: If tool execution fails
    
    Example:
        >>> result = my_tool("example.com")
        >>> print(result['status'])
    """
    pass
```

### 4. **Output Format**
Always return structured data:

```python
# Good: Structured dict
return {
    "target": target,
    "results": [...],
    "metadata": {...}
}

# Avoid: Unstructured text
return "results: ..., metadata: ..."
```

### 5. **Timeout Handling**
The `run_command()` function has a 300-second timeout. For longer operations:

```python
# Adjust timeout if needed
stdout, stderr, returncode = run_command(cmd, timeout=600)

# Or split into smaller chunks
for chunk in target_list:
    stdout, stderr, returncode = run_command([tool] + chunk)
```

---

## Common Tool Patterns

### Pattern 1: Direct Command Execution

```python
def scan_tool(target: str) -> Dict[str, Any]:
    """Simple command execution and parsing."""
    cmd = ["tool_name", "-options", target]
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode != 0:
        raise RuntimeError(f"Scan failed: {stderr}")
    
    results = parse_output(stdout)
    return {"target": target, "results": results}
```

### Pattern 2: XML/JSON Parsing

```python
import json
import xml.etree.ElementTree as ET

def tool_with_json(target: str) -> Dict[str, Any]:
    """Tool that outputs JSON."""
    cmd = ["tool_name", "--json", target]
    stdout, stderr, returncode = run_command(cmd)
    
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON: {str(e)}")
    
    return {"target": target, "data": data}
```

### Pattern 3: Multiple Passes

```python
def multi_stage_tool(target: str) -> Dict[str, Any]:
    """Tool that requires multiple passes."""
    # Stage 1: Discovery
    discovery_cmd = ["tool_name", "--discover", target]
    stdout1, _, _ = run_command(discovery_cmd)
    discovered = parse_discovery(stdout1)
    
    # Stage 2: Detailed scan
    results = []
    for item in discovered:
        scan_cmd = ["tool_name", "--scan", item]
        stdout2, _, _ = run_command(scan_cmd)
        results.append(parse_scan(stdout2))
    
    return {"target": target, "results": results}
```

---

## Example: Adding Subdomain Enumeration Tool

Here's a complete example of adding `amass` for subdomain enumeration:

### File: `tools/amass_enum.py`

```python
"""
Amass subdomain enumeration tool wrapper.
Uses the Amass tool for comprehensive subdomain discovery.
"""

from typing import Dict, Any, List
import json
from core.command_runner import run_command


def enum_subdomains(domain: str, sources: bool = True) -> Dict[str, Any]:
    """
    Enumerate subdomains using Amass.
    
    Args:
        domain: Target domain
        sources: Include source information
    
    Returns:
        Dictionary with domain and discovered subdomains
    """
    cmd = ["amass", "enum", "-d", domain, "-json"]
    
    if not sources:
        cmd.append("-nocolor")
    
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode != 0 and "error" not in stderr.lower():
        raise RuntimeError(f"Amass enumeration failed: {stderr}")
    
    subdomains = _parse_amass_output(stdout)
    
    return {
        "domain": domain,
        "subdomains": subdomains,
        "total_count": len(subdomains)
    }


def _parse_amass_output(json_output: str) -> List[Dict[str, str]]:
    """
    Parse Amass JSON output.
    
    Args:
        json_output: JSON output from Amass
    
    Returns:
        List of subdomain dictionaries
    """
    subdomains = []
    
    try:
        for line in json_output.strip().split('\n'):
            if not line.strip():
                continue
            data = json.loads(line)
            subdomains.append({
                "name": data.get("name"),
                "source": data.get("source"),
                "ip_addresses": data.get("addresses", [])
            })
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse Amass output: {str(e)}")
    
    return subdomains
```

### Register in MCP Server

```python
from tools.amass_enum import enum_subdomains

def _register_tools(self) -> None:
    """Register all available security tools."""
    self.tools["nmap_scan"] = scan_ports
    self.tools["whois_lookup"] = whois_lookup
    self.tools["amass_enum"] = enum_subdomains  # ← Add here
```

---

## Testing Your Tool

### Unit Test Example

```python
# test_new_tool.py
from tools.your_tool import your_function

def test_tool_execution():
    """Test basic tool execution."""
    result = your_function("test_target")
    
    assert result is not None
    assert "target" in result
    assert isinstance(result.get("results"), list)

def test_error_handling():
    """Test error handling."""
    try:
        result = your_function("invalid_target")
        assert False, "Should have raised an error"
    except RuntimeError as e:
        assert "failed" in str(e).lower()
```

### Run via MCP Server

```python
from mcp_server.server import run_tool

# Test execution
result = run_tool("your_tool_name", target="example.com")
print(f"Success: {result['success']}")
print(f"Data: {result['data']}")
```

---

## Planned Tools for Aegis

Here's a roadmap of tools planned for future implementation:

| Tool | Purpose | Status |
|------|---------|--------|
| **nmap** | Port scanning | ✅ Implemented |
| **whois** | Domain lookup | 📋 Planned |
| **amass** | Subdomain enumeration | 📋 Planned |
| **dig/nslookup** | DNS enumeration | 📋 Planned |
| **nikto** | Web vulnerability scanner | 📋 Planned |
| **dirb** | Directory brute forcing | 📋 Planned |
| **theHarvester** | Email enumeration | 📋 Planned |
| **SSLyze** | SSL/TLS analysis | 📋 Planned |
| **metasploit** | Exploit framework integration | 📋 Planned |
| **shodan** | Internet search integration | 📋 Planned |

---

## Tool Dependencies

### Install Tool Command Line

Ensure the tool is installed before registering it. Update this list in your installation docs:

```bash
# Nmap (already installed)
sudo apt-get install nmap

# WHOIS
sudo apt-get install whois

# Amass
sudo snap install amass

# Dig
sudo apt-get install dnsutils

# Nikto
sudo apt-get install nikto

# Dirb
sudo apt-get install dirb
```

---

## Troubleshooting

### Issue: "Command not found"
**Solution**: Ensure the tool is installed in your system PATH.

```bash
which nmap  # Check if installed
nmap --version  # Verify installation
```

### Issue: "Permission denied"
**Solution**: Some tools need root. Either run with sudo or adjust permissions.

```bash
sudo python3 -m cli.main scan target.com
```

### Issue: Timeout errors
**Solution**: Increase timeout in `core/command_runner.py` or optimize tool parameters.

### Issue: Parse errors
**Solution**: Test tool output directly and adjust parser for your tool version.

```bash
nmap -sV -oX - example.com  # Test nmap output
```

---

## Summary Checklist

When adding a new tool:

- [ ] Create tool wrapper in `tools/` directory
- [ ] Implement function with type hints
- [ ] Add comprehensive docstrings
- [ ] Return structured dictionary
- [ ] Handle errors properly
- [ ] Register in `mcp_server/server.py`
- [ ] Add to `list_tools()` descriptions
- [ ] Update AI agent if needed (optional)
- [ ] Add CLI command if needed (optional)
- [ ] Test execution
- [ ] Document in this file
- [ ] Update README.md

---

## Quick Reference

### Minimal Tool Template

```python
"""
Tool wrapper description.
"""

from typing import Dict, Any
from core.command_runner import run_command


def tool_name(target: str, param: str = "default") -> Dict[str, Any]:
    """
    Brief tool description.
    
    Args:
        target: Target parameter
        param: Optional parameter
    
    Returns:
        Structured result dictionary
    """
    cmd = ["tool_command", "-option", target]
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode != 0:
        raise RuntimeError(f"Tool failed: {stderr}")
    
    results = _parse_output(stdout)
    
    return {
        "target": target,
        "results": results
    }


def _parse_output(output: str) -> dict:
    """Parse tool output into structured format."""
    # Your parsing logic
    return {}
```

---

For questions or issues, refer to existing tool implementations in the `tools/` directory.
