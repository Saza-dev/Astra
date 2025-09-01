import subprocess
import json
from crewai.tools import tool

@tool("available_wifi_tool")
def available_wifi_tool() -> str:
    """
    Returns all available Wi-Fi networks and identifies saved ones.

    
    Returns:
        str: Formatted string with available networks and connection status
    """
    try:
        # Get available networks
        available_cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        available_output = subprocess.run(
            available_cmd, 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        # Parse available networks
        networks = []
        current_network = {}
        for line in available_output.stdout.splitlines():
            if "SSID" in line and ":" in line:
                if current_network:
                    networks.append(current_network)
                ssid = line.split(":", 1)[1].strip()
                current_network = {"ssid": ssid, "signal": 0}
            elif "Signal" in line and current_network:
                signal = line.split(":")[1].strip().replace("%", "")
                current_network["signal"] = int(signal) if signal.isdigit() else 0
        
        if current_network:
            networks.append(current_network)
        
        # Get saved profiles
        profiles_cmd = ["netsh", "wlan", "show", "profiles"]
        profiles_output = subprocess.run(
            profiles_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        saved_profiles = []
        for line in profiles_output.stdout.splitlines():
            if "All User Profile" in line:
                profile = line.split(":", 1)[1].strip()
                saved_profiles.append(profile)
        
        # Get current connection
        current_cmd = ["netsh", "wlan", "show", "interfaces"]
        current_output = subprocess.run(
            current_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        current_ssid = None
        for line in current_output.stdout.splitlines():
            if "SSID" in line and ":" in line and "BSSID" not in line:
                current_ssid = line.split(":", 1)[1].strip()
                break
        
        # Format output
        result = []
        if current_ssid:
            result.append(f"📶 Currently connected to: {current_ssid}\n")
        
        result.append("Available Wi-Fi Networks:")
        result.append("-" * 40)
        
        for net in sorted(networks, key=lambda x: x['signal'], reverse=True):
            ssid = net['ssid'] or "[Hidden Network]"
            signal = net['signal']
            status = ""
            
            if ssid == current_ssid:
                status = " [CONNECTED]"
            elif ssid in saved_profiles:
                status = " [SAVED]"
            
            signal_bars = "▂▄▆█"[min(3, signal // 25)] if signal > 0 else "▁"
            result.append(f"{signal_bars} {ssid} ({signal}%){status}")
        
        if not networks:
            result.append("No networks found. Make sure Wi-Fi is enabled.")
        
        return "\n".join(result)
        
    except subprocess.TimeoutExpired:
        return "Operation timed out. Please try again."
    except Exception as e:
        return f"Error scanning Wi-Fi networks: {str(e)}"