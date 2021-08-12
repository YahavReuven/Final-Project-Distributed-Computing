
import time
from collections.abc import Iterable

import dill


import requests
import base64



class Distribute:
    def __init__(self, iterable: Iterable, task_size: int):
        self.iterable = iterable
        self.task_size = task_size

    def __call__(self, cls):
        print('in __call__ decorator factory')
        return self.Decorator(self.iterable, self.task_size, cls)

    class Decorator:

        def __init__(self, iterable: Iterable, task_size: int, cls: type):
            self.iterable = iterable
            self.task_size = task_size
            self.cls = cls


        def __call__(self):
            """

            Requests the server to create a new project.

            Returns:
                An instance of the decorator
            """
            device = requests.get('http://127.0.0.1:8000/register_device')
            print(device.text[1:-1])
            serialized_class = dill.dumps(self.cls)
            serialized_iterable = dill.dumps(self.iterable)

            encoded_class = base64.b64encode(serialized_class).decode('utf-8')
            encoded_iterable = base64.b64encode(serialized_iterable).decode('utf-8')
            project1 = requests.post('http://127.0.0.1:8000/upload_new_project',
                                     json={'creator_id': device.text[1:-1],
                                           'task_size': self.task_size,
                                           'base64_serialized_class': encoded_class,
                                           'base64_serialized_iterable': encoded_iterable})
            print(project1.text[1:-1])

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
            results = None
            i = 0
            while not results:
                if i == 10:
                    results = 1
                    break
                print('asking server')

                time.sleep(1)
                i += 1
            print("done asking server")
            return results





def distribute(iterable: Iterable, task_size: int):

    def decorator(cls):

        device_id = None
        project_id = None

        def init():
            pass

        async def get_results(project_id: str):
            results = None
            i = 0
            while not results:
                if i == 10:
                    results = 1
                    break
                print('asking server')

                time.sleep(1)
                i += 1
            return results

        def inner():
            device = requests.get('http://127.0.0.1:8000/register_device')
            print(device.text[1:-1])
            serialized_class = dill.dumps(cls)
            serialized_iterable = dill.dumps(iterable)

            encoded_class = base64.b64encode(serialized_class).decode('utf-8')
            encoded_iterable = base64.b64encode(serialized_iterable).decode('utf-8')
            project1 = requests.post('http://127.0.0.1:8000/upload_new_project',
                                     json={'creator_id': device.text[1:-1], 'base64_serialized_class': encoded_class,
                                           'base64_serialized_iterable': encoded_iterable})
            print(project1.text[1:-1])

            #TODO: deal with imports
            x = get_results(1)
            return x

        return inner


    return decorator




@Distribute(range(100), 10)
class A:
    @staticmethod
    def a():
        return 'a'
    @staticmethod
    def b():
        return 'b'


# A = Distribute(range(100), 10)(A)
project = A()
# project.get_results()

