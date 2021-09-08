"""
Module used to handle the tasks.
"""

import json
import shutil
import base64

from handle_requests import request_get_new_task
from data_models import Task
import consts
from utils import create_path_string


def has_stop_function(cls):
    for attribute in dir(cls):
        if callable(attribute) and not attribute.startswith("__"):
            if attribute == consts.STOP_FUNCTION_NAME:
                return True
    return False


def add_result(iteration, result):
    results_file = create_path_string(consts.TASKS_DIRECTORY,
                                      consts.RESULTS_FILE + consts.JSON_EXTENSION,
                                      from_current_directory=False)

    with open(results_file, 'r+') as file:
        data = json.load(file)
        data[iteration] = result
        json.dump(data, file)


def zip_additional_results():
    task_path = create_path_string(consts.TASKS_DIRECTORY)

    additional_results_zip_path = create_path_string(task_path,
                                                     consts.ADDITIONAL_RESULTS_ZIP_FILE,
                                                     from_current_directory=False)
    additional_results_path = create_path_string(task_path,
                                                 consts.ADDITIONAL_RESULTS_DIRECTORY,
                                                 from_current_directory=False)

    zipped_results_path = shutil.make_archive(additional_results_zip_path, 'zip',
                                              additional_results_path)

    return zipped_results_path


def get_zip_additional_results():

    zipped_results_path = zip_additional_results()

    with open(zipped_results_path, 'rb') as file:
        zipped_results = file.read()
    zipped_results = base64.b64encode(zipped_results).decode('utf-8')
    return zipped_results


def get_results():

    results_path = create_path_string(consts.TASKS_DIRECTORY,
                                      consts.RESULTS_FILE + consts.JSON_EXTENSION)

    with open(results_path, 'r') as file:
        results = json.load(file)

    return results
