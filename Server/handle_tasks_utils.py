"""
Module contains helper functions for the handle_task module.
"""
import json
import zipfile
import os
import shutil
from datetime import datetime

from database import CustomDecoder
import consts
from data_models import Task, SentTask, Worker, Project
from utils import (validate_base64_and_decode, create_path_string,
                   rmtree_onerror_remove_readonly)


def add_new_task_to_database(project: Project) -> Task:
    """
    Adds an empty task to the project.

    Args:
        project (Project): the project to add the task to.

    Returns:
        Task: the empty task.

    """
    new_task = Task()
    project.tasks.append(new_task)
    return new_task


def create_task_to_send(project_id: str, task_number: int) -> SentTask:
    """
    Creates a new task to send to a worker.

    Args:
        project_id (str): the project id of the project associated with
            the task.
        task_number (int): the task number of the sent task.

    Returns:
        SentTask: a new task.

    """
    project_json_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                           consts.PROJECT_STORAGE_PROJECT,
                                           consts.PROJECT_STORAGE_JSON_PROJECT)
    with open(project_json_path, 'r') as file:
        project_storage = json.load(file, cls=CustomDecoder)

    return SentTask(project_id=project_id, task_number=task_number,
                    task_size=project_storage.task_size,
                    base64_serialized_class=project_storage.base64_serialized_class,
                    base64_serialized_iterable=project_storage.base64_serialized_iterable,
                    modules=project_storage.modules,
                    parallel_func=project_storage.parallel_func,
                    stop_func=project_storage.stop_func,
                    only_if_func=project_storage.only_if_func)


def create_new_worker(device_id: str) -> Worker:
    """
    Creates a new worker.

    Args:
        device_id (str): the device id of the worker.

    Returns:
        Worker: a new worker.

    """
    sent_date = datetime.utcnow()
    new_worker = Worker(worker_id=device_id, sent_date=sent_date)
    return new_worker


def add_worker_to_task(task: Task, device_id: str):
    """
    Adds a new worker to the given task.

    Args:
        task (Task): the task to add the worker to.
        device_id (str): the device id of the worker.

    """
    worker = create_new_worker(device_id)
    task.workers.append(worker)


def store_task_results(project_id: str, task_results: dict, task_number: int):
    """
    Stores a returned task's results.

    Args:
        project_id (str): the project id of the project which the task is associated with.
        task_results (dict): the results of the task.
        task_number (int): the task number of the returned task.

    """
    results_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                      consts.PROJECT_STORAGE_RESULTS, task_number,
                                      consts.RETURNED_TASK_RESULTS_DIRECTORY)
    os.makedirs(results_path, exist_ok=True, mode=0o777)

    result_file = create_path_string(results_path, consts.RESULTS_FILE,
                                     from_current_directory=False)
    with open(result_file, 'w') as file:
        os.chmod(result_file, mode=0o777)
        json.dump(task_results, file)


def store_task_additional_results(project_id: str, base64_zipped_additional_results: str,
                                  task_number: int):
    """
    Unzips a returned task's additional results and stores them in server's storage.

    Args:
        project_id (str): the project id of the project which the task is associated with.
        base64_zipped_additional_results (str): the zipped additional results in base64.
        task_number (int): the task number of the returned task.

    """
    decoded_additional_results = validate_base64_and_decode(base64_zipped_additional_results)
    results_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                      consts.PROJECT_STORAGE_RESULTS, task_number,
                                      consts.RETURNED_TASK_RESULTS_DIRECTORY,
                                      consts.RETURNED_TASK_ADDITIONAL_RESULTS_DIRECTORY)

    os.makedirs(results_path, exist_ok=True, mode=0o777)

    temp_results_file = create_path_string(results_path,
                                           consts.RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE,
                                           from_current_directory=False)
    with open(temp_results_file, 'wb') as file:
        os.chmod(temp_results_file, mode=0o777)
        file.write(decoded_additional_results)

    with zipfile.ZipFile(temp_results_file) as zip_file:
        zip_file.extractall(results_path)

    os.chmod(temp_results_file, mode=0o777)
    os.remove(temp_results_file)


def delete_unnecessary_tasks_storage(project: Project, stop_called_task_number: int):
    """
    Deletes all the tasks' storage in a project, besides the task
        which has the stop_called_task_number task number.

    Note:
        The function is called if a returned task of a project has a stop_called set.

    Args:
        project (Project): the project which is associated with the returned task.
        stop_called_task_number (int): the task number of the task which has the
            stop_called set.

    """
    results_path = create_path_string(consts.PROJECTS_DIRECTORY,
                                      project.project_id,
                                      consts.PROJECT_STORAGE_RESULTS)
    tasks_directories = os.listdir(results_path)

    for task_directory in tasks_directories:
        if task_directory != str(stop_called_task_number):
            task_path = create_path_string(results_path, task_directory,
                                           from_current_directory=False)
            shutil.rmtree(task_path, onerror=rmtree_onerror_remove_readonly)


def is_task_expired(worker: Worker) -> bool:
    """
    Checks if the task that was sent to the worker is expired.

    Args:
        worker (Worker): information about the worker (relevant to a particular task).

    Returns:
        True: if the task is expired.
        False: if the task is still valid.

    """
    return datetime.utcnow() - worker.sent_date > consts.SENT_TASK_VALIDITY
