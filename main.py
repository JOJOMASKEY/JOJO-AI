import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is loaded correctly
if not openai.api_key:
    raise ValueError("API key is not set. Please check your .env file.")

def select_model_based_on_task(question):
    """
    Automatically choose the model based on the task type.
    """
    # Define rules to choose the model based on the query

    # 1. Simple tasks - Use GPT-3.5
    if len(question.split()) < 10:  # Short questions or factual queries
        return "gpt-3.5-turbo"

    # 2. Creative tasks (writing, brainstorming) - Use GPT-4
    elif "write" in question.lower() or "story" in question.lower():
        return "gpt-4"  # Use GPT-4 for creative tasks like writing or brainstorming

    # 3. Problem-solving tasks (decision making, planning) - Use GPT-4
    elif "plan" in question.lower() or "decide" in question.lower():
        return "gpt-4"  # Use GPT-4 for complex reasoning tasks

    # 4. General or emotional support - Use GPT-3.5
    elif "help" in question.lower() or "feeling" in question.lower():
        return "gpt-3.5-turbo"  # Use GPT-3.5 for general support unless it's deeply emotional

    # Default: GPT-3.5
    else:
        return "gpt-3.5-turbo"

def ask_jojo(question):
    try:
        # Automatically choose the model based on the task type
        model_choice = select_model_based_on_task(question)

        # Make the API call to OpenAI, set a limit on tokens used for responses
        response = openai.ChatCompletion.create(
            model=model_choice,  # Dynamically chosen model
            messages=[{"role": "user", "content": question}],  # Correct format for chat models
            max_tokens=50,  # Limit the response to 50 tokens
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()  # Get the response from OpenAI
    except Exception as e:
        return f"Error: {str(e)}"

# Test the chatbot by asking a question
print("Welcome to JOJO! Ask your question below:")

user_input = input("Ask JOJO a question: ")
response = ask_jojo(user_input)
print(f"JOJO's response: {response}")
