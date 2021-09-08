"""
Module used to handle all the actions needed for a worker.
"""

from handle_requests import request_get_new_task, request_upload_task_results
from handle_users_data import UsersDataHandler

import base64
import dill
from itertools import islice

from handle_storage import init_task_result_storage, has_additional_results
from handle_tasks import has_stop_function, add_result, get_results, get_zip_additional_results
import consts
from consts import ReturnTypes
from data_models import Task, ReturnedTask

task = Task()

def execute_task(user: UsersDataHandler):
    return_type = run_task_code(user)
    return return_task()

def run_task_code(user: UsersDataHandler):

    global task
    task = request_get_new_task(user.ip, user.port, user.device_id)

    # load the neceseray code
    code = task.base64_serialized_class
    code = base64.b64decode(code)
    code = dill.loads(code)
    iterable = task.base64_serialized_class
    iterable = base64.b64decode(iterable)

    # init the task storage for the results
    init_task_result_storage()

    # TODO: maybe move to server
    # slice the iterable
    start = task.task_number * task.task_size
    end = start + task.task_size
    iterable = islice(iterable, start, end)

    has_stop_func = has_stop_function(code)

    iteration_index = start

    for param_value in iterable:

        return_value = code.consts.PARALLEL_FUNCTION_NAME(param_value)

        if has_stop_func:
            write_result = code.consts.STOP_FUNCTION_NAME(return_value)
            if write_result:
                # TODO: maybe write to an object and write to the file at the end
                add_result(iteration_index, return_value)
                return ReturnTypes.stopped
            iteration_index += 1
            continue

        add_result(iteration_index, return_value)
        iteration_index += 1

    if iteration_index < end - 1:
        return ReturnTypes.exhausted

    return ReturnTypes.normal


def return_task(user: UsersDataHandler, return_type: ReturnTypes):

    global task

    worker_id = user.device_id
    project_id = task.project_id
    task_number = task.task_number
    results = get_results()
    # TODO: try to remove and let the requests function to do the work
    base64_zipped_additional_results = None
    stop_called = False
    is_exhausted = False

    if has_additional_results():
        base64_zipped_additional_results = get_zip_additional_results()

    # returned_task = ReturnedTask(worker_id=worker_id, project_id=project_id,
    #                              task_number=task_number, results=results,
    #                              base64_zipped_additional_results=base64_zipped_additional_results,
    #                             )

    if return_type == ReturnTypes.stopped:
        stop_called = True
    elif return_type == ReturnTypes.exhausted:
        is_exhausted = True

    return request_upload_task_results(worker_id, project_id, task_number, results,
                                       base64_zipped_additional_results, stop_called,
                                       is_exhausted)







