import re
from datetime import datetime
import dateparser

def parse_reminder(text: str) -> dict:
    # Normalize text
    text = text.strip().lower()

    # Basic pattern: "remind me to [task] at [time]"
    match = re.search(r"remind(?: me)? to (.+?) at (.+)", text)
    if not match:
        return {"task": None, "time": None, "ambiguous_time": None}

    task = match.group(1).strip()
    time_str = match.group(2).strip()

    # Handle ambiguous time like "6"
    if re.fullmatch(r"\d{1,2}", time_str):
        return {"task": task, "time": None, "ambiguous_time": time_str}

    # Try to parse time
    parsed_time = dateparser.parse(time_str, settings={"PREFER_DATES_FROM": "future"})
    if parsed_time:
        return {
            "task": task,
            "time": parsed_time.isoformat(),
            "ambiguous_time": None
        }

    # Fallback if parse fails
    return {"task": task, "time": None, "ambiguous_time": time_str}

def parse_task(text: str) -> dict:
    text = text.strip().lower()

    match = re.search(r"(?:add a task to|task:)\s*(.+?)(?:\s+(?:in|by|on|at)\s+(.+))?$", text)
    if not match:
        return {"description": None, "time": None}

    description = match.group(1).strip()
    time_str = match.group(2).strip() if match.group(2) else None

    parsed_time = None
    if time_str:
        parsed = dateparser.parse(time_str, settings={"PREFER_DATES_FROM": "future"})
        if parsed:
            parsed_time = parsed.isoformat()

    return {
        "description": description,
        "time": parsed_time
    }
