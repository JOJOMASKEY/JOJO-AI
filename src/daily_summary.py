import json
from datetime import datetime
from pathlib import Path
import dateparser

REMINDER_PATH = Path("data/reminders.json")
TASK_PATH = Path("data/tasks.json")

def show_daily_summary():
    today = datetime.now().date()
    summary = {"reminders": [], "tasks": []}

    # Load reminders
    if REMINDER_PATH.exists():
        with open(REMINDER_PATH, "r") as f:
            reminders = json.load(f)
        for r in reminders:
            parsed_time = dateparser.parse(r.get("time", ""))
            if parsed_time and parsed_time.date() == today:
                summary["reminders"].append(r)

    # Load tasks
    if TASK_PATH.exists():
        with open(TASK_PATH, "r") as f:
            tasks = json.load(f)
        for t in tasks:
            parsed_time = dateparser.parse(t.get("due", ""))
            if parsed_time and parsed_time.date() == today:
                summary["tasks"].append(t)

    # Display summary
    print("\n📆 Here's what's on your schedule today:")
    if not summary["reminders"] and not summary["tasks"]:
        print("✅ No reminders or tasks for today!")
    else:
        if summary["reminders"]:
            print("\n🔔 Reminders:")
            for r in summary["reminders"]:
                print(f"- {r['task']} at {r['time']}")
        if summary["tasks"]:
            print("\n📋 Tasks:")
            for t in summary["tasks"]:
                due = f" (due {t['due']})" if "due" in t else ""
                print(f"- {t['description']}{due}")
