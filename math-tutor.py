import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()
model = "claude-sonnet-4-6"

def add_user_message(messages, text):
    user_message = { "role": "user", "content": text}
    messages.append(user_message)
    return messages


def add_assistant_message(messages, text):
    assistant_message = { "role": "assistant", "content": text}
    messages.append(assistant_message)
    return messages


system="""
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    Explain briefly each topic.
"""    

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
        system=system
    )
    return message.content[0].text

# Math Teacher by system propmpts
messages = []


while True:
    # get user input
    user_input = input("> ")
    print("User input >", user_input)

    # Add user input to messages
    add_user_message(messages, user_input)
    # Send to Chat
    answer = chat(messages)

    # Add assistant response to messages
    add_assistant_message(messages, answer)

    print("---")
    print(answer)
    print("---")
    


