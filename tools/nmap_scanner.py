"""
Nmap tool wrapper for port scanning.
Executes nmap with XML output and parses results into structured data.
"""

from typing import Dict, List, Any
import xml.etree.ElementTree as ET
from core.command_runner import run_command


def scan_ports(target: str, aggressive: bool = False) -> Dict[str, Any]:
    """
    Scan target host for open ports using nmap.
    
    Args:
        target: Target hostname or IP address
        aggressive: If True, use more aggressive scanning (-sV -sC)
    
    Returns:
        Dictionary with target, ports, and scan metadata
    """
    # Build nmap command
    cmd = ["nmap", "-sV", "-oX", "-"]
    
    if aggressive:
        cmd.insert(2, "-sC")
    
    cmd.append(target)
    
    # Execute nmap
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode != 0 and "warning" not in stderr.lower():
        raise RuntimeError(f"Nmap scan failed: {stderr}")
    
    # Parse XML output
    ports = _parse_nmap_xml(stdout)
    
    return {
        "target": target,
        "ports": ports,
        "scan_type": "aggressive" if aggressive else "standard"
    }


def _parse_nmap_xml(xml_output: str) -> List[Dict[str, str]]:
    """
    Parse nmap XML output and extract port information.
    
    Args:
        xml_output: XML output from nmap
    
    Returns:
        List of port dictionaries with port, state, and service information
    """
    ports = []
    
    try:
        root = ET.fromstring(xml_output)
    except ET.ParseError as e:
        raise RuntimeError(f"Failed to parse nmap XML: {str(e)}")
    
    # Find all hosts
    for host in root.findall(".//host"):
        for port_elem in host.findall(".//port"):
            port_num = port_elem.get("portid")
            protocol = port_elem.get("protocol")
            
            # Get state
            state_elem = port_elem.find("state")
            state = state_elem.get("state") if state_elem is not None else "unknown"
            
            # Get service info
            service_elem = port_elem.find("service")
            service_name = service_elem.get("name") if service_elem is not None else "unknown"
            service_product = service_elem.get("product") if service_elem is not None else ""
            service_version = service_elem.get("version") if service_elem is not None else ""
            
            # Only include open ports
            if state == "open":
                ports.append({
                    "port": port_num,
                    "protocol": protocol,
                    "state": state,
                    "service": service_name,
                    "product": service_product,
                    "version": service_version
                })
    
    return ports
