import json
import re
from datetime import datetime, timedelta
from pathlib import Path
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

def extract_time_from_query(query):
    query = query.lower().replace("at ", "").strip()
    matches = re.findall(r'\b(\d{1,2})(am|pm)\b', query)
    if matches:
        hour, period = matches[0]
        hour = int(hour)
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        return hour
    return None

def search_reminders(query: str):
    if not REMINDER_PATH.exists():
        print("🔍 You don’t have any reminders yet.")
        return

    with open(REMINDER_PATH, "r") as f:
        reminders = json.load(f)

    query = query.lower()
    query_hour = extract_time_from_query(query)
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    matches = []
    for r in reminders:
        task = r["task"].lower()
        time_str = r["time"]

        try:
            time_obj = datetime.fromisoformat(time_str)
        except ValueError:
            time_obj = None  # It's a string like "6pm"

        fuzzy_score = fuzz.partial_ratio(task, query)
        match_hour = time_obj and query_hour is not None and time_obj.hour == query_hour
        match_today = time_obj and "today" in query and time_obj.date() == today
        match_tomorrow = time_obj and "tomorrow" in query and time_obj.date() == tomorrow

        if fuzzy_score >= 60 or match_hour or match_today or match_tomorrow:
            matches.append(r)

    if matches:
        print("🔍 Here's what I found in your reminders:")
        for rem in matches:
            print(f"- {rem['task']} at {rem['time']}")
    else:
        print("🔍 I couldn’t find any reminders related to that.")
