"""
MCP Server - Central orchestrator for cybersecurity tools.
Routes requests from CLI or AI agent to appropriate tools and returns structured results.
"""

from typing import Dict, Any, Callable
from tools.nmap_scanner import scan_ports


class MCPServer:
    """
    Model Context Protocol Server for cybersecurity tools.
    Acts as central orchestrator for tool registration and routing.
    """
    
    def __init__(self):
        """Initialize MCP server and register available tools."""
        self.tools: Dict[str, Callable] = {}
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register all available security tools."""
        self.tools["nmap_scan"] = scan_ports
    
    def run_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a registered tool with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Parameters to pass to the tool
        
        Returns:
            Structured result from the tool
        
        Raises:
            ValueError: If tool not found
            RuntimeError: If tool execution fails
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}. Available tools: {list(self.tools.keys())}")
        
        try:
            result = self.tools[tool_name](**kwargs)
            return {
                "success": True,
                "tool": tool_name,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "tool": tool_name,
                "error": str(e)
            }
    
    def list_tools(self) -> Dict[str, str]:
        """
        List all available tools.
        
        Returns:
            Dictionary of tool names and descriptions
        """
        return {
            "nmap_scan": "Port scanning and service detection"
        }


# Global server instance
_server = MCPServer()


def get_server() -> MCPServer:
    """Get the global MCP server instance."""
    return _server


def run_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Execute a tool through the MCP server.
    
    Args:
        tool_name: Name of the tool to execute
        **kwargs: Parameters to pass to the tool
    
    Returns:
        Structured result from the tool
    """
    return _server.run_tool(tool_name, **kwargs)
