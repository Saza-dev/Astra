from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import math
from crewai.tools import tool


def _get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return interface.QueryInterface(IAudioEndpointVolume)

@tool("get_volume_tool")
def get_volume_tool() -> str:
    """
    Gets the current system master volume.
    
    Returns:
        str: Current volume percentage
    """
    try:
        volume = _get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar()
        return f"🔉 Current volume: {math.floor(current * 100)}%"
    except Exception as e:
        return f"❌ Error getting volume: {str(e)}"