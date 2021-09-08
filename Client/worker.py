"""
Module used to handle all the actions needed for a worker.
"""

from handle_requests import request_get_new_task
from handle_users_data import UsersDataHandler

import base64
import dill

def execute_task(user: UsersDataHandler):

    task = request_get_new_task(user.ip, user.port, user.device_id)

    # load the neceseray code
    code = task.base64_serialized_class
    code = base64.b64decode(code)
    code = dill.loads(code)
    iterable = task.base64_serialized_class
    iterable = base64.b64decode(iterable)

    # TODO: maybe move to server
    # slice the iterable
    start =
    iterable = islice(iterable, iteration_manager.start, iteration_manager.end)




