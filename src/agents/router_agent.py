from crewai import Agent,LLM

from dotenv import load_dotenv
import os 

# Load the .env file
load_dotenv()

# Access variables
MODEL = os.getenv("MODEL")
llm = LLM(model=MODEL)


router_agent = Agent(
    role="Router",
    goal=(
        "Classify the user query into one of: "
        "'FILE_OPS', 'OS_OPS', 'QA'. "
        "Output ONLY a compact JSON object like "
        '{"intent":"FILE_OPS","reason":"..."}'
    ),
    backstory=(
        "You are a strict intent classifier for a voice/desktop assistant. "
        "You never perform actions; you only choose the route."
        """
        
        QA :
          - For simple user questions that dosent need any action.

        FILE_OPS contains :
          - Search Files/Folders 
          - Open Files/Folders
          - close running applications/folders
          - create files/folders
          - delete files/folders
          - list directories and folders

        OS_OPS contains : 
          - Show/Connect/Disconnect wifi, blutooth devices
          - Adjust/Show Screen brightness and volume

        """
    ),
    allow_delegation=False,
    verbose=True,
    llm = llm 
)
