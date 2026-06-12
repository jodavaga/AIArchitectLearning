from claude_client import add_user_message, add_assistant_message, chat
import json

# Dataset generator
def generate_dataset():
    messages = []
    datasetSize = 3
    GENERATE_DATASET_PROMPT = """
        Generate a evaluation dataset for a prompt evaluation. 
        The dataset will be used to evaluate pro that generate Python, JSON, or Regex specifically for AWS-related tasks. 
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

    add_user_message(messages, GENERATE_DATASET_PROMPT)
    answer = chat(messages)
    print("Answer:", answer)

    add_assistant_message(messages, "```json")
    jsonText = chat(messages, stop_sequences=["```"])

    print("--- Generator")
    print(jsonText)
    print("---")

    return json.loads(jsonText)

def write_json_file(text="{'test': 'content'}"):
    with open("dataset.json", "w") as file:
        json.dump(text, file, indent=2)

# Generate Dataset
dataset = generate_dataset()
print("--- Dataset")
print(dataset)
write_json_file(dataset)
print("---")
    


