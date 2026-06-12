from client.claude_client import add_user_message, add_assistant_message, chat

MODEL = "claude-sonnet-4-6"
messages = []
system_prompt = """
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    Explain briefly each topic.
"""

while True:
    user_input = input("> ")
    print("Received user input. Thinking...")

    add_user_message(messages, user_input)
    answer = chat(messages, system=system_prompt, model=MODEL)
    add_assistant_message(messages, answer)

    print("---")
    print(answer)
    print("---")
