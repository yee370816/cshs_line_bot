import json
import importlib
import time
import os

def read_config(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as fs:
            return json.load(fs) # channelSecret & accessToken
    except FileNotFoundError:
        print('failed to load credential')
        quit("the LINE bot API is terminated")

def read_students(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as fs:
            return json.load(fs) # channelSecret & accessToken
    except FileNotFoundError:
        print('failed to load student data')
        quit("the LINE bot API is terminated")

def get_student_modules(student_data: dict, parent_module = "student_modules") -> dict:
    student_modules = {}
    for line_id, student_data in student_data.items():
        module_path = parent_module  + "." + student_data["student_no"]
        if importlib.util.find_spec(module_path):
            student_module = importlib.import_module(module_path)
            student_modules[line_id] = student_module
        else:
            debug = True
            module_path = "./" + parent_module  + "/" + student_data["student_no"] + ".py"
            with open(module_path, 'w', encoding='utf-8') as fs:
                fs.write("def process(message: str) -> None:\n")
                fs.write("    pass\n")
                fs.close()

    return student_modules
