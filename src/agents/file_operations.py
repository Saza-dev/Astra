from crewai import Agent, LLM
from src.tools.files.file_opener import file_open_tool
from tools.QnA import qna_tool
from tools.files.create_file_folder import create_file_folder
from tools.files.delete_file_folder import delete_file_folder
from tools.files.file_close_tool import file_close_tool
from tools.files.file_searcher import file_search_tool
from tools.files.folder_close_tool import close_folder_window
from tools.files.list_folder_tool import list_folder_tool

from dotenv import load_dotenv
import os 

# Load the .env file
load_dotenv()

# Access variables
MODEL = os.getenv("MODEL")
llm = LLM(model=MODEL)

file_agent = Agent(
    role="File Manager Agent",
    goal="To do the every user commanded file operation efficently",
    backstory="""You are a specialized file system agent. When given a query:
    check if the query and decide the file operation if you can't do that just say that you cant do it. 
    To each operation you must follow the below seperated rules.
    Always Ask from the user if u think the given context is not enough and wait for the user input again and then continue the tool use.
    File Search Rules:
    - Only call `file_search_tool` ONCE per query.
    - If the file is found return the file path.
    - If not found, return 'Files not found' without retrying.
    - Never repeat the search for the same query.
    File Open Rules:
    - Only call `file_search_tool` ONCE per query.
    - If the file is found, immediately call `file_open_tool` with the path.
    - If not found, return 'Files not found' without retrying.
    - Never repeat the search for the same query.
    File.folder close Rules:
    - Use file_close_tool to close running applications (by process name).
    - Use close_folder_window to close a folder
    Create file / folder Rules:
    - make sure the context is enough to create a file or a folder 
    - always report back the action
    Delete File / folder Rules:
    - make sure the context is enough to delete a file or a folder 
    - always report back the action 
    List Directories and folders :
    - make sure the context is enough to delete a file or a folder 
    - always report back the action 


always Report back with the action taken"""
    ,
    tools=[file_search_tool, file_open_tool,file_close_tool,qna_tool,create_file_folder,delete_file_folder,close_folder_window, list_folder_tool],
    llm=llm,
    verbose=True,
    memory=True
)