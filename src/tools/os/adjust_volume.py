from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from crewai.tools import tool

def _get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return interface.QueryInterface(IAudioEndpointVolume)

@tool("set_volume_tool")
def set_volume_tool(level: int) -> str:
    """
    Sets the system master volume (0-100).
    
    Args:
        level (int): Volume percentage (0 to 100)
    
    Returns:
        str: Success or error message
    """
    try:
        if 0 <= level <= 100:
            volume = _get_volume_interface()
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return f"🔊 Volume set to {level}%"
        else:
            return "⚠️ Please provide a value between 0 and 100."
    except Exception as e:
        return f"❌ Error setting volume: {str(e)}"