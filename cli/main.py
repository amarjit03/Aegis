"""
CLI Interface - Command line interface for Aegis framework.
Provides argument parsing and formatted output for security scanning operations.
"""

import sys
import os
import argparse
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import agent_scan
from mcp_server.server import get_server
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Initialize console for rich formatting
console = Console()


def format_scan_results(results: dict) -> None:
    """
    Format and display scan results with rich formatting.
    
    Args:
        results: Dictionary with scan results from agent
    """
    if not results.get("success"):
        console.print(f"[red]Error: {results.get('error', 'Unknown error')}[/red]")
        return
    
    target = results.get("target")
    scan_data = results.get("scan_results", {})
    analysis = results.get("analysis", {})
    ports = scan_data.get("ports", [])
    
    # Print target info
    console.print(f"\n[cyan]Target:[/cyan] {target}")
    console.print(f"[cyan]Scan Type:[/cyan] {scan_data.get('scan_type', 'standard')}")
    
    # Print risk assessment
    risk_level = analysis.get("risk_level", "UNKNOWN")
    risk_color = {
        "CRITICAL": "red",
        "HIGH": "yellow",
        "MEDIUM": "yellow",
        "LOW": "green"
    }.get(risk_level, "white")
    
    console.print(f"\n[bold]Risk Assessment[/bold]")
    console.print(f"[{risk_color}]Risk Level: {risk_level}[/{risk_color}]")
    console.print(f"Open Ports: {analysis.get('open_ports_count', 0)}")
    
    # Print ports table
    if ports:
        console.print(f"\n[bold]Open Ports[/bold]")
        table = Table(title="Port Details")
        table.add_column("Port", style="cyan")
        table.add_column("Protocol", style="magenta")
        table.add_column("Service", style="green")
        table.add_column("Product", style="yellow")
        table.add_column("Version", style="blue")
        
        for port in ports:
            table.add_row(
                port.get("port", ""),
                port.get("protocol", ""),
                port.get("service", ""),
                port.get("product", ""),
                port.get("version", "")
            )
        
        console.print(table)
    else:
        console.print("\n[green]No open ports detected[/green]")
    
    # Print recommendations
    recommendations = analysis.get("recommendations", [])
    if recommendations:
        console.print(f"\n[bold]Security Recommendations[/bold]")
        for i, rec in enumerate(recommendations, 1):
            console.print(f"  {i}. {rec}")


def cmd_scan(args: argparse.Namespace) -> int:
    """
    Handle 'scan' command.
    
    Args:
        args: Parsed arguments
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        results = agent_scan(
            target=args.target,
            aggressive=args.aggressive
        )
        format_scan_results(results)
        return 0 if results.get("success") else 1
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1


def cmd_tools(args: argparse.Namespace) -> int:
    """
    Handle 'tools' command - list available tools.
    
    Args:
        args: Parsed arguments
    
    Returns:
        Exit code (0 for success)
    """
    server = get_server()
    tools = server.list_tools()
    
    console.print(f"\n[bold]Available Tools[/bold]")
    for tool_name, description in tools.items():
        console.print(f"  • {tool_name}: {description}")
    
    return 0


def main() -> int:
    """
    Main entry point for CLI application.
    
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="Aegis - AI Powered Cybersecurity MCP Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m cli.main scan example.com
  python -m cli.main scan example.com --aggressive
  python -m cli.main tools
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan target for open ports")
    scan_parser.add_argument("target", help="Target hostname or IP address")
    scan_parser.add_argument(
        "--aggressive",
        action="store_true",
        help="Use aggressive scanning with OS detection"
    )
    scan_parser.set_defaults(func=cmd_scan)
    
    # Tools command
    tools_parser = subparsers.add_parser("tools", help="List available tools")
    tools_parser.set_defaults(func=cmd_tools)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
