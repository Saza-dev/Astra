import shutil
from crewai.tools import tool
import os


@tool("delete_file_folder")
def delete_file_folder(path: str):
    """
    Delete a file or folder. Optionally send to recycle bin.

    Args:
        path (str): Full path to delete
    Returns:
        dict: Success or error message
    """
    try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            else:
                return {"success": False, "message": f"Path not found: {path}"}
            return {"success": True, "message": f"Deleted: {path}"}
    except Exception as e:
        return {"success": False, "message": str(e)}