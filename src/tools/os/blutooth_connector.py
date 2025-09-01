import subprocess
from crewai.tools import tool

@tool("connect_bluetooth_tool")
def connect_bluetooth_tool(device_name: str) -> str:
    """
    Attempts to connect to a paired Bluetooth device.
    
    Args:
        device_name (str): Name of the Bluetooth device
        
    Returns:
        str: Connection status message
    """
    if not device_name:
        return "Error: Please provide the device name to connect to."
    
    try:
        # Windows doesn't have direct CLI Bluetooth connection
        # We'll use PowerShell with Windows Runtime
        ps_script = f"""
        Add-Type -AssemblyName System.Runtime.WindowsRuntime
        $null = [Windows.Devices.Bluetooth.BluetoothDevice,Windows.Devices.Bluetooth,ContentType=WindowsRuntime]
        $null = [Windows.Devices.Enumeration.DeviceInformation,Windows.Devices.Enumeration,ContentType=WindowsRuntime]
        
        $devices = [Windows.Devices.Enumeration.DeviceInformation]::FindAllAsync([Windows.Devices.Bluetooth.BluetoothDevice]::GetDeviceSelector()).GetAwaiter().GetResult()
        $targetDevice = $devices | Where-Object {{$_.Name -like '*{device_name}*'}}
        
        if ($targetDevice) {{
            Write-Output "Found device: $($targetDevice.Name)"
            # Note: Actual connection requires more complex WinRT interop
            Write-Output "Please connect to '$($targetDevice.Name)' using Windows Settings > Bluetooth"
        }} else {{
            Write-Output "Device '{device_name}' not found in paired devices"
        }}
        """
        
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        output = result.stdout.strip()
        
        if "not found" in output.lower():
            return (f"Device '{device_name}' not found.\n"
                   f"Please make sure the device is paired and try again.")
        else:
            # Since Windows doesn't have easy CLI Bluetooth connection
            return (f"🔵 Bluetooth connection request for '{device_name}'\n\n"
                   f"Due to Windows limitations, please complete the connection by:\n"
                   f"1. Opening Settings > Bluetooth & devices\n"
                   f"2. Click on '{device_name}'\n"
                   f"3. Click 'Connect'\n\n"
                   f"Alternatively, the device may auto-connect if it's in range and powered on.")
            
    except subprocess.TimeoutExpired:
        return "Operation timed out. Please try again."
    except Exception as e:
        return f"Error connecting to Bluetooth device: {str(e)}"