# data/loader.py
import json

def load_task_data(file_path):
    with open(file_path, "r") as file:
        task_data = json.load(file)
    return task_data

def save_task_data(file_path, task_data):
    with open(file_path, "w") as file:
        json.dump(task_data, file, indent=4)