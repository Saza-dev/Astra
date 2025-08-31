from crewai import Agent, LLM
from src.tools.files.file_opener import file_open_tool
from tools.files.file_searcher import file_search_tool


llm = LLM(model='groq/openai/gpt-oss-120b')

file_agent = Agent(
    role="File Manager Agent",
    goal="Search for files based on user queries and open the most relevant one",
    backstory="""You are a specialized file system agent. When given a query:
    1. First search for files matching the query
    2. If files are found, open the most relevant one
    3. Report back with the action taken""",
    tools=[file_search_tool, file_open_tool],
    llm=llm,
)