import os
import base64
from datetime import datetime


from fastapi import File, UploadFile, Body
from pydantic import BaseModel

import consts
from consts import DatabaseType
from data_models import Task, SentTask
from db_handler import DBHandler, find_project
from handle_projects import encode_zipped_project

# class ReturnTasks(BaseModel):
#     worker_id: int
#

# class ReturnTasks(BaseModel):
#     worker_id: int






async def get_new_task(device_id: str) -> SentTask:

    db = DBHandler()

    for project in db.get_database(DatabaseType.projects_db, lst_form=True):

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
            # all of the other tasks are still valid
            try:
                tasks[i]
            except IndexError:
                task, task_num = add_new_task_to_database(project.project_id)
                task.workers_ids.append(device_id)
                return create_task_to_send(project.project_id, task_num)

            # TODO: remove expired workers
            # checks if the task is expired and resends it in case it is
            is_expired = datetime.utcnow() - tasks[i].sent_date > consts.SENT_TASK_VALIDITY
            if (not tasks[i].is_finished) and is_expired:
                tasks[i].workers_ids.append(device_id)
                return create_task_to_send(project.project_id, i)

            i += 1



# TODO: check if the project is finished and move to finished in database
async def return_task_results():
    pass





def add_new_task_to_database(project_id: str):
    sent_date = datetime.utcnow()

    new_task = Task(sent_date=sent_date)

    project = find_project(project_id)
    project.tasks.append(new_task)

    return new_task, len(project.tasks)


def create_task_to_send(project_id: str, task_number: int):
    return SentTask(project_id=project_id, task_number=task_number,
                    base64_zipped_project=encode_zipped_project(project_id))



