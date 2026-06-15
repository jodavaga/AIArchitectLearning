from client.claude_client import add_user_message, add_assistant_message, chat

MODEL = "claude-sonnet-4-6"
messages = []

while True:
    user_input = input("> ")
    print("User input >", user_input)

    add_user_message(messages, user_input)
    answer = chat(messages, model=MODEL)
    add_assistant_message(messages, answer)

    print("---")
    print(answer)
    print("---")
