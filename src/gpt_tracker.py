import json
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("data/gpt_usage_log.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

PRICING = {
    "gpt-3.5-turbo": 0.0015 / 1000,  # $ per token (input + output)
    "gpt-4": 0.03 / 1000,            # $ per token (input + output)
    "gpt-4-turbo": 0.01 / 1000
}

def log_gpt_usage(model, tokens_in, tokens_out, feature):
    cost_per_token = PRICING.get(model, 0.03 / 1000)
    total_tokens = tokens_in + tokens_out
    cost = round(total_tokens * cost_per_token, 6)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "feature": feature,
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost": cost
    }

    logs = []
    if LOG_PATH.exists():
        with open(LOG_PATH, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    return entry
    
from collections import defaultdict

def get_usage_summary():
    if not LOG_PATH.exists():
        return "🧾 No GPT usage has been logged yet."

    try:
        with open(LOG_PATH, "r") as f:
            logs = json.load(f)
    except json.JSONDecodeError:
        return "⚠️ GPT log file is corrupted or unreadable."

    summary = defaultdict(lambda: {"calls": 0, "cost": 0.0})

    for entry in logs:
        month = entry["timestamp"][:7]  # YYYY-MM
        model = entry["model"]
        key = f"{month} | {model}"
        summary[key]["calls"] += 1
        summary[key]["cost"] += entry["cost"]

    lines = ["📊 GPT Usage Summary:\n"]
    for key, data in sorted(summary.items()):
        lines.append(f"🗓 {key}: {data['calls']} calls, ${data['cost']:.4f}")
    return "\n".join(lines)
