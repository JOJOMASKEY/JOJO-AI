import sys
import os
import re
from fuzzywuzzy import fuzz

# Add /src to system path
sys.path.append(os.path.abspath("src"))

import jojo_memory as memory
from command_handlers.reminder import add_reminder, list_reminders, search_reminders
from command_handlers.task import add_task, list_tasks, search_tasks
from command_handlers.note import add_note, list_notes, search_notes
from command_handlers.gpt_log import show_gpt_log
from absorb_engine import absorb_text_stream
from parser import parse_reminder, parse_task
from gpt_fallback import fallback_to_gpt
from gpt_tracker import get_usage_summary
from daily_summary import show_daily_summary

dev_mode = False

print("👋 I’m JOJO. Talk to me or type 'exit' to stop.")
show_daily_summary()

strip_prefixes = ["jojo", "hey jojo", "yo jojo", "jojo,", "hey jojo,"]

def normalize_input(text):
    text = text.lower().strip()
    text = text.replace("tommorow", "tomorrow").replace("tmrw", "tomorrow")
    text = text.replace("todayy", "today")
    return text

while True:
    user_input = normalize_input(input("You: "))

    if user_input in ["exit", "quit"]:
        print("JOJO: Goodbye! 👋")
        break

    for prefix in strip_prefixes:
        if user_input.startswith(prefix):
            user_input = user_input.replace(prefix, "").strip()
            break

    # === Absorb Mode ===
    if user_input in ["absorb mode", "enter absorb mode"]:
        print("🧠 Absorb Mode Activated. Feed me anything you want me to learn. Type 'exit absorb' to stop.")
        absorb_buffer = []
        while True:
            line = input("📝 ").strip()
            if line.lower() in ["exit absorb", "done", "stop"]:
                raw_input = " ".join(absorb_buffer)
                print("🧠 Absorbing what you shared...")
                saved_count, memories = absorb_text_stream(raw_input)
                print(f"JOJO: Learned {saved_count} things:")
                for mem in memories:
                    print(f" - [{mem['type']}/{mem['category']}] {mem['value']}")
                break
            absorb_buffer.append(line)
        continue

    # === GPT Usage Report ===
    if re.search(r"(gpt usage|api usage|how much.*spent|token usage|cost report|usage report)", user_input):
        print(get_usage_summary())
        continue

    # === Reminder Handling ===
    parsed = parse_reminder(user_input)
    if parsed:
        if parsed.get("time"):
            add_reminder(parsed["task"], parsed["time"])
            print(f"JOJO: Got it. Reminder set to '{parsed['task']}' at '{parsed['time']}'.")
        elif parsed.get("ambiguous_time"):
            print(f"JOJO: Did you mean {parsed['ambiguous_time']}am or {parsed['ambiguous_time']}pm?")
            clarification = input("You: ").strip().lower()
            if clarification in ["am", "a.m.", "in the morning"]:
                final_time = f"{parsed['ambiguous_time']}am"
            elif clarification in ["pm", "p.m.", "in the evening", "night"]:
                final_time = f"{parsed['ambiguous_time']}pm"
            else:
                print("JOJO: I still couldn't tell. Try again with 'am' or 'pm'.")
                continue
            updated_input = f"remind me to {parsed['task']} at {final_time}"
            final_parsed = parse_reminder(updated_input)
            if final_parsed and final_parsed.get("time"):
                add_reminder(final_parsed["task"], final_parsed["time"])
                print(f"JOJO: Reminder saved: '{final_parsed['task']}' at '{final_parsed['time']}'")
            else:
                print("JOJO: Sorry, I still couldn't parse that.")
        else:
            print("JOJO: Hmm, I couldn't understand the reminder time.")
        continue

    # === Task Parsing ===
    if user_input.startswith(("add a task", "task:")):
        parsed = parse_task(user_input)
        if parsed["description"]:
            add_task(parsed["description"], parsed["time"])
            time_info = f" (due {parsed['time']})" if parsed["time"] else ""
            print(f"JOJO: Got it. Task added: '{parsed['description']}'{time_info}.")
        else:
            print("JOJO: Hmm, I couldn’t understand the task.")
        continue

    # === Notes ===
    note_match = re.match(r"(add note\s*:|add note\s+|note\s*:|note\s+|take a note\s*:|take a note\s+|add a note saying\s*:|add a note saying\s+)(.+)", user_input)
    if note_match:
        content = note_match.group(2).strip()
        add_note(content)
        print(f"JOJO: Note taken: '{content}'.")
        continue

    if re.search(r"(find|search|look up|any.*note[s]?|note[s]?.*about|do i have.*note[s]?|anything.*note[s]?|other note[s]?|any other note[s]?|anyother note[s]?)", user_input.replace("?", "")):
        search_notes(user_input)
        continue

    if re.search(r"(show|list|display).*(my )?note[s]?", user_input):
        list_notes()
        continue

    if re.search(r"(show|list|display).*(my )?task[s]?", user_input):
        list_tasks()
        continue

    if re.search(r"(show|list|display|what).*(my )?reminder[s]?", user_input):
        list_reminders()
        continue

    if re.search(r"(remind|call|appointment|alarm|meeting|at|today|tomorrow|for today|for tomorrow|do.*anything|for the day|need.*do|\d{1,2}(am|pm)?)", user_input):
        search_reminders(user_input)
        continue

    if re.search(r"(task|todo|assignment|homework|email|submit|at|today|tomorrow|for today|for tomorrow|do.*anything|need.*do|for the day|\d{1,2}(am|pm)?)", user_input):
        search_tasks(user_input)
        continue

    if "what did you answer" in user_input or "show my ai history" in user_input or "show gpt log" in user_input:
        show_gpt_log(dev_mode)
        continue

    # === Memory Recall ===
    found = False
    mem = memory.list_all_memory()
    user_words = set(user_input.replace("?", "").split())

    for key, value in mem.items():
        readable_key = key.replace("_", " ")
        if (
            readable_key in user_input
            or any(word in user_words for word in readable_key.split())
            or (key == "loves" and any(q in user_input for q in ["what do i love", "what else", "do i love"]))
        ):
            if key == "loves" and isinstance(value, list):
                joined = ", ".join(value[:-1]) + " and " + value[-1] if len(value) > 1 else value[0]
                print(f"JOJO: You love {joined}.")
            elif key == "loves":
                print(f"JOJO: You love {value}.")
            else:
                if isinstance(value, list):
                    joined = ", ".join(value[:-1]) + " and " + value[-1] if len(value) > 1 else value[0]
                    print(f"JOJO: Your {readable_key} is {joined}.")
                else:
                    print(f"JOJO: Your {readable_key} is {value}.")
            found = True
            break

    if found:
        continue

    # === GPT Fallback ===
    print("JOJO:", fallback_to_gpt(user_input))
