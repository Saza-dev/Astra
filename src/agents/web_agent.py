# web_task.py
from crewai import Agent, LLM
from dotenv import load_dotenv
import os

from tools.web.web_tools import page_screenshot_b64, simple_search, visit_site
from tools.web.youtube.youtube_tool import youtube_control

load_dotenv()
llm = LLM(model=os.getenv("MODEL"))


WEB_AGENT_SYSTEM_RULES = """
Operating Rules:
- You MUST use tools; never answer from memory.
- Prefer headless browsing unless audio/video playback is explicitly requested.
- Return ONE concise line at the end: success confirmation or the key data.
- If a step fails, return ONE line: 'error: <what failed>'.
- When using `youtube_control`, ALWAYS pass a single argument named `payload`.
  - `payload` may be a JSON object or a JSON string.
  - Examples:
    Action: youtube_control
    Action Input: {"payload": {"action":"play_query","query":"Despacito","headless":false}}
    Action: youtube_control
    Action Input: {"payload": "{\"action\":\"volume\",\"percent\":20}"}
"""

web_agent = Agent(
    role="Web Manager",
    goal="Execute arbitrary web operations ONLY via tools and return a concise result.",
    backstory="A disciplined web operator that never hallucinates—uses tools for everything.",
    tools=[youtube_control, visit_site, simple_search, page_screenshot_b64],
    llm=llm,
    verbose=True,
    memory=False,
    constraints=[WEB_AGENT_SYSTEM_RULES],
)


