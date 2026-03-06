"""
Core utility module for executing system commands.
Provides a reusable function for running terminal commands with error handling.
"""

import subprocess
from typing import Tuple


def run_command(cmd: list) -> Tuple[str, str, int]:
    """
    Execute a system command and capture output.
    
    Args:
        cmd: List of command arguments (e.g., ['nmap', '-sV', 'example.com'])
    
    Returns:
        Tuple of (stdout, stderr, return_code)
    
    Raises:
        RuntimeError: If command execution fails
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Command timed out: {' '.join(cmd)}")
    except FileNotFoundError:
        raise RuntimeError(f"Command not found: {cmd[0]}")
    except Exception as e:
        raise RuntimeError(f"Error executing command: {str(e)}")
