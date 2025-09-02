import json
from dotenv import load_dotenv
from crewai import Task, Crew
from agents.web_agent import web_agent
from agents.router_agent import router_agent
from core.history import add_to_history, conversation_history
import re

load_dotenv()

def _handle_possible_qna(result, base_desc, agent, expected_output, rounds=2):
    """Detect __QNA__ markers, ask in terminal, and re-run with appended context."""
    desc = base_desc
    last = result
    for _ in range(rounds):
        if isinstance(last, str) and last.startswith("__QNA__:"):
            ask = last.split(":", 1)[1]
            print("Assistant:", ask)
            ans = input("user: ").strip()
            desc += f"\n\nUser clarification: {ans}"
            task = Task(description=desc, expected_output=expected_output, agent=agent)
            crew = Crew(agents=[agent], tasks=[task], verbose=False)
            last = crew.kickoff()
        else:
            break
    return last

def Astra(q):

    history_prompt = "\n".join([f"{h['role']}: {h['content']}" for h in conversation_history])

    add_to_history("user", q)
    # Route to intent
    router_task = Task(
        description=(
            f"{history_prompt}\n\n"
            "User query:\n"
            f"{q}\n\n"
            "Respond ONLY as JSON with keys 'intent' (FILE_OPS|OS_OPS|WEB_OPS|QA) and 'reason'."
        ),
        expected_output='{"intent":"FILE_OPS|OS_OPS|QA","reason":"..."}',
        agent=router_agent,
    )
    router_crew = Crew(agents=[router_agent], tasks=[router_task], verbose=False)
    raw = str(router_crew.kickoff()).strip()

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group())
            intent = parsed.get("intent", "QA").upper()
        except Exception:
            intent = "QA"
    else:
        intent = "QA"

    from src.agents.file_operations import file_agent
    from src.agents.question_answers import qa_agent
    from src.agents.os_operations import os_agent

    

    if intent == "FILE_OPS":
        base_desc = f"{history_prompt}\n\nProcess the file request: {q}\nPerform only the requested file operations. You MUST use tools; do not answer from memory.\n"
        expected = "A one-line confirmation of the file operation or a clear error message."
        task = Task(description=base_desc, expected_output=expected, agent=file_agent)
        crew = Crew(agents=[file_agent], tasks=[task], verbose=False)
        result = crew.kickoff()
        result = _handle_possible_qna(result, base_desc, file_agent, expected, rounds=3)

    elif intent == "OS_OPS":
        base_desc = f"{history_prompt}\n\nProcess the OS request: {q}\nUse available OS tools and confirm results. You MUST use tools; do not answer from memory.\n"
        expected = "A one-line confirmation of the OS operation or a clear error message."
        task = Task(description=base_desc, expected_output=expected, agent=os_agent)
        crew = Crew(agents=[os_agent], tasks=[task], verbose=False)
        result = crew.kickoff()
        result = _handle_possible_qna(result, base_desc, os_agent, expected, rounds=3)
    
    elif intent == "WEB_OPS":

        COMMON_RULES = """
        Rules:
        - You MUST use tools; do not answer from memory.
        - Choose the single best tool (or a short sequence) to fulfill the request.
        - Prefer headless browsing unless audio/video playback is explicitly requested.
        - Return a ONE-LINE final answer: either a short confirmation or key data.
        - If something fails, return a clear one-line error describing which step failed.
        - When using youtube_control, pass a single argument named 'payload' (dict or JSON string).
        """

        base_desc = (
            f"{history_prompt}\n\n"
            f"User request: {q}\n"
            f"{COMMON_RULES}\n"
            "Examples:\n"
            "- 'Open https://example.com and give me the title' -> visit_site(url)\n"
            "- 'Search for top 5 Rust frameworks' -> simple_search(query)\n"
            "- 'Play lofi hip hop on YouTube at 20% volume' -> call youtube_control twice:\n"
            "   Action: youtube_control\n"
            "   Action Input: {\"payload\": {\"action\":\"play_query\",\"query\":\"lofi hip hop\",\"headless\":false}}\n"
            "   Action: youtube_control\n"
            "   Action Input: {\"payload\": {\"action\":\"volume\",\"percent\":20}}\n"
            "- 'Screenshot this page' -> page_screenshot_b64(url)\n"
        )

        expected = "Return exactly one line: success confirmation or a short data snippet."

        task = Task(description=base_desc, expected_output=expected, agent=web_agent)
        crew = Crew(agents=[web_agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        result = _handle_possible_qna(result, base_desc, web_agent, expected, rounds=3)

    else:
        
        base_desc = f"{history_prompt}\n\nAnswer this question: {q}"
        expected = "A concise, correct answer."
        task = Task(description=base_desc, expected_output=expected, agent=qa_agent)
        crew = Crew(agents=[qa_agent], tasks=[task], verbose=False)
        result = crew.kickoff()
        result = _handle_possible_qna(result, base_desc, qa_agent, expected, rounds=3)
        
    add_to_history("agent", str(result))
    return str(result)
