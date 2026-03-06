"""
AI Agent - Intelligence layer for decision making.
Decides which tools to run and orchestrates the scanning workflow.
"""

from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.server import run_tool


def agent_scan(target: str, aggressive: bool = False) -> Dict[str, Any]:
    """
    AI agent scan orchestration.
    Decides which tools to run based on target and returns analysis.
    
    Args:
        target: Target hostname or IP address
        aggressive: If True, use aggressive scanning
    
    Returns:
        Dictionary with scan results and analysis
    """
    # Execute nmap scan through MCP server
    result = run_tool("nmap_scan", target=target, aggressive=aggressive)
    
    if not result["success"]:
        return {
            "target": target,
            "success": False,
            "error": result.get("error", "Unknown error")
        }
    
    scan_data = result["data"]
    ports = scan_data.get("ports", [])
    
    # Analyze results for security risks
    risk_level = _analyze_risk(ports)
    recommendations = _get_recommendations(ports)
    
    return {
        "target": target,
        "success": True,
        "scan_results": scan_data,
        "analysis": {
            "risk_level": risk_level,
            "open_ports_count": len(ports),
            "recommendations": recommendations
        }
    }


def _analyze_risk(ports: list) -> str:
    """
    Analyze security risk based on open ports.
    
    Args:
        ports: List of open ports from scan
    
    Returns:
        Risk level: CRITICAL, HIGH, MEDIUM, or LOW
    """
    if not ports:
        return "LOW"
    
    # Check for critical services
    critical_ports = {22, 23, 3389, 3306, 5432, 27017}
    high_ports = {21, 25, 53, 80, 443, 8080, 8443}
    
    port_numbers = {int(p.get("port", 0)) for p in ports}
    
    if any(p in port_numbers for p in critical_ports):
        return "CRITICAL"
    elif any(p in port_numbers for p in high_ports):
        return "HIGH"
    else:
        return "MEDIUM"


def _get_recommendations(ports: list) -> list:
    """
    Generate security recommendations based on open ports.
    
    Args:
        ports: List of open ports from scan
    
    Returns:
        List of security recommendations
    """
    recommendations = []
    port_numbers = {int(p.get("port", 0)): p for p in ports}
    
    if 23 in port_numbers:
        recommendations.append("Disable Telnet (port 23) - use SSH instead")
    
    if 21 in port_numbers:
        recommendations.append("Disable FTP (port 21) - use SFTP instead")
    
    if 22 in port_numbers:
        recommendations.append("Restrict SSH access with firewall rules")
    
    if 3389 in port_numbers:
        recommendations.append("Restrict RDP access with firewall rules")
    
    if any(p in port_numbers for p in [3306, 5432, 27017]):
        recommendations.append("Database ports exposed - restrict access immediately")
    
    if not recommendations:
        recommendations.append("No critical issues found, maintain standard security practices")
    
    return recommendations
