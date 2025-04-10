import json
from datetime import datetime
from pathlib import Path

MEMORY_FILE = Path("data/jojo_memory.json")
LOCK_FILE = Path("data/jojo_memory_locks.json")


def _load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {}


def _save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def add_memory(key, value):
    key = key.strip().lower().replace(" ", "_")
    memory = _load_json(MEMORY_FILE)
    locks = _load_json(LOCK_FILE)

    if locks.get(key):
        return f"🔒 '{key}' is locked and can't be changed."

    if key in memory:
        existing = memory[key]
        if isinstance(existing, list):
            if value not in existing:
                memory[key].append(value)
        elif existing != value:
            memory[key] = [existing, value]
    else:
        memory[key] = value

    _save_json(MEMORY_FILE, memory)
    return f"✅ Remembered: {key.replace('_', ' ')} = {value}"


def list_all_memory():
    return _load_json(MEMORY_FILE)


def delete_memory(key):
    key = key.strip().lower().replace(" ", "_")
    memory = _load_json(MEMORY_FILE)
    if key in memory:
        del memory[key]
        _save_json(MEMORY_FILE, memory)
        return f"🗑️ Forgot {key.replace('_', ' ')}"
    return f"❌ I don’t remember anything about {key.replace('_', ' ')}."


def update_memory(key, value):
    key = key.strip().lower().replace(" ", "_")
    memory = _load_json(MEMORY_FILE)
    memory[key] = value
    _save_json(MEMORY_FILE, memory)
    return f"✏️ Updated memory: {key.replace('_', ' ')} = {value}"


def lock_memory(key):
    key = key.strip().lower().replace(" ", "_")
    locks = _load_json(LOCK_FILE)
    locks[key] = True
    _save_json(LOCK_FILE, locks)
    return f"🔒 Locked memory: {key.replace('_', ' ')}"


def unlock_memory(key):
    key = key.strip().lower().replace(" ", "_")
    locks = _load_json(LOCK_FILE)
    if key in locks:
        del locks[key]
        _save_json(LOCK_FILE, locks)
        return f"🔓 Unlocked memory: {key.replace('_', ' ')}"
    return f"🔓 '{key}' wasn’t locked."


def clear_all_memory():
    _save_json(MEMORY_FILE, {})
    _save_json(LOCK_FILE, {})
    return "🧹 Memory completely wiped."


def save_bulk_memory(memory_dict: dict):
    memory = _load_json(MEMORY_FILE)
    locks = _load_json(LOCK_FILE)
    added = 0
    for k, v in memory_dict.items():
        if locks.get(k):
            continue
        memory[k] = v
        added += 1
    _save_json(MEMORY_FILE, memory)
    return f"🧠 Added {added} new memories."
