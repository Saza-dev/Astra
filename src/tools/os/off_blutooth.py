import subprocess
import ctypes
from crewai.tools import tool
import sys

@tool("turn_off_bluetooth_tool")
def turn_off_bluetooth_tool() -> str:
    """
    Completely disables Bluetooth adapters on Windows.
    Requires Administrator privileges.

    Returns:
        str: Real success or failure message
    """
    try:
        # Check for admin privileges
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            is_admin = False

        if not is_admin:
            return (
                "⚠️ Administrator privileges are required to completely disable Bluetooth.\n\n"
                "Please run this script as Administrator or disable Bluetooth manually:\n"
                "• Windows Settings > Bluetooth & devices > Turn off Bluetooth\n"
                "• Or use Device Manager to disable the Bluetooth adapter\n"
                "• Or use the Bluetooth icon in the system tray"
            )

        # PowerShell command to disable all active Bluetooth adapters
        ps_cmd = [
            "powershell", "-Command",
            """
            $radios = Get-PnpDevice -Class 'Bluetooth' -Status OK
            if ($radios) {
                $radios | Disable-PnpDevice -Confirm:$false -ErrorAction Stop
                Start-Sleep -Seconds 1
                # Verify
                $disabled = Get-PnpDevice -Class 'Bluetooth' | Where-Object {$_.Status -ne 'OK'}
                if ($disabled) { Write-Output 'Bluetooth adapters have been successfully disabled.' } 
                else { Write-Output 'Failed to disable Bluetooth adapters.' }
            } else {
                Write-Output 'No active Bluetooth adapters found.'
            }
            """
        ]

        result = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=20)
        output = result.stdout.strip() or result.stderr.strip()
        return output

    except subprocess.TimeoutExpired:
        return "Operation timed out. Please try again."
    except Exception as e:
        return f"Error disabling Bluetooth: {str(e)}"
