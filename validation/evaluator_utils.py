import os
import json

from client.claude_client import add_assistant_message, add_user_message, chat
from validation.data import dataset



def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""

    prompt = f"""
        Solve the following task:

        {test_case["task"]}
    """

    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output


def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    
    output = run_prompt(test_case)

   # TODO Grading
    score = 10

    return {
        "output": output,
        "test_case": test_case,
        "score": score
    } 

def run_evaluator(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    
    results = []
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    
    return results



print( json.dumps(run_evaluator(dataset), indent=2) )