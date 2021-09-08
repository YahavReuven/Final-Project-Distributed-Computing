"""
Module used to handle the client side storage.
"""

import os
import json

import consts
from utils import create_path_string

def init_task_result_storage():
    task_path = create_path_string(consts.TASKS_DIRECTORY)

    os.makedirs(task_path, exist_ok=True)

    additional_results_path = create_path_string(task_path, consts.ADDITIONAL_RESULTS_DIRECTORY,
                                                 from_current_directory=False)
    os.makedirs(additional_results_path, exist_ok=True)

    results_file = create_path_string(task_path, consts.RESULTS_FILE + consts.JSON_EXTENSION,
                                      from_current_directory=False)
    with open(results_file, 'w') as file:
        json.dump({}, file)


def has_additional_results() -> bool:
    additional_results_path = create_path_string(consts.TASKS_DIRECTORY,
                                                 consts.ADDITIONAL_RESULTS_DIRECTORY)

    return bool(os.listdir(additional_results_path))
