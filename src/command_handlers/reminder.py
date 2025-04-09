import json
from datetime import datetime
from pathlib import Path

REMINDER_PATH = Path("data/reminders.json")
REMINDER_PATH.parent.mkdir(parents=True, exist_ok=True)

def add_reminder(task: str, time: str):
    entry = {
        "task": task,
        "time": time,
        "timestamp": datetime.now().isoformat(),
        "tags": ["reminder"]
    }

    reminders = []
    if REMINDER_PATH.exists():
        with open(REMINDER_PATH, "r") as f:
            reminders = json.load(f)

    reminders.append(entry)

    with open(REMINDER_PATH, "w") as f:
        json.dump(reminders, f, indent=2)

def list_reminders():
    if not REMINDER_PATH.exists():
        print("🔔 You don't have any reminders yet.")
        return

    with open(REMINDER_PATH, "r") as f:
        reminders = json.load(f)

    if not reminders:
        print("🔔 Your reminder list is empty.")
        return

    print("\n🔔 Your Reminders:")
    for i, rem in enumerate(reminders, 1):
        print(f"{i}. {rem['task']} at {rem['time']} ({rem['timestamp'][:19]})")

# self-documentation:
# Updated reminder module for content-based input on Apr 8, 2025
