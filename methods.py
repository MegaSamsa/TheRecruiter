from init import json

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def sex_to_str(sex: bool):
    return 'male' if sex else 'female'

def format_few_worded_text(text: str):
    if "_" in text:
        return text.replace("_", " ")
    else:
        return text
