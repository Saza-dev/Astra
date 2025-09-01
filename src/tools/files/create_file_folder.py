import os
from crewai.tools import tool

@tool("create_file_folder")
def create_file_folder(path: str, is_folder: bool = False):
    """
    Create a new file or folder at the given path.

    Args:
        path (str): Full path of the file or folder
        is_folder (bool): True for folder, False for file

    Returns:
        dict: Success or error message
    """
    try:
        if is_folder:
            os.makedirs(path, exist_ok=True)
            return {"success": True, "message": f"Folder created at {path}"}
        else:
            with open(path, "w") as f:
                f.write("")  # empty file
            return {"success": True, "message": f"File created at {path}"}
    except Exception as e:
        return {"success": False, "message": str(e)}