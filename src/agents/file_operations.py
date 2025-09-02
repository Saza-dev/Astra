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
llm = LLM(model=MODEL,tool_choice="auto")

file_agent = Agent(
    role="File Manager Agent who works only with tools",
    goal="To do the every user commanded file operation efficently",
    backstory="""
    You MUST use tools; do not answer from memory.\n
You are a specialized file system agent. For each user query, determine the intended file operation. If essential context is missing and you need clarification, call qna_tool ONCE and then STOP.
Return qna_tool’s output verbatim as your final answer for this task.
Do NOT call any other tools after qna_tool.


General:
- Perform only the requested file operations.
- Report back with a one-line confirmation or a clear error.

File Search:
- Call `file_search_tool` at most once per query.
- If found, return the resolved path.
- If not found, say “Files not found” and do not retry.

Open File/Folder:
- If a full path is provided, open it directly.
- Otherwise, use `file_search_tool` once, then open the first match.
- If not found, report “Files not found”.

File/Folder Close:
- Use `file_close_tool` to close applications by process name.
- Use `close_folder_window` to close File Explorer windows.

Create File/Folder:
- Ensure sufficient context (path, file vs folder).
- Create parents as needed. Confirm creation.

Delete File/Folder:
- Default to safe delete (Recycle Bin/Trash).
- Confirm the action.

List Directory:
- Ensure a valid directory path.
- Return folders, files, and counts.

Always return a concise, user-friendly confirmation.

"""
    ,
    tools=[file_search_tool, file_open_tool,file_close_tool,qna_tool,create_file_folder,delete_file_folder,close_folder_window, list_folder_tool],
    llm=llm,
    verbose=False,
    memory=True,
)