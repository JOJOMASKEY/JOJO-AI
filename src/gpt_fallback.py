from openai import OpenAI
import os
from dotenv import load_dotenv
from gpt_tracker import log_gpt_usage

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fallback_to_gpt(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=400
        )
        reply = response.choices[0].message.content.strip()

        # Estimate token usage
        tokens_in = len(user_input.split())
        tokens_out = len(reply.split())
        log_gpt_usage(model="gpt-3.5-turbo", tokens_in=tokens_in, tokens_out=tokens_out, feature="fallback")

        return reply
    except Exception as e:
        return "Sorry, I had trouble finding an answer."
