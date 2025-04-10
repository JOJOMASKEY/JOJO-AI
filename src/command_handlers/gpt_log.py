import json
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("data/gpt_fallback_log.json")

def show_gpt_log(dev_mode: bool = False, limit: int = 5):
    if not LOG_PATH.exists():
        print("🔍 I don’t have any past AI responses stored.")
        return

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    recent_logs = logs[-limit:]

    print(f"\n📜 Here are the last {len(recent_logs)} answers I gave:\n")
    for log in recent_logs:
        ts = datetime.fromisoformat(log["timestamp"]).strftime("%b %d, %H:%M")
        if dev_mode:
            print(f"📅 {ts} | Model: {log.get('model_used', 'gpt-?')}")
            print(f"Q: {log['query']}")
            print(f"A: {log['response']}\n")
        else:
            print(f"🕑 {ts}")
            print(f"Q: {log['query']}")
            print(f"A: {log['response']}\n")
