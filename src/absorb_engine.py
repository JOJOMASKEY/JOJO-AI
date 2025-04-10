import os
import json
from pathlib import Path
from datetime import datetime

import fitz  # PyMuPDF for PDF
from gpt_fallback import gpt_complete
from jojo_memory import add_memory

ABSORB_LOG_PATH = Path("data/absorb_log.json")
ABSORB_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def read_file_content(filepath):
    ext = filepath.suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext in [".txt", ".md"]:
        return filepath.read_text(encoding="utf-8")
    else:
        return None

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def absorb_text_stream(text):
    prompt = f"""Extract knowledge and preferences from the following notes. Classify each as either:
- personal/preference
- personal/belief
- personal/interest
- personal/identity
- world/fact
- world/concept

Respond in JSON list format like:
[
  {{"type": "personal", "category": "preference", "value": "likes hiking at sunrise"}},
  ...
]

TEXT:
{text}
"""
    response = gpt_complete(prompt)
    try:
        parsed = json.loads(response)
        count = 0
        for item in parsed:
            if item.get("value"):
                key = f"{item['type']}_{item['category']}"
                value = item["value"]
                add_memory(key, value)
                count += 1
        log_absorb_event("text", count, text)
        return count, parsed
    except Exception as e:
        print("⚠️ Failed to parse absorb response:", e)
        return 0, []

def absorb_from_file(file_path_str):
    filepath = Path(file_path_str)
    if not filepath.exists():
        return "❌ File not found."

    content = read_file_content(filepath)
    if not content:
        return "⚠️ Unsupported or unreadable file format."

    count, parsed = absorb_text_stream(content)
    summary = f"🧠 Learned {count} things from {filepath.name}"
    return summary

def log_absorb_event(source_type, count, raw_text):
    log_entry = {
        "source": source_type,
        "timestamp": datetime.now().isoformat(),
        "items_learned": count,
        "preview": raw_text[:200]
    }
    try:
        logs = []
        if ABSORB_LOG_PATH.exists():
            with open(ABSORB_LOG_PATH, "r") as f:
                logs = json.load(f)
        logs.append(log_entry)
        with open(ABSORB_LOG_PATH, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print("⚠️ Could not log absorb event:", e)
