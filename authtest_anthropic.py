import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# IMPORTANT: For Anthropic SDK, your Base URL should NOT include '/v1' or '/messages'
# because the SDK adds it for you.
# Example: Use "https://proxy.company.com/v1/anthropic" 
# NOT "https://proxy.company.com/v1/anthropic/v1/messages"

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    base_url=os.environ.get("ANTHROPIC_BASE_URL") 
)

message = client.messages.create(
    model="anthropic/claude-opus-4-6", # Use the model name provided by your company
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)