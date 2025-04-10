import json
from datetime import datetime
from pathlib import Path
import fitz  # PyMuPDF
from gpt_fallback import gpt_complete
from jojo_memory import update_memory

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_text_from_txt(file_path):
    with open(file_path, "r") as f:
        return f.read().strip()

def absorb_text_stream(text):
    prompt = f"""You are JOJO, a helpful assistant learning from a user's text input.

Please extract meaningful information and return it in a structured JSON format like:

{{
  "personal_identity": {{ "name": "...", "dob": "...", "student_id": "...", "sevis_id": "...", "university": "..." }},
  "mental_health_status": {{ "diagnosis": "...", "ptsd_evaluation": true, "counselor": "...", "clinic": "...", "visit_date": "...", "treatment_start": "...", "prognosis": "..." }},
  "academic_accommodations": {{ "recommendation": "...", "credit_hours": 9, "until": "..." }}
}}

Only include fields you find. Do not guess.
Text:
\"\"\"{text}\"\"\"
"""

    response = gpt_complete(prompt)
    try:
        data = json.loads(response)
        for key, val in data.items():
            update_memory(key, val)
        return data
    except Exception as e:
        print("⚠️ Failed to parse absorb response:", e)
        return {}

def absorb_from_file(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        return {"error": "❌ File not found."}

    if file_path.suffix == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_path.suffix == ".txt":
        text = extract_text_from_txt(file_path)
    else:
        return {"error": "❌ Unsupported file type."}

    return absorb_text_stream(text)
