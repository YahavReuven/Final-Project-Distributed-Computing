import os
import base64
import json
from datetime import datetime
import zipfile
import os
import shutil
from typing import Union

from fastapi import File, UploadFile, Body
from pydantic import BaseModel

import consts
from consts import DatabaseType, ProjectsDatabaseType
from data_models import Task, SentTask, ReturnedTask, Worker, Project
from errors import IDNotFoundError, ProjectNotFoundError, ProjectFinishedError, WorkerNotAuthenticatedError, UnnecessaryTaskError
from db_handler import DBHandler, find_project
from handle_projects import encode_zipped_project, is_project_done

# class ReturnTasks(BaseModel):
#     worker_id: int
#

# class ReturnTasks(BaseModel):
#     worker_id: int






async def get_new_task(device_id: str) -> SentTask:

    # TODO: authenticate device id

    db = DBHandler()

    for project in db.get_database(DatabaseType.projects_db):

        # if the project has a stop_immediately with a value True,
        # the project is finished and doesn't create more tasks
        if project.stop_immediately:
            continue

        i = 0
        stop_number = project.stop_number
        tasks = project.tasks

        while 0 <= stop_number < i:
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
                is_expired = datetime.utcnow() - worker.sent_date > consts.SENT_TASK_VALIDITY
                if (not worker.is_finished) and is_expired:
                    worker = create_new_worker(device_id)
                    tasks[i].workers = list(worker)
                    return create_task_to_send(project.project_id, i)

            i += 1



# TODO: check if the project is finished and move to finished in database
async def return_task_results(returned_task: ReturnedTask):

    db = DBHandler()
    project = find_project(returned_task.project_id, ProjectsDatabaseType.projects_db)
    if not project:
        project = find_project(returned_task.project_id, ProjectsDatabaseType.finished_projects_db)
        if project:
            raise ProjectFinishedError
        raise ProjectNotFoundError

    # TODO: maybe delete worker. maybe delete when stop number is called. maybe store in database
    if 0 <= project.stop_number < returned_task.task_number:
        raise UnnecessaryTaskError

    # TODO: error check
    task = project.tasks[returned_task.task_number]

    # TODO: check if the task is already finished

    if not (worker := find_worker(returned_task.worker_id, task)):
        raise WorkerNotAuthenticatedError

    store_task_results(returned_task.project_id, returned_task.base64_zipped_results, returned_task.task_number)

    worker.is_finished = True

    if returned_task.stop_called:
        project.stop_immediately = True
        delete_unnecessary_tasks_storage(project, returned_task.task_number)

    if returned_task.is_exhausted:
        project.stop_number = returned_task.task_number

    if is_project_done(project):
        db.move_project_to_finished(project)


def add_new_task_to_database(project: Project) -> Task:
    new_task = Task()
    project.tasks.append(new_task)
    return new_task


def create_task_to_send(project_id: str, task_number: int):
    project_json_path = (
                            f'{consts.PROJECTS_DIRECTORY}/{project_id}'
                            f'{consts.PROJECT_STORAGE_PROJECT}'
                            f'{consts.PROJECT_STORAGE_JSON_PROJECT}'
    )

    with open(project_json_path, 'r') as file:
        project = json.load(file)

    return SentTask(project_id=project_id, task_number=task_number,
                    base64_serialized_class=project.get(consts.JSON_PROJECT_BASE64_SERIALIZED_CLASS),
                    base64_serialized_iterable=project.get(consts.JSON_PROJECT_BASE64_SERIALIZED_ITERABLE))
                    # base64_zipped_project=encode_zipped_project(project_id))


def create_new_worker(device_id: str) -> Worker:
    sent_date = datetime.utcnow()
    new_worker = Worker(worker_id=device_id, sent_date=sent_date)
    return new_worker


def add_worker_to_task(task: Task, device_id: str):
    worker = create_new_worker(device_id)
    task.workers.append(worker)


def store_task_results(project_id: str, base64_zipped_results: str, task_number: int):

    decoded_project = base64.b64decode(base64_zipped_results)
    results_path = (
                    f'{consts.PROJECTS_DIRECTORY}/{project_id}'
                    f'{consts.PROJECT_STORAGE_RESULTS}/{task_number}'
    )
    os.makedirs(results_path)

    with open(results_path + consts.RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE, 'wb') as file:
        file.write(decoded_project)

    with zipfile.ZipFile(results_path + consts.RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE) as zip_file:
        zip_file.extractall(results_path)

    file_names = os.listdir(results_path + consts.RETURNED_TASK_RESULTS_DIRECTORY)

    for file_name in file_names:
        shutil.move(
            os.path.join(results_path + consts.RETURNED_TASK_RESULTS_DIRECTORY, file_name),
            results_path)

    os.rmdir(results_path + consts.RETURNED_TASK_RESULTS_DIRECTORY)
    os.remove(results_path + consts.RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE)


def delete_unnecessary_tasks_storage(project: Project, stop_called_task_number: int):

    results_path = (
                    f'{consts.PROJECTS_DIRECTORY}/{project.project_id}'
                    f'{consts.PROJECT_STORAGE_RESULTS}'
    )

    tasks_directories = os.listdir(results_path)

    for task_directory in tasks_directories:
        if task_directory != str(stop_called_task_number):
            shutil.rmtree(f'{results_path}/{task_directory}')


def find_worker(worker_id: str, task: Task) -> Union[Worker, None]:

    for worker in task.workers:
        if worker.worker_id == worker_id:
            return worker

    return None


# def authenticate_worker_in_task(worker_id: str, task: Task) -> bool:
#
#     for worker in task.workers:
#         if worker_id == worker.worker_id:
#             return True
#     return False

