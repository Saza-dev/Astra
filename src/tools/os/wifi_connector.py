import subprocess
from crewai.tools import tool

@tool("connect_wifi_tool")
def connect_wifi_tool(ssid: str) -> str:
    """
    Connect to a saved Wi-Fi network by SSID.
    
    Args:
        ssid (str): Name of the Wi-Fi network to connect to
        
    Returns:
        str: Success or failure message with details
    """
    if not ssid:
        return "Error: Please provide the network name (SSID) to connect to."
    
    try:
        # Check if profile exists
        profiles_cmd = ["netsh", "wlan", "show", "profiles"]
        profiles_output = subprocess.run(
            profiles_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        profile_exists = False
        for line in profiles_output.stdout.splitlines():
            if "All User Profile" in line:
                profile = line.split(":", 1)[1].strip()
                if profile.lower() == ssid.lower():
                    profile_exists = True
                    ssid = profile  # Use exact case
                    break
        
        if not profile_exists:
            return (f"Network '{ssid}' is not saved on this computer.\n"
                   f"Please connect to it manually first with the password, "
                   f"then I can reconnect automatically in the future.")
        
        # Attempt connection
        connect_cmd = ["netsh", "wlan", "connect", f"name={ssid}"]
        result = subprocess.run(
            connect_cmd,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            # Verify connection
            import time
            time.sleep(2)  # Wait for connection to establish
            
            verify_cmd = ["netsh", "wlan", "show", "interfaces"]
            verify_output = subprocess.run(
                verify_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            connected = False
            for line in verify_output.stdout.splitlines():
                if "SSID" in line and ssid in line:
                    connected = True
                    break
            
            if connected:
                return f"✅ Successfully connected to '{ssid}'"
            else:
                return f"Connection initiated to '{ssid}' but verification pending. Please check your connection status."
        else:
            error_msg = result.stderr or result.stdout
            return f"Failed to connect to '{ssid}'. Error: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return "Connection attempt timed out. Please try again."
    except Exception as e:
        return f"Error connecting to Wi-Fi: {str(e)}"