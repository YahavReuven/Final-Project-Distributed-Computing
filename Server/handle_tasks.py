"""
Module used to handle tasks and operation on tasks that are accessible to the client.
"""
import json
import zipfile
import os
import shutil
from datetime import datetime

import consts
from consts import DatabaseType
from data_models import Task, SentTask, ReturnedTask, Worker, Project, TaskStatisticsServer, TaskStatistics
from errors import (ProjectNotFoundError, ProjectFinishedError, UnnecessaryTaskError,
                    NoTaskAvailable)
from db import DBHandler
from handle_projects import is_project_done, get_project_state
from utils import validate_base64_and_decode, create_path_string
from authentication import authenticate_device, authenticate_worker

from handle_tasks_utils import (add_new_task_to_database, create_task_to_send,
                                create_new_worker, add_worker_to_task,
                                store_task_results, store_task_additional_results,
                                delete_unnecessary_tasks_storage, is_task_expired)


async def get_new_task(device_id: str) -> SentTask:
    """
    Selects and returns an available task to send to a worker.

    Args:
        device_id (str): the device id of the worker which requests to
            receive a task.

    Returns:
        SentTask: the task. An object containing the needed information
            by the client.

    Raises:
        NoTaskAvailable: in case there isn't a task available to send
        to the worker. Extremely unlikely in a large network.
    """
    # TODO: maybe send sliced iterator

    authenticate_device(device_id)

    db = DBHandler()

    for project in db.get_database(DatabaseType.active_projects_db)[0]:

        # if the project has a stop_immediately set to True,
        # the project is finished and doesn't create additional tasks
        # TODO: might not be needed
        if project.stop_immediately:
            continue

        task_num = 0
        stop_number = project.stop_number
        tasks = project.tasks

        while stop_number < 0 or task_num < stop_number:
            # if the stop number is less than 0, it means that it isn't set
            # and should be ignored.
            # if the task position (also task num) the server is looking for,
            # is greater than the stop number, the project is finished.

            # creates a new task if no task has been created or
            # all of the other tasks are still valid.
            if task_num >= len(tasks):
                task = add_new_task_to_database(project)
                add_worker_to_task(task, device_id)
                return create_task_to_send(project.project_id, task_num)

            # TODO: change in case more than one worker is needed for the task
            for worker in tasks[task_num].workers:
                # checks if the task is expired and resends it in case it is.
                is_expired = is_task_expired(worker)
                if (not worker.is_finished) and is_expired:
                    worker = create_new_worker(device_id)
                    tasks[task_num].workers = list(worker)
                    return create_task_to_send(project.project_id, task_num)

            task_num += 1

    raise NoTaskAvailable


# TODO: check waiting database
# TODO: function too long
# TODO: check if the project is finished and move to finished in database
# TODO: check if statistics are valid
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


    if returned_task.base64_zipped_additional_results:
        validate_base64_and_decode(returned_task.base64_zipped_additional_results,
                                   return_obj=False)
        store_task_additional_results(returned_task.project_id, returned_task.base64_zipped_additional_results,
                                      returned_task.task_number)

    worker.is_finished = True
    worker.statistics = TaskStatisticsServer(task_statistics=TaskStatistics(**returned_task.statistics),
                                             with_communications=datetime.utcnow() - worker.sent_date)

    if returned_task.stop_called:
        project.stop_immediately = True
        delete_unnecessary_tasks_storage(project, returned_task.task_number)

    if returned_task.is_exhausted:
        project.stop_number = returned_task.task_number

    if is_project_done(project):
        db.move_project(project, DatabaseType.active_projects_db, DatabaseType.waiting_to_return_projects_db)
