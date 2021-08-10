
import asyncio
from collections.abc import Iterable

import dill


import requests
import base64

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

                asyncio.sleep(5)
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




@distribute(range(100), 10)
class A:
    @staticmethod
    def a():
        return 'a'
    @staticmethod
    def b():
        return 'b'


x = A()