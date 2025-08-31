import os
import signal
import psutil  
from crewai.tools import tool

@tool("file_close_tool")
def file_close_tool(process_name: str):
    """
    Close (terminate) a running application by process name.
    
    Args:
        process_name (str): The name of the process to close (e.g., 'Riot Client.exe')
    
    Returns:
        dict: Result message of success or failure
    """
    closed = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                os.kill(proc.info['pid'], signal.SIGTERM)
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    if closed:
        return {"success": True, "message": f"Closed all processes named '{process_name}'"}
    else:
        return {"success": False, "message": f"No running process found with name '{process_name}'"}
