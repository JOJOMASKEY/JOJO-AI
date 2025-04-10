import re
import dateparser

def parse_reminder(text):
    text = text.lower().strip()

    # Pattern: remind me to [task] at [time]
    at_match = re.match(r"remind(?: me)? to (.+?) at (\d{1,2}(?::\d{2})?\s?(am|pm)?)", text)
    if at_match:
        task = at_match.group(1).strip()
        time_str = at_match.group(2).strip()
        parsed_time = dateparser.parse(time_str)
        if parsed_time:
            return {"task": task, "time": parsed_time.isoformat()}
        else:
            return None

    # Pattern: remind me to [task] [when]
    when_match = re.match(r"remind(?: me)? to (.+?) (tomorrow|next week|next month|in \d+ (minutes?|hours?|days?)|on \w+)", text)
    if when_match:
        task = when_match.group(1).strip()
        when = when_match.group(2).strip()
        parsed = dateparser.parse(when + " at 9am")  # default time
        if parsed:
            return {"task": task, "time": parsed.isoformat()}
        else:
            return None

    # Pattern: remind to [task] [when]
    simple_match = re.match(r"remind(?: me)? to (.+)", text)
    if simple_match:
        task_and_time = simple_match.group(1).strip()
        parsed = dateparser.parse(task_and_time)
        if parsed:
            return {"task": task_and_time, "time": parsed.isoformat()}

        # Handle vague "at 2"
        time_guess = re.match(r"(.+?) at (\d{1,2})$", task_and_time)
        if time_guess:
            return {
                "task": time_guess.group(1).strip(),
                "ambiguous_time": time_guess.group(2).strip()
            }

    return None


def parse_task(text):
    text = text.lower().strip()
    match = re.match(r"(add a task to|task:)\s*(.+)", text)
    if match:
        desc = match.group(2).strip()
        words = desc.split()
        for i in range(len(words)):
            maybe_time = " ".join(words[i:])
            parsed = dateparser.parse(maybe_time)
            if parsed:
                return {
                    "description": " ".join(words[:i]).strip(),
                    "time": parsed.isoformat()
                }
        return {"description": desc, "time": None}
