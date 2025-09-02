import screen_brightness_control as sbc
from crewai.tools import tool

@tool("set_brightness_tool")
def set_brightness_tool(level: int) -> str:
    """
    Sets the screen brightness to a given level (0-100).
    
    Args:
        level (int): Brightness percentage (0 to 100)
    
    Returns:
        str: Success or error message
    """
    try:
        if 0 <= level <= 100:
            sbc.set_brightness(level,method="wmi")
            return {"success": True, "message": f"Brightness set to {level}%"}
        else:
            return {"success": False, "message": "Provide a value between 0 and 100."}
    except Exception as e:
        return {"success": False, "message": f"Error setting brightness: {e}"}