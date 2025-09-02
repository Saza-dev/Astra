import json
import os

HISTORY_FILE = "conversation_history.json"

# Load existing history
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        conversation_history = json.load(f)
else:
    conversation_history = []

def add_to_history(role, content):
    global conversation_history
    conversation_history.append({"role": role, "content": content})
    
    MAX_HISTORY = 10
    if len(conversation_history) > MAX_HISTORY:
        conversation_history = conversation_history[-MAX_HISTORY:]

    # Save to JSON
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, indent=4)
