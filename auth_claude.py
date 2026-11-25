import os

from anthropic import Anthropic

auth_kwargs = (
    {"api_key": os.environ["ANTHROPIC_API_KEY"]}
    if os.environ.get("ANTHROPIC_API_KEY")
    else {"auth_token": os.environ.get("ANTHROPIC_AUTH_TOKEN")}
)
client = Anthropic(base_url=os.environ.get("ANTHROPIC_BASE_URL"), **auth_kwargs)


def ask(prompt: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


print(ask("What is quantum computing? Answer in one sentence."))
print(ask("Write another sentence."))
