import os 
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()


def Chat_Agent(q):
    llm = LLM(model='groq/llama3-70b-8192')

    qa_agent = Agent(
        role="Question Answering Chatbot",
        goal="Answer user questions clearly and accurately",
        backstory="You are a helpful chatbot that provides relevant, concise answers. Your name is KYLIE",
        tools=[],
        llm=llm
    )

    qa_task = Task(
        description="Answer the following user question:\n\n{question}",
        expected_output="A clear and concise answer addressing the user's question in one short user friendly sentence",
        agent=qa_agent
    )

    crew = Crew(
        agents=[qa_agent],
        tasks=[qa_task],
    )

    result = crew.kickoff(inputs={'question':q})
    return str(result)