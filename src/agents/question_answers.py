from crewai import Agent, Task, Crew, LLM 

llm = LLM(model='groq/openai/gpt-oss-120b')

# QA Agent for general questions
qa_agent = Agent(
    role="Question Answering Chatbot",
    goal="Answer user questions clearly and accurately",
    backstory="You are a helpful chatbot that provides relevant, concise answers. Your name is KYLIE",
    tools=[],
    llm=llm,
    verbose=True
)