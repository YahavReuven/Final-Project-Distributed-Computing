import os
import base64
from datetime import datetime
import zipfile
import os
import shutil

from fastapi import File, UploadFile, Body
from pydantic import BaseModel

import consts
from consts import DatabaseType, ProjectsDatabaseType
from data_models import Task, SentTask, ReturnedTask, NewWorker
from errors import IDNotFoundError, ProjectFinished, WorkerNotAuthenticated
from db_handler import DBHandler, find_project
from handle_projects import encode_zipped_project

# class ReturnTasks(BaseModel):
#     worker_id: int
#

# class ReturnTasks(BaseModel):
#     worker_id: int






async def get_new_task(device_id: str) -> SentTask:


    db = DBHandler()

    for project in db.get_database(DatabaseType.projects_db):

        # if the project has a stop_immediately with a value True,
        # the project is finished and doesn't create more tasks
        if project.stop_immediately:
            continue

        i = 0
        stop_number = project.stop_number
        tasks = project.tasks
        while True:

            # if the is less than 0, it means that it isn't set
            # and should be ignored.
            # if the stop number is less than the task position
            # (also task num) the server is looking for, the project is finished
            if 0 <= stop_number < i:
                break

            # creates a new task if no task has been created or
            # all of the other tasks are still valid.
            try:
                tasks[i]
            except IndexError:
                task, task_num = add_new_task_to_database(project.project_id)
                add_worker_to_task(task, device_id)
                return create_task_to_send(project.project_id, task_num)

            # TODO: change in case more than one worker is needed for the task
            for worker in tasks[i].workers_ids:
                # checks if the task is expired and resends it in case it is.
                is_expired = datetime.utcnow() - worker.sent_date > consts.SENT_TASK_VALIDITY
                if (not worker.is_finished) and is_expired:
                    worker = create_new_worker(device_id)
                    tasks[i].workers_ids = [worker]
                    return create_task_to_send(project.project_id, i)

            i += 1



# TODO: check if the project is finished and move to finished in database
async def return_task_results(returned_task: ReturnedTask):

    project = find_project(returned_task.project_id, ProjectsDatabaseType.projects_db)
    if not project:
        project = find_project(returned_task.project_id, ProjectsDatabaseType.finished_projects_db)
        if project:
            raise ProjectFinished
        raise IDNotFoundError

    # TODO: error check
    task = project.tasks[returned_task.task_number]

    # if not authenticate_worker_in_task(returned_task.worker_id, task):
    #     raise WorkerNotAuthenticated

    store_task_results(returned_task.project_id, returned_task.base64_zipped_results)

    if returned_task.stop_called:
        # stop immediatly in function
        # move function to finished
        return
    if returned_task.is_exhausted:
        # change project stop_number
        return

    # if project stop_number >=0:
        # search if every task is finished and move to finished





def add_new_task_to_database(project_id: str):
    # sent_date = datetime.utcnow()

    # new_worker = NewWorker(sent_date=sent_date)
    new_task = Task()

    project = find_project(project_id, ProjectsDatabaseType.projects_db)
    project.tasks.append(new_task)

    return new_task, len(project.tasks)


def create_task_to_send(project_id: str, task_number: int):
    return SentTask(project_id=project_id, task_number=task_number,
                    base64_zipped_project=encode_zipped_project(project_id))


def create_new_worker(device_id: str):
    sent_date = datetime.utcnow()
    new_worker = NewWorker(worker_id=device_id, sent_date=sent_date)
    return new_worker


def add_worker_to_task(task: Task, device_id: str):
    worker = create_new_worker(device_id)
    task.workers_ids.append(worker)


def authenticate_worker_in_task(worker_id: str, task: Task) -> bool:

    for w_id in task.workers_ids:
        if worker_id == w_id:
            return True
    return False


def store_task_results(project_id: str, base64_zipped_results: str):

    decoded_project = base64.b64decode(base64_zipped_results)
    results_path = f'{consts.PROJECTS_DIRECTORY}/{project_id}{consts.PROJECT_STORAGE_RESULTS}'


    with open(results_path + '/temp.zip', 'wb') as file:
        file.write(decoded_project)


    # with zipfile.ZipFile(results_path + '/temp.zip', mode='w') as file:
    #     file.writestr('/temp.zip', decoded_project)

    with zipfile.ZipFile(results_path + '/temp.zip') as zip_file:
        zip_file.extractall(results_path)


    file_names = os.listdir(results_path + '/results')

    for file_name in file_names:
        shutil.move(os.path.join(results_path + '/results', file_name), results_path)

    os.rmdir(results_path + '/results')
    os.remove(results_path + '/temp.zip')


