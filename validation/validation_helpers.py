import ast
import json
import re


def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0
        

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0
    

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0


def validate_lisp(text):
    """Checks that AutoLISP source has balanced parens/strings and defines a command.

    There's no AutoLISP interpreter available outside AutoCAD, so this is a
    structural syntax check rather than a semantic one: unbalanced parens or
    an unterminated string means the script can't even be read by AutoCAD,
    and a missing (defun c: ...) means it doesn't define a runnable command.
    """
    text = text.strip()
    if not text:
        return 0

    depth = 0
    in_string = False
    i = 0
    while i < len(text):
        char = text[i]
        if in_string:
            if char == "\\":
                i += 1  # skip escaped character
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == ";":
            newline = text.find("\n", i)
            if newline == -1:
                break
            i = newline
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                return 0
        i += 1

    if depth != 0 or in_string:
        return 0
    return 10 if re.search(r"\(defun\s+c:", text, re.IGNORECASE) else 5


def grade_syntax(response, test_case):
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    elif format == "python":
        return validate_python(response)
    elif format == "lsp":
        return validate_lisp(response)
    else:
        return validate_regex(response)