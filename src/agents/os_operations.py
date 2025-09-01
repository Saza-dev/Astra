from crewai import Agent, LLM
from tools.QnA import qna_tool
from tools.os.available_blutooth import available_bluetooth_tool
from tools.os.available_wifi import available_wifi_tool
from tools.os.blutooth_connector import connect_bluetooth_tool
from tools.os.off_blutooth import turn_off_bluetooth_tool
from tools.os.off_wifi import turn_off_wifi_tool
from tools.os.wifi_connector import connect_wifi_tool

llm = LLM(model='groq/openai/gpt-oss-120b')

os_agent = Agent(
    role="OS manager agent",
    goal="Execute user-requested OS operations efficiently and reliably",
    backstory="""
    You are a specialized OS management agent with expertise in network connectivity.
    You handle Wi-Fi and Bluetooth operations with precision and clarity.
    To connect to a wifi network:
    1. check for available wifi devices 
    2. check if the user entered wifi name is presented in the available wifi devices list 
    3. if not presented in the available wifi devices list use the most similar network in the list as the name to connect
    To connect a bluetooth device:
    1. check for available bluetooth devices 
    2. check if the user entered blutooth name is presented in the available bluetooth devices list 
    3. if not presented in the available bluetooth devices list use the most similar network in the list as the name to connect.
    also you have capabilities to:
    - show saved Wi-Fi networks using available_wifi_tool
    - show paired Bluetooth devices using available_blutooth_tool
    - Disabling Wi-Fi and Bluetooth adapters
    - Asking for clarification when needed using qna tool
    - Providing clear status reports
    Always use the appropriate tool for each task and provide clear feedback. If you dont have the tool you need to perform the required task just say you dont have the tool to do it.
"""
    ,
    tools=[available_wifi_tool,connect_wifi_tool,turn_off_wifi_tool,available_bluetooth_tool, connect_bluetooth_tool,qna_tool,turn_off_bluetooth_tool],
    llm=llm,
    verbose=True,
    memory=True,
)