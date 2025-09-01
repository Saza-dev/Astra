from pathlib import Path
from crewai.tools import tool

@tool("list_folder_tool")
def list_folder_tool(path: str):
    """
    List contents of a folder or drive.
    
    Args:
        path (str): Full path to the folder or drive.
    
    Returns:
        dict: {
            "success": bool,
            "path": str,
            "folders": [list of folder names],
            "files": [list of file names],
            "total_items": int,
            "message": str
        }
    """
    p = Path(path)
    if not p.exists():
        return {
            "success": False,
            "path": path,
            "folders": [],
            "files": [],
            "total_items": 0,
            "message": f"Path does not exist: {path}"
        }
    if not p.is_dir():
        return {
            "success": False,
            "path": path,
            "folders": [],
            "files": [],
            "total_items": 0,
            "message": f"Path is not a folder: {path}"
        }
    
    folders = []
    files = []
    try:
        for item in p.iterdir():
            if item.is_dir():
                folders.append(item.name)
            else:
                files.append(item.name)
    except PermissionError:
        return {
            "success": False,
            "path": path,
            "folders": [],
            "files": [],
            "total_items": 0,
            "message": f"Permission denied to access {path}"
        }
    
    return {
        "success": True,
        "path": str(p),
        "folders": folders,
        "files": files,
        "total_items": len(folders) + len(files),
        "message": f"Found {len(folders)} folders and {len(files)} files in {path}"
    }
