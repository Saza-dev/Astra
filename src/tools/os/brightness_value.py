import screen_brightness_control as sbc
from crewai.tools import tool

@tool("get_brightness_tool")
def get_brightness_tool() -> str:
    """
    Gets the current screen brightness level.
    
    Returns:
        str: Current brightness percentage
    """
    try:
        levels = sbc.get_brightness(display=0)  # returns list
        val = int(levels[0]) if levels else None
        if val is None:
            return {"success": False, "message": "No brightness value returned."}
        return {"success": True, "message": f"🌞 Current brightness: {val}%","value": val}
    except Exception as e:
        return {"success": False, "message": f"Error getting brightness: {e}"}