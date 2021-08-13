

import requests
import base64
device1 = requests.get('http://127.0.0.1:8000/register_device')
print(device1.text)
device2 = requests.get('http://127.0.0.1:8000/register_device')
print(device2.text)
b64 = base64.b64encode(b'\x54\x43\x65')
project1 = requests.post('http://127.0.0.1:8000/upload_new_project',
                         json={'creator_id': device1.text[1:-1], 'zip_project': b64.decode('utf-8')})
task1 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device1.text[1:-1]}')
task2 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device2.text[1:-1]}')
task3 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device2.text[1:-1]}')
task4 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device2.text[1:-1]}')

# test return task results
# a project is exhausted
# SHOULD RETURN:
#     INFO:     127.0.0.1:55389 - "POST /upload_task_results HTTP/1.1" 200 OK
#     INFO:     127.0.0.1:55390 - "POST /upload_task_results HTTP/1.1" 200 OK
#     INFO:     127.0.0.1:55391 - "POST /upload_task_results HTTP/1.1" 400 Bad Request
#     INFO:     127.0.0.1:55392 - "POST /upload_task_results HTTP/1.1" 200 OK
result1 = requests.post('http://127.0.0.1:8000/upload_task_results',
                       json={'worker_id': device1.text[1:-1], 'project_id': project1.text[1:-1],
                             'task_number': 0, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                             'stop_called': False, 'is_exhausted': False})
result3 = requests.post('http://127.0.0.1:8000/upload_task_results',
                       json={'worker_id': device2.text[1:-1], 'project_id': project1.text[1:-1],
                             'task_number': 2, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                             'stop_called': False, 'is_exhausted': True})
result4 = requests.post('http://127.0.0.1:8000/upload_task_results',
                       json={'worker_id': device2.text[1:-1], 'project_id': project1.text[1:-1],
                             'task_number': 3, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                             'stop_called': False, 'is_exhausted': True})
result2 = requests.post('http://127.0.0.1:8000/upload_task_results',
                       json={'worker_id': device2.text[1:-1], 'project_id': project1.text[1:-1],
                             'task_number': 1, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                             'stop_called': False, 'is_exhausted': False})

# a project is stopped
# SHOULD RETURN:
#     INFO:     127.0.0.1:60433 - "POST /upload_task_results HTTP/1.1" 200 OK
#     INFO:     127.0.0.1:60434 - "POST /upload_task_results HTTP/1.1" 200 OK
#     INFO:     127.0.0.1:60435 - "POST /upload_task_results HTTP/1.1" 200 OK
#     INFO:     127.0.0.1:60436 - "POST /upload_task_results HTTP/1.1" 400 Bad Request
result1 = requests.post('http://127.0.0.1:8000/upload_task_results',
                       json={'worker_id': device1.text[1:-1], 'project_id': project1.text[1:-1],
                             'task_number': 0, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                             'stop_called': False, 'is_exhausted': False})
result3 = requests.post('http://127.0.0.1:8000/upload_task_results',
                       json={'worker_id': device2.text[1:-1], 'project_id': project1.text[1:-1],
                             'task_number': 2, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                             'stop_called': False, 'is_exhausted': False})
result2 = requests.post('http://127.0.0.1:8000/upload_task_results',
                        json={'worker_id': device2.text[1:-1], 'project_id': project1.text[1:-1],
                              'task_number': 1,
                              'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                              'stop_called': True, 'is_exhausted': False})
result4 = requests.post('http://127.0.0.1:8000/upload_task_results',
                       json={'worker_id': device2.text[1:-1], 'project_id': project1.text[1:-1],
                             'task_number': 3, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA=',
                             'stop_called': False, 'is_exhausted': False})
