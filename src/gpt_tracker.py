import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

LOG_PATH = Path("data/gpt_fallback_log.json")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# === Logger ===
def log_gpt_call(model: str, prompt_tokens: int = 0, completion_tokens: int = 0):
    cost = estimate_cost(model, prompt_tokens, completion_tokens)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
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

# === Estimator ===
def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    # Token costs based on OpenAI rates
    if model == "gpt-3.5-turbo":
        return (prompt_tokens + completion_tokens) * 0.0015 / 1000
    elif model == "gpt-4":
        return prompt_tokens * 0.03 / 1000 + completion_tokens * 0.06 / 1000
    return 0.0

# === Summarizer ===
def get_gpt_usage_summary():
    if not LOG_PATH.exists():
        return "No GPT usage logged yet."

    with open(LOG_PATH, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            return "⚠️ GPT log file is corrupted."

    summary = defaultdict(lambda: defaultdict(lambda: {"calls": 0, "cost": 0.0}))

    for log in logs:
        try:
            dt = datetime.fromisoformat(log["timestamp"])
            month = dt.strftime("%Y-%m")
            model = log["model"]
            summary[month][model]["calls"] += 1
            summary[month][model]["cost"] += log.get("cost", 0.0)
        except Exception:
            continue

    output = "📊 GPT Usage Summary:\n"
    for month in sorted(summary.keys()):
        for model in summary[month]:
            calls = summary[month][model]["calls"]
            cost = summary[month][model]["cost"]
            output += f"\n🗓 {month} | {model}: {calls} calls, ${cost:.4f}"

    return output
