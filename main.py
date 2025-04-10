import sys
import os
import re
import json
from datetime import datetime

# Extend system path to include src folder
sys.path.append(os.path.abspath("src"))

from command_handlers.reminder import add_reminder, list_reminders, search_reminders
from command_handlers.task import add_task, list_tasks, search_tasks
from command_handlers.note import add_note, list_notes, search_notes
from jojo_memory import add_memory, list_all_memory, update_memory, delete_memory, lock_memory, unlock_memory
from gpt_tracker import get_gpt_usage_summary
from absorb_engine import absorb_text_stream, absorb_from_file
from smart_recall import smart_recall_handler
from power_mode import get_power_mode

print("👋 I’m JOJO. Talk to me or type 'exit' to stop.\n")

# Display summary if memory exists
mem = list_all_memory()
if mem:
    print("📆 Here's what's on your schedule today:\n")
    today = datetime.now().date().isoformat()
    search_reminders("today")

strip_prefixes = ["jojo", "hey jojo", "yo jojo", "jojo,", "hey jojo,"]

def normalize_input(text):
    for prefix in strip_prefixes:
        if text.startswith(prefix):
            text = text.replace(prefix, "").strip()
    return text.strip().lower()

absorb_mode = False
absorb_lines = []

while True:
    try:
        user_input = input("You: ").strip()
    except KeyboardInterrupt:
        print("\nJOJO: 👋 Goodbye!")
        break

    if user_input.lower() in ["exit", "quit"]:
        print("JOJO: 👋 Goodbye!")
        break

    user_input = normalize_input(user_input)

    if absorb_mode:
        if user_input in ["exit absorb", "stop absorb", "done"]:
            absorb_mode = False
            print("🧠 Absorbing what you shared...")
            learned = absorb_text_stream("\n".join(absorb_lines))
            absorb_lines = []
            if learned:
                print(f"JOJO: 🧠 Learned {len(learned)} things:")
                for line in learned:
                    print(f" - {line}")
            else:
                print("JOJO: 🧠 I didn’t learn anything from that.")
            continue
        else:
            absorb_lines.append(user_input)
            continue

    if user_input in ["absorb mode", "start absorb"]:
        absorb_mode = True
        absorb_lines = []
        print("🧠 Absorb Mode Activated. Feed me anything you want me to learn. Type 'exit absorb' to stop.")
        continue

    if user_input.startswith("absorb file"):
        file_path = user_input.replace("absorb file", "").strip()
        if os.path.exists(file_path):
            learned = absorb_from_file(file_path)
            if learned:
                print(f"JOJO: 🧠 Learned {len(learned)} things from {os.path.basename(file_path)}")
                for line in learned:
                    print(f" - {line}")
            else:
                print(f"JOJO: 🧠 Learned 0 things from {os.path.basename(file_path)}")
        else:
            print("JOJO: ❌ File not found.")
        continue

    if user_input == "how much have i spent?":
        print("📊 GPT Usage Summary:\n")
        print(get_gpt_usage_summary())
        continue

    if "what do you know about me" in user_input or user_input == "who am i":
        memory = list_all_memory()
        if memory:
            print("JOJO: Based on the information provided to me, I know the following about you:\n")
            for k, v in memory.items():
                print(f"- {k.replace('_', ' ').capitalize()}: {v}")
        else:
            print("JOJO: I don’t remember anything about you yet.")
        continue

    # === COMMAND HANDLERS ===
    if re.match(r"remind me to .+ at .+", user_input):
        match = re.match(r"remind me to (.+?) at (.+)", user_input)
        add_reminder(match.group(1), match.group(2))
        continue

    if re.match(r"add a task to .+", user_input):
        match = re.match(r"add a task to (.+)", user_input)
        add_task(match.group(1))
        continue

    if re.match(r"(note|add note|take note|remember this):?", user_input):
        content = user_input.split(":", 1)[-1].strip()
        add_note(content)
        print(f"JOJO: Note taken: '{content}'.")
        continue

    if re.search(r"(show|list|display).*(reminders)", user_input):
        list_reminders()
        continue

    if re.search(r"(show|list|display).*(tasks)", user_input):
        list_tasks()
        continue

    if re.search(r"(show|list|display).*(notes)", user_input):
        list_notes()
        continue

    if re.match(r"(find|any|search|what).*reminder", user_input):
        search_reminders(user_input)
        continue

    if re.match(r"(find|any|search|what).*task", user_input):
        search_tasks(user_input)
        continue

    if re.match(r"(find|any|search|what).*note", user_input):
        search_notes(user_input)
        continue

    # === SMART RECALL CATCH-ALL ===
    smart_response = smart_recall_handler(user_input)
    if smart_response:
        print(f"JOJO: {smart_response}")
        continue

    print("JOJO: I didn’t understand that. Try asking something else.")

