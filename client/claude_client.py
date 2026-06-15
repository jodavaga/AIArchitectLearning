import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()
DEFAULT_MODEL = "claude-haiku-4-5"


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})
    return messages


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})
    return messages


def chat(messages, system=None, model=DEFAULT_MODEL, temperature=0.6, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    message = client.messages.create(**params)
    return message.content[0].text
