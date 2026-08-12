import os
import json
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# 1. Try loading from local .env first
load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY")
base_url = os.environ.get("ANTHROPIC_BASE_URL")

# 2. Fallback: If not in .env, look inside the global Claude settings
if not api_key or not base_url:
    global_settings_path = Path.home() / ".claude" / "settings.json"
    
    if global_settings_path.exists():
        try:
            with open(global_settings_path, "r") as f:
                data = json.load(f)
                # Extract from the "env" block in settings.json
                env_block = data.get("env", {})
                
                # Note: Your settings.json uses ANTHROPIC_AUTH_TOKEN, 
                # but the Python SDK expects api_key
                if not api_key:
                    api_key = env_block.get("ANTHROPIC_AUTH_TOKEN")
                if not base_url:
                    base_url = env_block.get("ANTHROPIC_BASE_URL")
        except Exception:
            pass # Handle gracefully if JSON is malformed

# Initialize client with whatever we found
client = Anthropic(
    api_key=api_key,
    base_url=base_url 
)

def add_user_message(messages, content):
    messages.append({"role": "user", "content": content})

def add_assistant_message(messages, content):
    messages.append({"role": "assistant", "content": content})

def chat_with_claude(messages):
    response = client.messages.create(
        model="anthropic/claude-opus-4-6", # Use the model name provided by your company
        max_tokens=1024,
        messages=messages
    )
    return response.content[0].text

# Example conversation

while True:     

    question = input("Enter your question: ")
    
    conversation = []
    add_user_message(conversation, question)
    response = chat_with_claude(conversation)
    print(response)
    add_assistant_message(conversation, response)
    add_user_message(conversation, "Write another sentence.")
    response = chat_with_claude(conversation)
    print(response)
    
    continue_chat = input("Do you want to continue the conversation? (yes/no): ")
    if continue_chat.lower() != "yes":
        break   
