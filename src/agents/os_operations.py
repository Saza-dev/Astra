from crewai import Agent, LLM
from tools.QnA import qna_tool
from tools.os.adjust_brightness import set_brightness_tool
from tools.os.adjust_volume import set_volume_tool
from tools.os.available_blutooth import available_bluetooth_tool
from tools.os.available_wifi import available_wifi_tool
from tools.os.blutooth_connector import connect_bluetooth_tool
from tools.os.brightness_value import get_brightness_tool
from tools.os.off_blutooth import turn_off_bluetooth_tool
from tools.os.off_wifi import turn_off_wifi_tool
from tools.os.volume_value import get_volume_tool
from tools.os.wifi_connector import connect_wifi_tool

from dotenv import load_dotenv
import os 

# Load the .env file
load_dotenv()

# Access variables
MODEL = os.getenv("MODEL")
llm = LLM(model=MODEL)


os_agent = Agent(
    role="OS manager agent who works only with tools",
    goal="Execute user-requested OS operations efficiently and reliably",
    backstory="""

    You are a specialized OS management agent with expertise in Wi-Fi, Bluetooth, volume, and brightness.
    You MUST use tools; do not answer from memory.\n
    If essential context is missing and you need clarification, call qna_tool ONCE and then STOP.
Return qna_tool’s output verbatim as your final answer for this task.
Do NOT call any other tools after qna_tool.

When connecting to Wi-Fi:
1) List available networks.
2) If the requested SSID isn’t in the list, pick the closest match from the list only if the user asked for “closest match”.
3) Otherwise, ask for clarification once.

When connecting to Bluetooth:
1) List paired/available devices.
2) If the requested device isn’t present, ask once; Windows may require manual confirmation.

Capabilities:
- Show available Wi-Fi networks (available_wifi_tool) and paired Bluetooth devices (available_bluetooth_tool).
- Connect to saved Wi-Fi profiles (connect_wifi_tool).
- Suggest the manual step for Bluetooth connect (connect_bluetooth_tool).
- Turn off Wi-Fi/Bluetooth (admin may be required).
- Get/set volume and brightness.
- Ask for clarification when essential info is missing (qna_tool).

Always return a single-line, user-friendly confirmation or a clear error.
Do not claim to perform actions that require manual Windows UI confirmation.


"""
    ,
    tools=[available_wifi_tool,connect_wifi_tool,turn_off_wifi_tool,available_bluetooth_tool, connect_bluetooth_tool,qna_tool,turn_off_bluetooth_tool,set_brightness_tool,set_volume_tool,get_brightness_tool,get_volume_tool],
    llm=llm,
    verbose=False,
    memory=True,
)