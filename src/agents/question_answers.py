from crewai import Agent, LLM 

from dotenv import load_dotenv
import os 

# Load the .env file
load_dotenv()

# Access variables
MODEL = os.getenv("MODEL")
llm = LLM(model=MODEL)


# QA Agent for general questions
qa_agent = Agent(
    role="Question Answering Chatbot",
    goal="Answer user questions clearly and accurately",
    backstory="You are a helpful chatbot that provides relevant, concise answers. Your name is KYLIE",
    tools=[],
    llm=llm,
    verbose=True
)