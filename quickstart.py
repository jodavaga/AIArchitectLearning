import anthropic
from  dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()
model = "claude-sonnet-4-6"

message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "What is quantum computing?. describe in one sentence"
        }
    ]
)

print(message.content)