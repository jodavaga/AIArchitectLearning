import json
import os

with open(os.path.join(os.path.dirname(__file__), "dataset.json")) as f:
    dataset = json.load(f)
