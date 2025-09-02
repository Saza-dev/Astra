import os
import platform
import subprocess
from crewai.tools import tool

@tool("file_open_tool")
def file_open_tool(path: str) -> str:
    
    """
    Open a file or folder.
    Args:
        path: Full file path to open
    Returns:
        Success or error message
    """

    try:
        if not os.path.exists(path):
            return {"success": False, "message": f"Path does not exist: {path}"}
        os.startfile(path)
        return {"success": True, "message": f"Opened: {path}"}
    except Exception as e:
        return {"success": False, "message": f"Error opening '{path}': {e}"}