import subprocess
import ctypes
import sys
from crewai.tools import tool

@tool("turn_off_wifi_tool")
def turn_off_wifi_tool() -> str:
    """
    Turns off Wi-Fi adapter on Windows.
    
    Returns:
        str: Success or failure message
    """
    try:
        # Check for admin privileges
        if not ctypes.windll.shell32.IsUserAnAdmin():
            return ("⚠️ Administrator privileges required to disable Wi-Fi.\n"
                   "Please run this script as administrator or use Windows Settings to turn off Wi-Fi manually.")
        
        # Try multiple adapter names
        adapter_names = ["Wi-Fi", "WiFi", "Wireless", "WLAN"]
        success = False
        
        for adapter in adapter_names:
            try:
                cmd = ["netsh", "interface", "set", "interface", adapter, "disable"]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    success = True
                    return f"✅ Wi-Fi adapter '{adapter}' has been disabled successfully."
            except:
                continue
        
        if not success:
            # Alternative method using PowerShell
            ps_cmd = [
                "powershell", "-Command",
                "Get-NetAdapter | Where-Object {$_.Name -like '*Wi*Fi*' -or $_.Name -like '*Wireless*'} | Disable-NetAdapter -Confirm:$false"
            ]
            result = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return "✅ Wi-Fi has been turned off successfully."
            else:
                return ("Could not disable Wi-Fi programmatically.\n"
                       "Please turn off Wi-Fi manually through:\n"
                       "• Windows Settings > Network & Internet > Wi-Fi\n"
                       "• Or click the Wi-Fi icon in system tray")
                
    except subprocess.TimeoutExpired:
        return "Operation timed out. Please try again."
    except Exception as e:
        return f"Error disabling Wi-Fi: {str(e)}"
    
    