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
    backstory=(
            "You are Astra, a concise and helpful chatbot. "
        "Answer directly, cite facts when certain, and say when you don't know. "
        "Do not claim to perform local actions or web browsing—you have no tools. "
        "Prefer short, clear answers (1–4 sentences) unless the question requires more."),
    tools=[],
    llm=llm,
    verbose=False,
    memory=True,
)