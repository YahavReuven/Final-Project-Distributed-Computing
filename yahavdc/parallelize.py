"""
Module used to allow the creation of projects and parallelization.
"""
import time
from typing import Iterator

from errors import ResultsBeforeCreationError, ServerError
from handle_users import validate_user_name, get_user
from handle_requests import request_upload_new_project, request_get_project_results
from data_models import NewProject
from project_utils import create_class_to_send, create_iterator_to_send
from handle_results import save_results, find_results_free_path
from handle_imports import validate_builtins
from creator_statistics import save_statistics
from handle_project_functions import validate_special_functions


class Distribute:

    def __init__(self, user_name: str, iterator: Iterator, task_size: int,
                 results_path: str, *, parallel_func: str = 'parallel_func',
                 stop_func: str = '', only_if_func: str = '', modules: list = []):
        """
        Prepares a new project before being called.

        Args:
            user_name (str): the name of the desired connection.
            iterator (Iterator): the range of values on which to perform the project.
            task_size (int): the size of each task executed by the workers.
            results_path (str): the path in which to save the project results.
            parallel_func (str) = 'parallel_func': the name of the special function 'parallel_func'
            stop_func (str): the name of the special function 'stop_func'
            only_if_func (str): the name of the special function 'only_if_func'
            modules (list) = []: a list of the names of the needed modules.

        """
        self._user_name = user_name
        validate_user_name(self._user_name)
        self._iterator = iterator
        self._task_size = int(task_size)
        # TODO: delete and find a way to do it from client
        self._results_path = results_path
        self._parallel_func = parallel_func
        self._stop_func = stop_func
        self._only_if_func = only_if_func
        self._modules = modules

    def __call__(self, cls):
        return self.Decorator(cls, self._user_name, self._iterator, self._task_size,
                              self._results_path, self._parallel_func, self._stop_func,
                              self._only_if_func, self._modules)

    class Decorator:

        def __init__(self, cls, user_name: str, iterator: Iterator, task_size: int,
                     results_path: str, parallel_func: str, stop_func: str,
                     only_if_func: str, modules: list):
            self._cls = cls
            self._user_name = user_name
            self._iterator = iterator
            self._task_size = task_size
            self._results_path = results_path
            self._parallel_func = parallel_func
            self._stop_func = stop_func
            self._only_if_func = only_if_func
            self._modules = modules

            self._user = None

            validate_user_name(self._user_name)
            validate_builtins(self._modules)
            validate_special_functions(cls, parallel_func=self._parallel_func,
                                       stop_func=self._stop_func,
                                       only_if_func=self._only_if_func)

        def __call__(self):
            """
            Requests the server to create a new project.

            Returns:
                An instance of the decorator.

            """
            self._user = get_user(self._user_name)
            self._cls = create_class_to_send(self._cls)
            self._iterator = create_iterator_to_send(self._iterator)

            project = NewProject(creator_id=self._user.device_id,
                                 task_size=self._task_size,
                                 parallel_func=self._parallel_func,
                                 stop_func=self._stop_func,
                                 only_if_func=self._only_if_func,
                                 base64_serialized_class=self._cls,
                                 base64_serialized_iterable=self._iterator,
                                 modules=self._modules)
            self._project_id = request_upload_new_project(self._user.ip, self._user.port,
                                                          project)
            return self

        def get_results(self):
            """
            Requests the project's results from the server.

            Note:
                  The function blocks until the results are received.
                  This function shouldn't be called until the results are required.

            Returns:
                dict {iteration_number: result}: a dictionary containing the
                    results with their corresponding iteration number.

            Raises:
                ResultsBeforeCreationError: if the method was called before
                    the project is initialized.

            """
            if not self._user:
                raise ResultsBeforeCreationError

            while True:
                try:
                    project_results = request_get_project_results(self._user.ip,
                                                                  self._user.port,
                                                                  self._user.device_id,
                                                                  self._project_id)
                except ServerError:
                    time.sleep(5)
                    continue
                else:
                    break

            self._results_path = find_results_free_path(self._results_path)
            save_results(project_results, self._results_path)
            save_statistics(self._results_path, project_results.statistics)
            return project_results.results
.