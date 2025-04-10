import json
from pathlib import Path
from datetime import datetime

MEMORY_PATH = Path("data/jojo_memory.json")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_memory():
    if MEMORY_PATH.exists():
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(key, value):
    memory = load_memory()
    if key in memory:
        if isinstance(memory[key], list):
            memory[key].append(value)
        elif memory[key] != value:
            memory[key] = [memory[key], value]
    else:
        memory[key] = value
    save_memory(memory)

# === Save Extracted Insights ===

update_memory("personal_identity", {
    "name": "Nirdesh Maskey",
    "dob": "2001-07-08",
    "student_id": "991468856",
    "sevis_id": "N0034103405",
    "university": "University of Wisconsin–Milwaukee"
})

update_memory("mental_health_status", {
    "diagnosis": "Adjustment disorder with mixed anxiety and depression",
    "ptsd_evaluation": True,
    "counselor": "Constance Phillips, MSW, LCSW, CSAC, ICS",
    "clinic": "SHAW Counseling",
    "visit_date": "2025-04-04",
    "treatment_start": "2025-04-08T12:00:00",
    "prognosis": "Good with ongoing treatment"
})

update_memory("academic_accommodations", {
    "recommendation": "Reduced course load",
    "credit_hours": 9,
    "until": "2025-05-18"
})

print("✅ Medical insights saved to memory.")
