import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

def add_user_message(messages, text):
    user_message = { "role": "user", "content": text}
    messages.append(user_message)
    return messages


def add_assistant_message(messages, text):
    assistant_message = { "role": "assistant", "content": text}
    messages.append(assistant_message)
    return messages

def chat(messages, system=None, isActiveSystemPrompt=True):
    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": 0.5
    }

    if system and isActiveSystemPrompt:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text

# Math Teacher by system propmpts
messages = []
system_prompt="""
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    Explain briefly each topic.
"""   

while True:
    # get user input
    user_input = input("> ")
    print("Received user input. Thinking...")

    # Add user input to messages
    add_user_message(messages, user_input)
    # Send to Chat
    answer = chat(messages, system_prompt)

    # Add assistant response to messages
    add_assistant_message(messages, answer)

    print("---")
    print(answer)
    print("---")
    


