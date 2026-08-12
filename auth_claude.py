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

message = client.messages.create(
    model="anthropic/claude-opus-4-6", # Use the model name provided by your company
    max_tokens=1024,
    messages=[
        {"role": "user", 
         "content": "What is quantum computing? Answer in one sentence."}
    ]
)

print(message.content[0].text)

message = client.messages.create(
    model="anthropic/claude-opus-4-6", # Use the model name provided by your company
    max_tokens=1024,
    messages=[
        {"role": "user", 
         "content": "Write another sentence.",
         }
    ]
)

print(message.content[0].text)