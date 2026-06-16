import json
import re
from statistics import mean

from client.claude_client import add_assistant_message, add_user_message, chat
from validation.data import dataset
from validation.validation_helpers import grade_syntax


def grade_by_model(test_case, output):
    eval_prompt = f"""
        You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

        Original Task:
        <task>
        {test_case["task"]}
        </task>

        Solution to Evaluate:
        <solution>
        {output}
        </solution>

        Output Format
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key strengths
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1-10

        Respond with JSON. Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}"""

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])

    # Fix bare backslashes in JSON string values (e.g. \d, \s from code/regex in solutions)
    sanitized = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', eval_text)
    return json.loads(sanitized)


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""

    prompt = f"""
        Solve the following task:

        {test_case["task"]}

    * Respond only with Python, JSON or plain regex code
    * Do not add any comments, commentary or explanation neither before or after code solution
    """

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    output = chat(messages, stop_sequences=["```"])
    return output


def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    
    output = run_prompt(test_case)

    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    syntax_score = grade_syntax(output, test_case)

    score = (syntax_score + model_score) / 2

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning
    } 

def run_evaluator(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    
    results = []
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    # Read it as: "give me result["score"] for each result in the results list."
    print(f"Average score: {average_score:.2f}")
    
    return results
