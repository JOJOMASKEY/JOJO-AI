import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from smart_recall import query_memory

print("🧠 Testing Smart Recall...\n")

queries = [
    "Do I like hiking?",
    "What mental health status do I have?",
    "What are my academic accommodations?",
    "What do I believe about creativity?",
    "What are my personal interests?",
    "Where was I born?",
    "Who created you?",
    "What do you know about me?",
]

for q in queries:
    print(f"Q: {q}")
    print("A:", query_memory(q))
    print()
