import json
from dotenv import load_dotenv
from crewai import Task, Crew
from agents.router_agent import router_agent
from core.history import add_to_history, conversation_history
import re

load_dotenv()

def Kylie(q):
    router_task = Task(
        description=(
            "User query:\n"
            f"{q}\n\n"
            "Respond ONLY as JSON with keys 'intent' (FILE_OPS|OS_OPS|QA) and 'reason'."
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

    history_prompt = "\n".join([f"{h['role']}: {h['content']}" for h in conversation_history])

    if intent == "FILE_OPS":
        task = Task(
            description=f"Process the file request: {q}\nPerform only the requested file operations.",
            expected_output="A one-line confirmation of the file operation or a clear error message.",
            agent=file_agent,
        )
        crew = Crew(agents=[file_agent], tasks=[task], verbose=True)
        result = crew.kickoff()

    elif intent == "OS_OPS":
        task = Task(
            description=f"Process the OS request: {q}\nUse available OS tools and confirm results.",
            expected_output="A one-line confirmation of the OS operation or a clear error message.",
            agent=os_agent,
        )
        crew = Crew(agents=[os_agent], tasks=[task], verbose=True)
        result = crew.kickoff()

    else:
        add_to_history("user", q)
        task = Task(
            description=f"{history_prompt}\n\nAnswer this question: {q}",
            expected_output="A concise, correct answer.",
            agent=qa_agent,
        )
        crew = Crew(agents=[qa_agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        add_to_history("agent", str(result))

    return str(result)
