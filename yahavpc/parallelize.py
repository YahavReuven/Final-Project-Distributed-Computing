import time
import base64
from collections.abc import Iterable
import json

import requests
import dill

import consts
from errors import ParallelFunctionNotFound
from utils import create_path_string
from handle_users import validate_user_name, get_user
from handle_requests import request_upload_new_project, request_get_project_results
from data_models import NewProject
from project_utils import create_class_to_send, create_iterable_to_send
from handle_results import save_results


class Distribute:
    def __init__(self, user_name: str, iterable: Iterable, task_size: int, results_path):
        self._user_name = user_name
        validate_user_name(self._user_name)
        self._iterable = iterable
        self._task_size = task_size
        # TODO: delete and find a way to do it from client
        self._results_path = results_path

    def __call__(self, cls):
        print('in __call__ decorator factory')
        return self.Decorator(cls, self._user_name, self._iterable, self._task_size, self._results_path)

    class Decorator:

        def __init__(self, cls, user_name, iterable: Iterable, task_size: int, results_path):
            self._cls = cls
            self._user_name = user_name
            self._iterable = iterable
            self._task_size = task_size
            self._results_path = results_path

            validate_user_name(self._cls)

        def __call__(self):
            """
            Requests the server to create a new project.

            Returns:
                An instance of the decorator

            """
            self._user = get_user(self._user_name)
            self._cls = create_class_to_send(self._cls)
            self._iterable = create_iterable_to_send(self._iterable)

            project = NewProject(creator_id=self._user.device_id, task_size=self._task_size,
                                 base64_serialized_class=self._cls,
                                 base64_serialized_iterable=self._iterable)
            self._project_id = request_upload_new_project(self._user.ip, self._user.port, project)

            print(self._project_id)

            # TODO: deal with imports
            print(1)
            return self

        def get_results(self):
            """
            Once called, the function requests the project's results from the server.

            Note:
                  The function blocks until the results are received.
                  This function shouldn't be called until the results are required.

            Returns:
                dict {iteration_number: result}: a dictionary containing the results with
                their corresponding iteration number.

            """
            project_results = None
            while not project_results:
                project_results = request_get_project_results(self._user.ip, self._user.port,
                                                              self._user.device_id, self._project_id)
                time.sleep(1)
            print("done asking server")
            save_results(project_results, self._results_path)
            return project_results.results

# @Distribute(range(100), 10)
# class A:
#     @staticmethod
#     def a():
#         return 'a'
#
#     @staticmethod
#     def b():
#         return 'b'
#
#
# # A = Distribute(range(100), 10)(A)
# project = A()
# project.get_results()


# import os
# import json
# import base64
#
# returned_project = json.loads(c)
# temp_results_file = './results.zip'
# results_path = './results'
# os.makedirs(results_path, exist_ok=True)
# with open(temp_results_file, 'wb') as file:
#     file.write(base64.b64decode(returned_project['base64_zipped_additional_results']))
# with zipfile.ZipFile(temp_results_file) as zip_file:
#     zip_file.extractall(results_path)
