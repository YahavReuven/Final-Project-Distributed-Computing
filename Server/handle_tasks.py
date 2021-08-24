import base64
import json
import zipfile
import os
import shutil
from datetime import datetime

import consts
from consts import DatabaseType
from data_models import Task, SentTask, ReturnedTask, Worker, Project
from errors import ProjectNotFoundError, ProjectFinishedError, UnnecessaryTaskError
from db import DBHandler
from handle_projects import is_project_done, get_project_state
from utils import validate_base64_and_decode, create_path_string
from authentication import authenticate_device, authenticate_worker


async def get_new_task(device_id: str) -> SentTask:
    # TODO: maybe send sliced iterator

    authenticate_device(device_id)

    db = DBHandler()

    for project in db.get_database(DatabaseType.active_projects_db)[0]:

        # if the project has a stop_immediately with a value True,
        # the project is finished and doesn't create more tasks
        if project.stop_immediately:
            continue

        i = 0
        stop_number = project.stop_number
        tasks = project.tasks

        while stop_number < 0 or i < stop_number:
            # TODO: check comments
            # if the stop number is less than 0, it means that it isn't set
            # and should be ignored.
            # if the stop number is less than the task position
            # (also task num) the server is looking for, the project is finished

            # creates a new task if no task has been created or
            # all of the other tasks are still valid.
            if i >= len(tasks):
                task = add_new_task_to_database(project)
                add_worker_to_task(task, device_id)
                return create_task_to_send(project.project_id, i)

            # TODO: change in case more than one worker is needed for the task
            for worker in tasks[i].workers:
                # checks if the task is expired and resends it in case it is.
                is_expired = is_task_expired(worker)
                if (not worker.is_finished) and is_expired:
                    worker = create_new_worker(device_id)
                    tasks[i].workers = list(worker)
                    return create_task_to_send(project.project_id, i)

            i += 1


# TODO: check waiting database
# TODO: function too long
# TODO: check if the project is finished and move to finished in database
async def return_task_results(returned_task: ReturnedTask):
    db = DBHandler()

    project, project_state = get_project_state(returned_task.project_id)
    if (project_state & DatabaseType.waiting_to_return_projects_db or
            project_state & DatabaseType.finished_projects_db):
        raise ProjectFinishedError
    if not project_state:
        raise ProjectNotFoundError

    # TODO: maybe delete worker. maybe delete when stop number is called. maybe store in database
    if 0 <= project.stop_number < returned_task.task_number:
        raise UnnecessaryTaskError

    task = project.tasks[returned_task.task_number]

    # TODO: check if the task is already finished

    worker = authenticate_worker(returned_task.worker_id, task)

    # TODO: check if there are results and additional results
    store_task_results(returned_task.project_id, returned_task.results, returned_task.task_number)

    validate_base64_and_decode(returned_task.base64_zipped_additional_results,
                               return_obj=False)
    store_task_additional_results(returned_task.project_id, returned_task.base64_zipped_additional_results,
                                  returned_task.task_number)

    worker.is_finished = True

    if returned_task.stop_called:
        project.stop_immediately = True
        delete_unnecessary_tasks_storage(project, returned_task.task_number)

    if returned_task.is_exhausted:
        project.stop_number = returned_task.task_number

    if is_project_done(project):
        db.move_project(project, DatabaseType.active_projects_db, DatabaseType.waiting_to_return_projects_db)


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
        project_id (str): the project id of the project associated with the task.
        task_number (int): the task number of the sent task.

    Returns:
        SentTask: a new task.
    """
    project_json_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                           consts.PROJECT_STORAGE_PROJECT,
                                           consts.PROJECT_STORAGE_JSON_PROJECT)
    with open(project_json_path, 'r') as file:
        project = json.load(file)

    return SentTask(project_id=project_id, task_number=task_number,
                    base64_serialized_class=project[consts.JSON_PROJECT_BASE64_SERIALIZED_CLASS],
                    base64_serialized_iterable=project[consts.JSON_PROJECT_BASE64_SERIALIZED_ITERABLE])


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
    Adds a new worker to the task given.

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
        project_id (str): the project id of the project which the task is associated with.:
        task_results (dict): the results of the task.
        task_number (int): the task number of the returned task.
    """
    results_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                      consts.PROJECT_STORAGE_RESULTS, task_number,
                                      consts.RETURNED_TASK_RESULTS_DIRECTORY)
    os.makedirs(results_path, exist_ok=True)

    result_file = create_path_string(results_path, consts.RESULTS_FILE,
                                     from_current_directory=False)
    with open(result_file, 'w') as file:
        json.dump(task_results, file)


def store_task_additional_results(project_id: str, base64_zipped_additional_results: str, task_number: int):
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
                                      consts.RETURNED_TASK_RESULTS_DIRECTORY)

    os.makedirs(results_path, exist_ok=True)

    temp_results_file = create_path_string(results_path, consts.RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE,
                                           from_current_directory=False)
    with open(temp_results_file, 'wb') as file:
        file.write(decoded_additional_results)

    with zipfile.ZipFile(temp_results_file) as zip_file:
        zip_file.extractall(results_path)

    # file_names = os.listdir(results_path + consts.RETURNED_TASK_RESULTS_DIRECTORY)
    #
    # for file_name in file_names:
    #     shutil.move(
    #         os.path.join(results_path + consts.RETURNED_TASK_RESULTS_DIRECTORY, file_name),
    #         results_path)
    #
    # os.rmdir(results_path + consts.RETURNED_TASK_RESULTS_DIRECTORY)
    os.remove(temp_results_file)


def delete_unnecessary_tasks_storage(project: Project, stop_called_task_number: int):
    """
    Deletes all of the tasks storage in a project, besides the task
    which has the stop_called_task_number task number.

    Note:
        The function is called if a returned task of a project has a stop_called set.

    Args:
        project (Project): the project which is associated with the returned task.
        stop_called_task_number (int): the task number of the task which has the
            stop_called set
    """
    results_path = create_path_string(consts.PROJECTS_DIRECTORY,
                                      project.project_id,
                                      consts.PROJECT_STORAGE_RESULTS)
    tasks_directories = os.listdir(results_path)

    for task_directory in tasks_directories:
        if task_directory != str(stop_called_task_number):
            task_path = create_path_string(results_path, task_directory,
                                           from_current_directory=False)
            shutil.rmtree(task_path)


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
