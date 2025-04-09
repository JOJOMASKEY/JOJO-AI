import json
from datetime import datetime, timedelta
from pathlib import Path
import dateparser
from fuzzywuzzy import fuzz

TASK_PATH = Path("data/tasks.json")
TASK_PATH.parent.mkdir(parents=True, exist_ok=True)

def add_task(description: str, time: str = None):
    entry = {
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "tags": ["task"]
    }
    if time:
        entry["due"] = time

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
        due = f" (due {task['due']})" if "due" in task else ""
        print(f"{i}. {task['description']}{due} ({task['timestamp'][:19]})")

def search_tasks(query: str):
    if not TASK_PATH.exists():
        print("🔍 You don’t have any tasks yet.")
        return

    with open(TASK_PATH, "r") as f:
        tasks = json.load(f)

    query_words = set(query.lower().split())
    now = datetime.now()

    target_time = None
    for word in query_words:
        parsed_time = dateparser.parse(word, settings={"PREFER_DATES_FROM": "future"})
        if parsed_time:
            target_time = parsed_time
            break

    results = []

    for task in tasks:
        desc = task["description"].lower()
        fuzzy_score = fuzz.partial_ratio(desc, query.lower())
        match_text = fuzzy_score >= 70

        task_time = dateparser.parse(task.get("due")) if "due" in task else None
        match_time = False

        if "today" in query_words or "for today" in query:
            if task_time and task_time.date() == now.date():
                match_time = True
        elif "tomorrow" in query_words or "for tomorrow" in query:
            if task_time and task_time.date() == (now + timedelta(days=1)).date():
                match_time = True
        elif target_time and task_time:
            delta = abs((task_time - target_time).total_seconds())
            if delta <= 1800:
                match_time = True

        if match_text or match_time:
            results.append(task)

    if results:
        print("🔍 Here's what I found in your tasks:")
        for t in results:
            due = f" (due {t['due']})" if "due" in t else ""
            print(f"- {t['description']}{due}")
    else:
        print("🔍 I couldn’t find any tasks related to that.")
