import json
from datetime import datetime
from pathlib import Path
from fuzzywuzzy import fuzz
import re


NOTE_PATH = Path("data/notes.json")
NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)

def add_note(content: str):
    entry = {
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "tags": ["note"]
    }

    notes = []
    if NOTE_PATH.exists():
        with open(NOTE_PATH, "r") as f:
            notes = json.load(f)

    notes.append(entry)

    with open(NOTE_PATH, "w") as f:
        json.dump(notes, f, indent=2)

def list_notes():
    if not NOTE_PATH.exists():
        print("🗒️ You don't have any notes yet.")
        return

    with open(NOTE_PATH, "r") as f:
        notes = json.load(f)

    if not notes:
        print("🗒️ Your note list is empty.")
        return

    print("\n🗒️ Your Notes:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['content']} ({note['timestamp'][:19]})")

def search_notes(query: str):
    if not NOTE_PATH.exists():
        print("🔍 You don’t have any notes yet.")
        return

    with open(NOTE_PATH, "r") as f:
        notes = json.load(f)

    query = query.lower().strip().replace("tommorow", "tomorrow")
    query_words = set(re.sub(r"[^\w\s]", "", query).split())
    matches = []

    for note in notes:
        content = note["content"].lower().replace(":", "").strip()
        plain_text = re.sub(r"[^\w\s]", "", content)
        fuzzy_score = fuzz.partial_ratio(plain_text, query)
        keyword_match = any(word in plain_text for word in query_words)

        if fuzzy_score >= 60 or keyword_match:
            matches.append(note)

    if matches:
        print("🔍 Here's what I found in your notes:")
        for n in matches:
            print(f"- {n['content']} ({n['timestamp'][:19]})")
    else:
        print("🔍 I couldn’t find any notes related to that.")
