import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import jojo_memory
from gpt_tracker import log_gpt_usage

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def extract_memories_from_text(raw_text: str) -> list:
    """Uses GPT to extract structured memories from absorb input."""
    prompt = f"""
You are an intelligent AI assistant that helps categorize and extract important structured insights from human data streams. Your task is to return a JSON list of memory items that are valuable for an AI assistant to remember about its user or the world. Each item should have:

- "type": either "personal", "world", or "self"
- "category": such as "preference", "belief", "fact", "habit", "trigger", "identity", "knowledge"
- "value": the actual insight
- "permanent": true

Only return the list. Here's the raw data:

\"\"\"{raw_text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        reply = response.choices[0].message.content.strip()

        # Estimate token usage
        tokens_in = len(prompt.split())
        tokens_out = len(reply.split())
        log_gpt_usage(model="gpt-4", tokens_in=tokens_in, tokens_out=tokens_out, feature="absorb_mode")

        parsed = json.loads(reply)
        return parsed
    except Exception as e:
        print("❌ Absorb failed:", e)
        return []

def absorb_text_stream(input_text: str):
    memories = extract_memories_from_text(input_text)
    saved = 0
    for mem in memories:
        result = jojo_memory.add_memory(
            key=f"{mem['type']}_{mem['category']}",
            value=mem['value']
        )
        saved += 1
    return saved, memories
