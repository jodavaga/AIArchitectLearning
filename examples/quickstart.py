from client.claude_client import add_user_message, add_assistant_message, chat

MODEL = "claude-sonnet-4-6"
messages = []

add_user_message(messages, "Define quantum computing in one sentence")
answer = chat(messages, model=MODEL)
print("Assistant:", answer)

add_assistant_message(messages, answer)

add_user_message(messages, "Write another sentence")
final_answer = chat(messages, model=MODEL)
print("Assistant:", final_answer)
