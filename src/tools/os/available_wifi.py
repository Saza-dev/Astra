import subprocess
import json
from crewai.tools import tool

@tool("available_wifi_tool")
def available_wifi_tool() -> dict:
    """Lists available Wi-Fi networks; marks [CONNECTED]/[SAVED]."""
    import subprocess
    try:
        nets_proc = subprocess.run(["netsh","wlan","show","networks","mode=bssid"], capture_output=True, text=True, timeout=10)
        prof_proc = subprocess.run(["netsh","wlan","show","profiles"], capture_output=True, text=True, timeout=10)
        iface_proc = subprocess.run(["netsh","wlan","show","interfaces"], capture_output=True, text=True, timeout=10)

        # Parse saved profiles
        saved = []
        for line in prof_proc.stdout.splitlines():
            if "All User Profile" in line:
                saved.append(line.split(":",1)[1].strip())

        # Parse current SSID
        current = None
        for line in iface_proc.stdout.splitlines():
            if "SSID" in line and ":" in line and "BSSID" not in line:
                current = line.split(":",1)[1].strip()
                break

        # Parse available nets
        networks, cur = [], {}
        for line in nets_proc.stdout.splitlines():
            if "SSID" in line and ":" in line:
                if cur:
                    networks.append(cur)
                ssid = line.split(":",1)[1].strip()
                cur = {"ssid": ssid, "signal": None}
            elif "Signal" in line and cur:
                s = line.split(":",1)[1].strip().replace("%","")
                cur["signal"] = int(s) if s.isdigit() else None
        if cur:
            networks.append(cur)

        return {"success": True, "message": "OK", "current": current, "saved": saved, "networks": networks}
    except subprocess.TimeoutExpired:
        return {"success": False, "message": "Wi-Fi scan timed out."}
    except Exception as e:
        return {"success": False, "message": f"Error scanning Wi-Fi: {e}"}
