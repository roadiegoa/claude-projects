import os

from anthropic import Anthropic

auth_kwargs = (
    {"api_key": os.environ["ANTHROPIC_API_KEY"]}
    if os.environ.get("ANTHROPIC_API_KEY")
    else {"auth_token": os.environ.get("ANTHROPIC_AUTH_TOKEN")}
)
client = Anthropic(base_url=os.environ.get("ANTHROPIC_BASE_URL"), **auth_kwargs)


def add_user_message(messages, content):
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages, content):
    messages.append({"role": "assistant", "content": content})


def chat_with_claude(messages):
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=messages,
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
