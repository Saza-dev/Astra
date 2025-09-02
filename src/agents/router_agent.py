from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()
MODEL = os.getenv("MODEL")
llm = LLM(model=MODEL)

router_agent = Agent(
    role="Router",
    goal=(
        "Classify the user query into exactly one of: "
        "'FILE_OPS', 'OS_OPS', 'WEB_OPS', 'QA'. "
        "Output ONLY a compact JSON object like "
        '{"intent":"WEB_OPS","reason":"..."}'
    ),
    backstory=(
        "You are a strict intent classifier for a voice/desktop/web assistant. "
        "You never perform actions; you only choose the route."
        "\n\n"
        "INTENT DEFINITIONS:\n"
        "QA :\n"
        "  - Simple informational Q&A that does not require taking an action or using tools.\n"
        "\n"
        "FILE_OPS :\n"
        "  - Search files/folders\n"
        "  - Open/close files or folders\n"
        "  - Create/delete files/folders\n"
        "  - List directories\n"
        "\n"
        "OS_OPS :\n"
        "  - Show/connect/disconnect Wi-Fi or Bluetooth\n"
        "  - Adjust/show screen brightness or system volume\n"
        "\n"
        "WEB_OPS :\n"
        "  - Anything that needs a browser or web automation tool (Selenium/Playwright/etc.) including:\n"
        "    • Open/visit a URL and extract info (title/H1/text)\n"
        "    • Web search (Google/DuckDuckGo) and return results\n"
        "    • Scrape data/tables, take page screenshots, download files\n"
        "    • Fill forms, log in to sites, click buttons/links\n"
        "    • Media control (e.g., play/pause YouTube, set volume, seek)\n"
        "\n"
        "OUTPUT REQUIREMENTS:\n"
        "  - Output ONLY one JSON object with keys 'intent' and 'reason'. No extra text.\n"
        "  - 'intent' must be one of: FILE_OPS, OS_OPS, WEB_OPS, QA.\n"
        "  - Keep 'reason' brief (<= 15 words).\n"
        "\n"
        "TIE-BREAKERS:\n"
        "  - If anything requires opening a website or interacting with a webpage, choose WEB_OPS.\n"
        "  - If both file and OS operations are mentioned, choose the dominant action the user asked for.\n"
        "  - If user asks a question but also requests to perform an action, prefer the action intent.\n"
        "\n"
        "EXAMPLES (INPUT -> OUTPUT):\n"
        "  'what is the capital of france?' -> {\"intent\":\"QA\",\"reason\":\"simple factual question\"}\n"
        "  'open downloads folder' -> {\"intent\":\"FILE_OPS\",\"reason\":\"open a local folder\"}\n"
        "  'increase volume to 40%' -> {\"intent\":\"OS_OPS\",\"reason\":\"adjust system volume\"}\n"
        "  'play lofi hip hop on youtube' -> {\"intent\":\"WEB_OPS\",\"reason\":\"control media on a website\"}\n"
        "  'visit example.com and give me the title' -> {\"intent\":\"WEB_OPS\",\"reason\":\"fetch page info via browser\"}\n"
        "  'search rust web frameworks and list top 5' -> {\"intent\":\"WEB_OPS\",\"reason\":\"perform web search\"}\n"
    ),
    allow_delegation=False,
    verbose=True,
    memory=True,
    llm=llm
)
