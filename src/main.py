import sys
import os
import re

# Add /src to system path
sys.path.append(os.path.abspath("src"))

import jojo_memory as memory

print("👋 I’m JOJO. Talk to me or type 'exit' to stop.")

strip_prefixes = ["jojo", "hey jojo", "yo jojo", "jojo,", "hey jojo,"]

while True:
    user_input = input("You: ").strip().lower()

    if user_input in ["exit", "quit"]:
        print("JOJO: Goodbye! 👋")
        break

    # Remove trigger words like "jojo," from beginning
    for prefix in strip_prefixes:
        if user_input.startswith(prefix):
            user_input = user_input.replace(prefix, "").strip()
            break

    # === SUMMARIZE MEMORY ===
    if "summarize" in user_input or "what do you know" in user_input:
        mem = memory.list_all_memory()
        if mem:
            print("JOJO: Here's what I know about you:")
            for key, value in mem.items():
                if isinstance(value, list):
                    v = ", ".join(value[:-1]) + " and " + value[-1] if len(value) > 1 else value[0]
                else:
                    v = value
                print(f" - Your {key.replace('_', ' ')} is {v}")
        else:
            print("JOJO: I don’t remember anything yet.")
        continue

    # === FORGET MEMORY ===
    forget_match = re.match(r"forget my (.+)", user_input)
    if forget_match:
        key = forget_match.group(1).strip().replace(" ", "_")
        print("JOJO:", memory.delete_memory(key))
        continue

    # === UPDATE MEMORY ===
    update_match = re.match(r"change my (.+?) to (.+)", user_input)
    if update_match:
        key = update_match.group(1).strip().replace(" ", "_")
        value = update_match.group(2).strip()
        print("JOJO:", memory.update_memory(key, value))
        continue

    # === LOCK MEMORY ===
    lock_match = re.match(r"lock my (.+)", user_input)
    if lock_match:
        key = lock_match.group(1).strip().replace(" ", "_")
        print("JOJO:", memory.lock_memory(key))
        continue

    # === UNLOCK MEMORY ===
    unlock_match = re.match(r"unlock my (.+)", user_input)
    if unlock_match:
        key = unlock_match.group(1).strip().replace(" ", "_")
        print("JOJO:", memory.unlock_memory(key))
        continue

    # === LEARNING ===
    learned = False
    learn_patterns = [
        (r"my (.+?) is (.+)", lambda m: (m.group(1), m.group(2))),
        (r"i live in (.+)", lambda m: ("location", m.group(1))),
        (r"i was born in (.+)", lambda m: ("birth_place", m.group(1))),
        (r"call me (.+)", lambda m: ("preferred_name", m.group(1))),
        (r"i(?: really| truly| also| fucking| absolutely| always)? love (.+)", lambda m: ("loves", m.group(1))),
        (r"my birthday is (.+)", lambda m: ("birthday", m.group(1))),
        (r"my village is (.+)", lambda m: ("village", m.group(1)))
    ]

    segments = re.split(r"\band\b", user_input)
    for segment in segments:
        for pattern, extractor in learn_patterns:
            match = re.match(pattern, segment.strip())
            if match:
                key, value = extractor(match)
                key = key.strip().replace(" ", "_")
                value = value.strip()
                print("JOJO:", memory.add_memory(key, value))
                learned = True
                break
        if learned:
            continue

    if learned:
        continue

    # === MEMORY RETRIEVAL ===
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

    if not found:
        print("JOJO: I don’t remember that yet. Try saying something like 'I love pizza' or 'Change my name to Neo.'")
