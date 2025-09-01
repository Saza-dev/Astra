import subprocess
import re
from crewai.tools import tool

@tool("available_bluetooth_tool")
def available_bluetooth_tool() -> str:
    """
    returns available Bluetooth devices and their approximate connection status.
    
    Returns:
        str: Formatted list of Bluetooth devices
    """
    try:
        # PowerShell command to get Bluetooth devices
        ps_cmd = [
            "powershell", "-Command",
            "Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName} | "
            "Select-Object FriendlyName, Status | ConvertTo-Json"
        ]

        result = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=15)

        import json
        try:
            devices_data = json.loads(result.stdout)
            if isinstance(devices_data, dict):
                devices_data = [devices_data]
        except:
            devices_data = []

        if not devices_data:
            return "No paired Bluetooth devices found."

        # Filter out sub-services/profiles
        filtered_devices = {}
        ignore_keywords = ["avrcp", "service", "profile", "pse", "audio", "gateway", "network"]

        for d in devices_data:
            name = d.get("FriendlyName", "Unknown")
            status = d.get("Status", "Unknown")
            # Skip sub-services
            if any(k in name.lower() for k in ignore_keywords):
                continue
            # Only keep first occurrence of each device
            if name not in filtered_devices:
                filtered_devices[name] = "Connected" if status == "OK" else "Paired but not connected"

        if not filtered_devices:
            return "No paired Bluetooth devices found after filtering sub-services."

        # Prepare output
        output = ["Bluetooth Devices:", "-" * 40]
        connected = [f"{n} [{s}]" for n, s in filtered_devices.items() if s == "Connected"]
        disconnected = [f"{n} [{s}]" for n, s in filtered_devices.items() if s != "Connected"]

        if connected:
            output.append("\nConnected devices:")
            output.extend(connected)
        if disconnected:
            output.append("\nAvailable to connect:")
            output.extend(disconnected)

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Operation timed out. Please try again."
    except Exception as e:
        return f"Error checking Bluetooth devices: {str(e)}"
