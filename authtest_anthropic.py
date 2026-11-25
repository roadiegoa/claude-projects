import os

from anthropic import Anthropic

auth_kwargs = (
    {"api_key": os.environ["ANTHROPIC_API_KEY"]}
    if os.environ.get("ANTHROPIC_API_KEY")
    else {"auth_token": os.environ.get("ANTHROPIC_AUTH_TOKEN")}
)
client = Anthropic(base_url=os.environ.get("ANTHROPIC_BASE_URL"), **auth_kwargs)

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}],
)

print(message.content[0].text)
