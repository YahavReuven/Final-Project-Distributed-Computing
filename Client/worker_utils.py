"""
Module contains helper functions for the worker module.
"""
import os
import json
import shutil
import base64

from handle_requests import request_get_new_task
from data_models import ReceivedTask
import consts
from utils import create_path_string

import dill


def has_stop_function(cls) -> bool:
    """
    Checks if a parallel class has a stop function or not.

    Args:
        cls: the parallel class

    Returns:
        whether or not the parallel class has a stop function.
    """
    for attribute in dir(cls):
        if callable(getattr(cls, attribute)) and attribute == consts.STOP_FUNCTION_NAME:
            return True
    return False


# TODO: maybe change results to own object
def results_to_file(results: dict):
    """
    Writes the results of a task to he results file.
    Args:
        results:

    Returns:

    """
    results_file = create_path_string(consts.TASKS_DIRECTORY,
                                      consts.RESULTS_FILE + consts.JSON_EXTENSION,
                                      from_current_directory=False)

    with open(results_file, 'w') as file:
        json.dump(results, file)


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


# TODO: maybe get only the decoded class
def get_task_cls(task: ReceivedTask):
    """
    Turns the decoded class received from task to a class object.

    Args:
        task (ReceivedTask): the task.

    Returns:
        the class as an object.
    """
    parallel_cls = task.base64_serialized_class
    parallel_cls = base64.b64decode(parallel_cls)
    parallel_cls = dill.loads(parallel_cls)
    return parallel_cls


# TODO: maybe get only the decoded iterable
def get_task_iterable(task: ReceivedTask):
    """
    Turns the decoded iterable received from task to an object.

    Args:
        task (ReceivedTask): the task.

    Returns:
        the iterable as an object.
    """
    iterable = task.base64_serialized_class
    iterable = base64.b64decode(iterable)
    iterable = dill.loads(iterable)
    return iterable


def has_additional_results() -> bool:
    additional_results_path = create_path_string(consts.TASKS_DIRECTORY,
                                                 consts.ADDITIONAL_RESULTS_DIRECTORY)

    return bool(os.listdir(additional_results_path))


def init_task_result_storage():
    task_path = create_path_string(consts.TASKS_DIRECTORY)

    additional_results_path = create_path_string(task_path, consts.ADDITIONAL_RESULTS_DIRECTORY,
                                                 from_current_directory=False)
    os.makedirs(additional_results_path, exist_ok=True)

    results_file = create_path_string(task_path, consts.RESULTS_FILE + consts.JSON_EXTENSION,
                                      from_current_directory=False)
    with open(results_file, 'w') as file:
        json.dump({}, file)