import json
from datetime import datetime
from pathlib import Path

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
        print("📝 You don't have any notes yet.")
        return

    with open(NOTE_PATH, "r") as f:
        notes = json.load(f)

    if not notes:
        print("📝 Your notes list is empty.")
        return

    print("\n🗒️ Your Notes:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['content']} ({note['timestamp'][:19]})")

# self-documentation:
# Updated note module for content-based input on Apr 8, 2025
