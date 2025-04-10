import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from fuzzywuzzy import fuzz

TASK_PATH = Path("data/tasks.json")
TASK_PATH.parent.mkdir(parents=True, exist_ok=True)

def add_task(description: str, time: str = ""):
    entry = {
        "description": description,
        "time": time,
        "timestamp": datetime.now().isoformat(),
        "tags": ["task"]
    }

    tasks = []
    if TASK_PATH.exists():
        with open(TASK_PATH, "r") as f:
            tasks = json.load(f)

    tasks.append(entry)

    with open(TASK_PATH, "w") as f:
        json.dump(tasks, f, indent=2)

def list_tasks():
    if not TASK_PATH.exists():
        print("📋 You don't have any tasks yet.")
        return

    with open(TASK_PATH, "r") as f:
        tasks = json.load(f)

    if not tasks:
        print("📋 Your task list is empty.")
        return

    print("\n📋 Your Tasks:")
    for i, task in enumerate(tasks, 1):
        time_info = f" (due {task.get('time', '')})" if task.get("time") else ""
        print(f"{i}. {task['description']}{time_info} ({task['timestamp'][:19]})")

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

def search_tasks(query: str):
    if not TASK_PATH.exists():
        print("🔍 You don’t have any tasks yet.")
        return

    with open(TASK_PATH, "r") as f:
        tasks = json.load(f)

    query = query.lower()
    query_hour = extract_time_from_query(query)
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    matches = []
    for t in tasks:
        desc = t["description"].lower()
        time_str = t.get("time", "")

        try:
            time_obj = datetime.fromisoformat(time_str)
        except (ValueError, TypeError):
            time_obj = None

        fuzzy_score = fuzz.partial_ratio(desc, query)
        match_hour = time_obj and query_hour is not None and time_obj.hour == query_hour
        match_today = time_obj and "today" in query and time_obj.date() == today
        match_tomorrow = time_obj and "tomorrow" in query and time_obj.date() == tomorrow

        if fuzzy_score >= 60 or match_hour or match_today or match_tomorrow:
            matches.append(t)

    if matches:
        print("🔍 Here's what I found in your tasks:")
        for task in matches:
            time_info = f" (due {task.get('time', '')})" if task.get("time") else ""
            print(f"- {task['description']}{time_info}")
    else:
        print("🔍 I couldn’t find any tasks related to that.")
