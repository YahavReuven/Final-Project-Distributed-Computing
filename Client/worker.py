"""
Module used to handle all the actions needed for a worker.
"""

from handle_requests import request_get_new_task, request_upload_task_results
from handle_users_data import UsersDataHandler

from itertools import islice

from worker_utils import (has_stop_function, results_to_file, get_results, has_additional_results,
                          get_zip_additional_results, get_task_cls, get_task_iterable,
                          init_task_result_storage)
import consts
from consts import ReturnTypes
from data_models import ReceivedTask, ReturnedTask

task = None


def execute_task(user: UsersDataHandler):
    return_type = run_task_code(user)
    return return_task(user, return_type)


def run_task_code(user: UsersDataHandler):
    global task
    task = request_get_new_task(user.ip, user.port, user.device_id)

    # load the neceseray code
    parallel_cls = get_task_cls(task)
    iterable = get_task_iterable(task)

    # init the task storage for the results
    init_task_result_storage()

    # TODO: maybe move to server
    # slice the iterable
    start = task.task_number * task.task_size
    end = start + task.task_size
    iterable = islice(iterable, start, end)

    # TODO: maybe add has_parallel_function
    # TODO: maybe change to try - more pythonic?
    has_stop_func = has_stop_function(parallel_cls)

    iteration_index = start
    results = {}

    for param_value in iterable:

        return_value = getattr(parallel_cls, consts.PARALLEL_FUNCTION_NAME)(param_value)

        if has_stop_func:
            write_result = getattr(parallel_cls, consts.STOP_FUNCTION_NAME)(return_value)
            if write_result:
                # TODO: maybe write to an object and write to the file at the end
                # TODO: maybe create a designd object for result
                results[iteration_index] = return_value
                results_to_file(results)
                return ReturnTypes.stopped
            iteration_index += 1
            continue

        results[iteration_index] = return_value
        iteration_index += 1

    results_to_file(results)

    if iteration_index < end - 1:
        return ReturnTypes.exhausted

    return ReturnTypes.normal


def return_task(user: UsersDataHandler, return_type: ReturnTypes):
    global task

    data = {}

    data[consts.RETURNED_TASK_WORKER_ID_KEY] = user.device_id
    data[consts.RETURNED_TASK_PROJECT_ID_KEY] = task.project_id
    data[consts.RETURNED_TASK_TASK_NUMBER_KEY] = task.task_number
    data[consts.RETURNED_TASK_RESULTS_KEY] = get_results()

    if has_additional_results():
        data[consts.RETURNED_TASK_BASE64_ZIPPED_ADDITIONAL_RESULTS_KEY] = get_zip_additional_results()

    if return_type == ReturnTypes.stopped:
        data[consts.RETURNED_TASK_STOP_CALLED_KEY] = True
    elif return_type == ReturnTypes.exhausted:
        data[consts.RETURNED_TASK_IS_EXHAUSTED_KEY] = True

    returned_task = ReturnedTask(**data)

    return request_upload_task_results(returned_task)
