import sys
import os
import re
from datetime import datetime
from fuzzywuzzy import fuzz

# Add /src to system path
sys.path.append(os.path.abspath("src"))

import jojo_memory as memory
from command_handlers.reminder import add_reminder, list_reminders, search_reminders
from command_handlers.task import add_task, list_tasks, search_tasks
from command_handlers.note import add_note, list_notes, search_notes
from command_handlers.gpt_log import show_gpt_log
from absorb_engine import absorb_text_stream, absorb_from_file
from parser import parse_reminder, parse_task
from gpt_fallback import fallback_to_gpt
from gpt_tracker import get_usage_summary
from daily_summary import show_daily_summary

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

    # === Absorb from File ===
    if user_input.startswith("absorb file"):
        filepath = user_input.replace("absorb file", "").strip()
        result = absorb_from_file(filepath)
        print("JOJO:", result)
        continue

    # === GPT Usage Report ===
    if re.search(r"(gpt usage|api usage|how much.*spent|token usage|cost report|usage report)", user_input):
        print(get_usage_summary())
        continue

    # === Fallback ===
    print("JOJO:", fallback_to_gpt(user_input))
