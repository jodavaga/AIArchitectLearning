import os
import json

from client.claude_client import add_user_message, add_assistant_message, chat

DATA_DIR = "validation/data"

GENERATE_DATASET_PROMPT = """
    Generate a evaluation dataset for a prompt evaluation.
    The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks.
    Generate an array of each representing task that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
        {
            "task": "Description of task"
        },
        ...additional
    ]
    ```

    *   Focus on tasks that can be solved by writing a single Python function, a single JSON object,
    *   Focus on tasks that do not require writing much code

    lets generate 3 objects
"""


def generate_dataset():
    messages = []
    add_user_message(messages, GENERATE_DATASET_PROMPT)
    answer = chat(messages)
    print("Answer:", answer)

    add_assistant_message(messages, "```json")
    json_text = chat(messages, stop_sequences=["```"])

    print("--- Generator")
    print(json_text)
    print("---")

    return json.loads(json_text)


def write_json_file(data, filename="dataset.json"):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


dataset = generate_dataset()
print("--- Dataset")
print(dataset)
write_json_file(dataset)
print("---")
