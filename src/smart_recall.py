import json
from pathlib import Path
from fuzzywuzzy import fuzz
from jojo_memory import list_all_memory

# Concept alias mapping
CONCEPT_ALIASES = {
    "birth_place": ["where was i born", "place of birth", "birthplace"],
    "birthday": ["when is my birthday", "birth date", "date of birth"],
    "personal_preference":
    ["what do i like", "do i like", "what are my preferences"],
    "personal_belief": ["what do i believe", "beliefs", "philosophy"],
    "personal_interest":
    ["what are my interests", "what do i enjoy", "hobbies"],
    "mental_health_status": [
        "what is my mental health", "mental health diagnosis",
        "mental health status"
    ],
    "academic_accommodations":
    ["what are my accommodations", "course load", "academic help"],
    "name": ["who am i", "what is my name"],
    "village": ["where is my village", "hometown", "village name"],
    "loves": ["what do i love", "my favorite things"],
    "world_fact": ["tell me a world fact", "fun fact", "about the world"],
    "personal_identity": ["who am i", "my identity", "about me"],
}


def normalize_text(text):
    return text.lower().strip()


def match_alias(query):
    q = normalize_text(query)
    for key, phrases in CONCEPT_ALIASES.items():
        if any(phrase in q for phrase in phrases):
            return key
    return None


def query_memory(query):
    memory = list_all_memory()
    matched_key = match_alias(query)

    if matched_key and matched_key in memory:
        value = memory[matched_key]
        if isinstance(value, list):
            return f"{matched_key}[0]: {value[0]}"
        elif isinstance(value, dict):
            first_key = list(value.keys())[0]
            return f"{matched_key}.{first_key}: {value[first_key]}"
        return f"{matched_key}: {value}"

    # Fallback fuzzy matching
    query_words = set(normalize_text(query).split())
    best_score = 0
    best_key = None

    for key, value in memory.items():
        score = fuzz.partial_ratio(" ".join(query_words), key.lower())
        if score > best_score:
            best_score = score
            best_key = key

    if best_score > 60:
        return f"{best_key}: {memory[best_key]}"
    return "I couldn't find anything relevant."
