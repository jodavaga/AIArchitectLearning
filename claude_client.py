import anthropic
from dotenv import load_dotenv


load_dotenv()

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

def add_user_message(messages, text):
    user_message = { "role": "user", "content": text}
    messages.append(user_message)
    return messages


def add_assistant_message(messages, text):
    assistant_message = { "role": "assistant", "content": text}
    messages.append(assistant_message)
    return messages

def chat(messages, system=None, temperature=0.6, stop_sequences=[]):
    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }

    if system:
        params["system"] = system

    if stop_sequences: 
        params["stop_sequences"] = stop_sequences


    message = client.messages.create(**params)
    return message.content[0].text

