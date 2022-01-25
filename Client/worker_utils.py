"""
Module contains helper functions for the worker module.
"""
import os
import json
import shutil
import base64

import dill

from data_models import ReceivedTask
import consts
from utils import create_path_string


# TODO: maybe change results to own object
def results_to_file(results: dict):
    """
    Writes the results of a task to the results file.

    Args:
        results (dict): the results of the task.

    """
    results_file = create_path_string(consts.TASKS_DIRECTORY,
                                      consts.RESULTS_FILE + consts.JSON_EXTENSION,
                                      from_current_directory=False)

    with open(results_file, 'w') as file:
        json.dump(results, file)


def zip_additional_results() -> str:
    """
    Zips the additional results of a task.

    Returns:
        str: the path to the additional results zip file.

    """
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


def get_zip_additional_results() -> str:
    """
    Loads the finished task's additional results from its file and returns it.

    Returns:
        bytes: the additional results of a finished task.

    """
    zipped_results_path = zip_additional_results()

    with open(zipped_results_path, 'rb') as file:
        zipped_results = file.read()
    zipped_results = base64.b64encode(zipped_results).decode('utf-8')
    return zipped_results


def get_results() -> dict:
    """
    Loads the finished task's results from its file and returns it.

    Returns:
        dict: the results of a finished task.

    """
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
    Turns the decoded iterator received from task to an object.

    Args:
        task (ReceivedTask): the task.

    Returns:
        the iterator as an object.

    """
    iterator = task.base64_serialized_iterable
    iterator = base64.b64decode(iterator)
    iterator = dill.loads(iterator)
    return iterator


def has_additional_results() -> bool:
    """
    Checks whether the finished task has additional results.

    Returns:
        bool: whether or not the finished task has additional results.

    """
    additional_results_path = create_path_string(consts.TASKS_DIRECTORY,
                                                 consts.ADDITIONAL_RESULTS_DIRECTORY)
    return bool(os.listdir(additional_results_path))


def init_task_result_storage():
    """
    Initializes the storage for a task's results.

    """
    task_path = create_path_string(consts.TASKS_DIRECTORY)
    additional_results_path = create_path_string(task_path, consts.ADDITIONAL_RESULTS_DIRECTORY,
                                                 from_current_directory=False)
    os.makedirs(additional_results_path, exist_ok=True, mode=0o777)
    results_file = create_path_string(task_path, consts.RESULTS_FILE + consts.JSON_EXTENSION,
                                      from_current_directory=False)
    with open(results_file, 'w') as file:
        os.chmod(results_file, mode=0o777)
        json.dump({}, file)


def clean_results_directory():
    """
    Deletes the task's results storage.

    """
    task_path = create_path_string(consts.TASKS_DIRECTORY)
    shutil.rmtree(task_path)
