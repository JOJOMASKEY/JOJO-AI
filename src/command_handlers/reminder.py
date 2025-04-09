import json
from datetime import datetime, timedelta
from pathlib import Path
import dateparser
from fuzzywuzzy import fuzz

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

def search_reminders(query: str):
    if not REMINDER_PATH.exists():
        print("🔍 You don’t have any reminders yet.")
        return

    with open(REMINDER_PATH, "r") as f:
        reminders = json.load(f)

    query_words = set(query.lower().split())
    now = datetime.now()

    target_time = None
    for word in query_words:
        parsed_time = dateparser.parse(word, settings={"PREFER_DATES_FROM": "future"})
        if parsed_time:
            target_time = parsed_time
            break

    results = []

    for rem in reminders:
        task_text = rem["task"].lower()
        rem_time = dateparser.parse(rem["time"]) if "time" in rem else None

        # Check fuzzy match
        fuzzy_score = fuzz.partial_ratio(task_text, query.lower())
        match_text = fuzzy_score >= 70

        # Match by day
        match_time = False
        if "today" in query_words or "for today" in query:
            if rem_time and rem_time.date() == now.date():
                match_time = True
        elif "tomorrow" in query_words or "for tomorrow" in query:
            if rem_time and rem_time.date() == (now + timedelta(days=1)).date():
                match_time = True
        elif target_time and rem_time:
            delta = abs((rem_time - target_time).total_seconds())
            if delta <= 1800:
                match_time = True

        if match_text or match_time:
            results.append(rem)

    if results:
        print("🔍 Here's what I found in your reminders:")
        for r in results:
            print(f"- {r['task']} at {r['time']}")
    else:
        print("🔍 I couldn’t find any reminders related to that.")
