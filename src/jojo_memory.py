import json
import os

MEMORY_FILE = os.path.join("data", "jojo_memory.json")
LOCK_FILE = os.path.join("data", "jojo_memory_locks.json")

# Create memory file if it doesn't exist
for file in [MEMORY_FILE, LOCK_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def load_locks():
    with open(LOCK_FILE, "r") as f:
        return json.load(f)

def save_locks(locks):
    with open(LOCK_FILE, "w") as f:
        json.dump(locks, f, indent=4)

def add_memory(key, value):
    memory = load_memory()
    locks = load_locks()
    if locks.get(key, False):
        return f"Sorry, '{key}' is locked and cannot be changed."

    if key in memory:
        existing = memory[key]
        if isinstance(existing, list):
            if value not in existing:
                existing.append(value)
        else:
            if existing != value:
                memory[key] = [existing, value]
    else:
        memory[key] = value

    save_memory(memory)
    return f"Saved '{key.replace('_',' ')}' as '{value}'."

def get_memory(key):
    return load_memory().get(key, None)

def delete_memory(key):
    memory = load_memory()
    locks = load_locks()
    if locks.get(key, False):
        return f"'{key}' is locked and cannot be deleted."

    if key in memory:
        del memory[key]
        save_memory(memory)
        return f"Forgot '{key.replace('_',' ')}'."
    return f"I don’t remember '{key.replace('_',' ')}'."

def update_memory(key, value):
    memory = load_memory()
    locks = load_locks()
    if locks.get(key, False):
        return f"'{key}' is locked and cannot be updated."

    memory[key] = value
    save_memory(memory)
    return f"Updated '{key.replace('_',' ')}' to '{value}'."

def lock_memory(key):
    locks = load_locks()
    locks[key] = True
    save_locks(locks)
    return f"Locked '{key.replace('_',' ')}'."

def unlock_memory(key):
    locks = load_locks()
    if key in locks:
        del locks[key]
        save_locks(locks)
        return f"Unlocked '{key.replace('_',' ')}'."
    return f"'{key.replace('_',' ')}' wasn’t locked."

def list_all_memory():
    return load_memory()
