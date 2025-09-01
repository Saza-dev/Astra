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
        level = sbc.get_brightness(display=0)  # main display
        return f"🌞 Current brightness: {level[0]}%"
    except Exception as e:
        return f"❌ Error getting brightness: {str(e)}"