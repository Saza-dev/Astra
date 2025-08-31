import os
import platform
import subprocess
from crewai.tools import tool

@tool("file_open_tool")
def file_open_tool(path: str) -> str:
    """
    Open a file with the default application.
    Args:
        path: Full file path to open
    Returns:
        Success or error message
    """
    try:
        if not os.path.exists(path):
            return f"Error: File does not exist at {path}"
        
        # Cross-platform file opening
        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', path], check=True)
        else:  # Linux and others
            subprocess.run(['xdg-open', path], check=True)
        
        return f"Successfully opened: {path}"
    except Exception as e:
        return f"Error opening file: {str(e)}"