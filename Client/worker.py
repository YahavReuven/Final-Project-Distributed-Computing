"""
Module used to handle all the actions needed for a worker.
"""
from itertools import islice
from datetime import datetime
import time

from handle_requests import request_get_new_task, request_upload_task_results
from handle_users_data import UsersDataHandler
from client_statistics import get_task_statistics, task_statistics_as_dict

from worker_utils import (results_to_file, get_results, has_additional_results,
                          get_zip_additional_results, get_task_cls, get_task_iterable,
                          init_task_result_storage, clean_results_directory)
from consts import ReturnTypes
from data_models import ReturnedTask, TaskStatistics
from handle_imports import import_modules
from errors import ServerError


def task_menu(user: UsersDataHandler):
    """
    Displays the task menu and starts to execute tasks.

    Args:
        user (UsersDataHandler): the user which executes the tasks.

    """
    action = input('please enter how many tasks you would like to execute: ')
    try:
        num_of_tasks = int(action)
    except ValueError:
        print("actions that are not positive values are not supported yet")
        return
    execute_multiple_tasks(user, num_of_tasks)


def execute_multiple_tasks(user: UsersDataHandler, num_of_tasks: int):
    """
    Executes multiple tasks one after another.

    Args:
        user (UsersDataHandler): the user whi executes the task.
        num_of_tasks (int): the amount of tasks to execute.

    """
    for i in range(num_of_tasks):
        response = execute_task(user)


def execute_task(user: UsersDataHandler):
    """
    Executes a single task.

    Args:
        user (UsersDataHandler): the user whi executes the task.

    Returns:
        Response: the response form the server.

    """
    return_type = TaskExecUtils.run_task_code(user)
    response = TaskExecUtils.return_task(user, return_type)
    clean_results_directory()
    return response


class TaskExecUtils:
    task = None

    @classmethod
    def run_task_code(cls, user: UsersDataHandler):
        """
        Executes the task.

        Args:
            user (UsersDataHandler): the user to execute the task with.

        Returns:
            ReturnTypes: the type generated from the execution.
                normal: the task ended with no errors.
                exhausted: the iterator of the project ended in the middle of the task.
                stopped: a stop function was called and returned True.

        """
        return_type = ReturnTypes.normal

        while not cls.task:
            try:
                cls.task = request_get_new_task(user.user.ip, user.user.port, user.user.device_id)
            except ServerError:
                time.sleep(1)
                continue

        total_execution_time_start = datetime.utcnow()
        # load the necessary code
        parallel_cls = get_task_cls(cls.task)
        parallel_obj = parallel_cls()
        iterable = get_task_iterable(cls.task)

        # init the task storage for the results
        init_task_result_storage()

        # slice the iterable
        start = cls.task.task_number * cls.task.task_size
        end = start + cls.task.task_size
        iterable = islice(iterable, start, end)

        has_stop_func = len(cls.task.stop_func)
        has_only_if_func = len(cls.task.only_if_func)

        iteration_index = start
        results = {}

        parallel_func = getattr(parallel_obj, cls.task.parallel_func, None)
        stop_func = getattr(parallel_obj, cls.task.stop_func, None)
        only_if_func = getattr(parallel_obj, cls.task.only_if_func, None)

        import_modules(cls.task.modules, parallel_func, stop_func, only_if_func)
        pure_run_time_start = datetime.utcnow()
        for param_value in iterable:
            param_storage = param_value
            if type(param_value) != int and type(param_value) != float and type(param_value) != bool and type(
                    param_value) is not None:
                param_storage = str(param_value)
            return_value = parallel_func(param_value)
            if has_stop_func:
                write_result = stop_func(return_value)
                if write_result:
                    results[param_storage] = return_value
                    return_type = ReturnTypes.stopped
                    break
            elif has_only_if_func:
                write_result = only_if_func(return_value)
                if write_result:
                    results[param_storage] = return_value
            else:
                results[param_storage] = return_value

            iteration_index += 1

        pure_run_time_end = datetime.utcnow()

        results_to_file(results)

        total_execution_time_end = datetime.utcnow()
        task_statistics = TaskStatistics(pure_run_time=pure_run_time_end - pure_run_time_start,
                                         total_execution_time=
                                         total_execution_time_end - total_execution_time_start)
        user.add_task(cls.task.project_id, cls.task.task_number,
                      task_statistics)
        if iteration_index < end - 1:
            return_type = ReturnTypes.exhausted

        return return_type

    @classmethod
    def return_task(cls, user: UsersDataHandler, return_type: ReturnTypes):
        """
        Returns a finished task to the server.

        Args:
            user (UsersDataHandler): the user which executed the task.
            return_type (ReturnTypes): the ReturnTypes generated from the execution.

        Returns:
             Response: the response from the server.

        """
        task_statistics = task_statistics_as_dict(
            get_task_statistics(user, cls.task.project_id, cls.task.task_number).statistics)
        returned_task = ReturnedTask(worker_id=user.user.device_id, project_id=cls.task.project_id,
                                     task_number=cls.task.task_number, results=get_results(),
                                     statistics=task_statistics)

        if has_additional_results():
            returned_task.base64_zipped_additional_results = get_zip_additional_results()

        if return_type == ReturnTypes.stopped:
            returned_task.stop_called = True
        elif return_type == ReturnTypes.exhausted:
            returned_task.is_exhausted = True

        cls.task = None
        return request_upload_task_results(user.user.ip, user.user.port, returned_task)
