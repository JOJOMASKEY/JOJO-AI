import json
from datetime import datetime
from pathlib import Path

USAGE_PATH = Path("data/gpt_usage.json")
USAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

MODEL_COST = {
    "gpt-3.5-turbo": 0.0001,  # dollars per call (example)
    "gpt-4": 0.00365
}

def log_gpt_call(model):
    now = datetime.now()
    month = now.strftime("%Y-%m")
    usage = {}

    if USAGE_PATH.exists():
        with open(USAGE_PATH, "r") as f:
            usage = json.load(f)

    if month not in usage:
        usage[month] = {}

    if model not in usage[month]:
        usage[month][model] = {"calls": 0, "cost": 0}

    usage[month][model]["calls"] += 1
    usage[month][model]["cost"] += MODEL_COST.get(model, 0)

    with open(USAGE_PATH, "w") as f:
        json.dump(usage, f, indent=2)

def get_usage_summary():
    if not USAGE_PATH.exists():
        return "🧾 No GPT usage logged yet."

    with open(USAGE_PATH, "r") as f:
        usage = json.load(f)

    lines = ["📊 GPT Usage Summary:\n"]
    for month, data in usage.items():
        for model, stats in data.items():
            cost = f"${stats['cost']:.4f}"
            lines.append(f"🗓 {month} | {model}: {stats['calls']} calls, {cost}")
    return "\n".join(lines)
