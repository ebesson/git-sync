import json
import os


def read_projects_from_json(projects_file):
    file_handler = os.path.join('.', projects_file)
    try:
        with open(file_handler) as json_file:
            projects = json.load(json_file)
    except Exception as e:
        raise Exception("Invalid json file...")
    return projects