from crewai.tools import tool

@tool("connect_wifi_tool")
def connect_wifi_tool(ssid: str) -> dict:
    """Connect to a saved Wi-Fi profile by SSID."""
    import subprocess, time
    if not ssid:
        return {"success": False, "message": "Provide an SSID to connect."}
    try:
        # Check saved profiles (case-insensitive)
        prof = subprocess.run(["netsh","wlan","show","profiles"], capture_output=True, text=True, timeout=10)
        exact = None
        for line in prof.stdout.splitlines():
            if "All User Profile" in line:
                name = line.split(":",1)[1].strip()
                if name.lower() == ssid.lower():
                    exact = name
                    break
        if not exact:
            return {"success": False, "message": f"Network '{ssid}' is not saved on this PC. Connect once manually first."}

        # Connect
        res = subprocess.run(["netsh","wlan","connect", f"name={exact}"], capture_output=True, text=True, timeout=15)
        if res.returncode != 0:
            return {"success": False, "message": f"Failed to connect to '{exact}'. {res.stderr or res.stdout}".strip()}

        time.sleep(2)
        ver = subprocess.run(["netsh","wlan","show","interfaces"], capture_output=True, text=True, timeout=10)
        connected = any(("SSID" in line and exact in line) for line in ver.stdout.splitlines())
        if connected:
            return {"success": True, "message": f"✅ Connected to '{exact}'"}
        return {"success": True, "message": f"Connection to '{exact}' initiated. Verification pending."}
    except subprocess.TimeoutExpired:
        return {"success": False, "message": "Connection attempt timed out."}
    except Exception as e:
        return {"success": False, "message": f"Error connecting to Wi-Fi: {e}"}
