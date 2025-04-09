import json
from datetime import datetime
from pathlib import Path

TASK_PATH = Path("data/tasks.json")
TASK_PATH.parent.mkdir(parents=True, exist_ok=True)

def add_task(description: str):
    entry = {
        "description": description,
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

    print("\n📌 Your Tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['description']} ({task['timestamp'][:19]})")

# self-documentation:
# Updated task module for content-based input on Apr 8, 2025
