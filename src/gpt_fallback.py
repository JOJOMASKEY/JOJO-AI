import os
import openai
import json
from datetime import datetime
from pathlib import Path
from gpt_tracker import log_gpt_call
from jojo_memory import list_all_memory

# Load from .env or environment
openai.api_key = os.getenv("OPENAI_API_KEY")

DEV_MODE = False
DEFAULT_MODEL = "gpt-3.5-turbo"
FALLBACK_LOG = Path("data/gpt_fallback_log.json")
FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)

def gpt_complete(prompt, model=None):
    model = model or decide_model(prompt)
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        reply = response['choices'][0]['message']['content'].strip()
        log_gpt_call(model)
        log_fallback_event(prompt, reply, model)
        return reply
    except Exception as e:
        return f"⚠️ GPT Error: {e}"

def fallback_to_gpt(query):
    context = get_context_injection()
    model = decide_model(query)
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content'].strip()
        log_gpt_call(model)
        log_fallback_event(query, reply, model)
        if DEV_MODE:
            return f"🧠 [via {model}]: {reply}"
        return reply
    except Exception as e:
        return f"⚠️ GPT Error: {e}"

def decide_model(text):
    keywords = ["complex", "deep", "analyze", "explain", "research", "advanced", "smart", "detailed"]
    if any(k in text.lower() for k in keywords):
        return "gpt-4"
    return DEFAULT_MODEL

def get_context_injection():
    mem = list_all_memory()
    lines = [f"{k.replace('_', ' ')}: {v}" for k, v in mem.items()]
    context = "You are JOJO, a personal AI assistant built by Nirdesh. Here's what you know:\n" + "\n".join(lines)
    return context

def log_fallback_event(prompt, reply, model):
    event = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "prompt": prompt,
        "reply": reply
    }
    log = []
    if FALLBACK_LOG.exists():
        with open(FALLBACK_LOG, "r") as f:
            log = json.load(f)
    log.append(event)
    with open(FALLBACK_LOG, "w") as f:
        json.dump(log, f, indent=2)
