import json
import importlib

def read_config(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as fs:
            return json.load(fs) # channelSecret & accessToken
    except FileNotFoundError:
        print('failed to load credential')
        quit("the LINE bot API is terminated")

def read_students(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as fs:
            return json.load(fs) # channelSecret & accessToken
    except FileNotFoundError:
        print('failed to load student data')
        quit("the LINE bot API is terminated")

def get_student_modules(student_data: dict, parent_module = "student_modules") -> dict:
    student_modules = {}
    for line_id, student_data in student_data.items():
        module_path = parent_module  + "." + student_data["student_no"]
        student_module = importlib.import_module(module_path)
        student_modules[line_id] = student_module
    return student_modules
