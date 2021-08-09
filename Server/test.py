

import requests
import base64
device1 = requests.post('http://127.0.0.1:8000/register_device')
print(device1.text)
device2 = requests.post('http://127.0.0.1:8000/register_device')
print(device2.text)
b64 = base64.b64encode(b'\x54\x43\x65')
project1 = requests.post('http://127.0.0.1:8000/upload_new_project',
                         json={'creator_id': device1.text[1:-1],'zip_project': b64.decode('utf-8')})
task1 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device1.text[1:-1]}')
task2 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device2.text[1:-1]}')
task3 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device2.text[1:-1]}')
task4 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device2.text[1:-1]}')

# test return task results
# a project is exhausted
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




# import requests
# import base64
# device1 = requests.post('http://127.0.0.1:8000/register_device')
# b64 = base64.b64encode(b'\x54\x43\x65')
# project1 = requests.post('http://127.0.0.1:8000/upload_new_project',
#                          json={'creator_id': device1.text[1:-1],'zip_project': b64.decode('utf-8')})
# task1 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device1.text}')
# # with open('C:/Users/yahav/Downloads/results.zip', 'rb') as file:
# #     zipped_results = file.read()
# # zipped_results = str(base64.b64encode(zipped_results))
# result = requests.post('http://127.0.0.1:8000/upload_task_results',
#                        json={'worker_id': device1.text[1:-1], 'project_id': project1.text[1:-1],
#                              'task_number': 0, 'base64_zipped_results': 'UEsDBBQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAcmVzdWx0cy9mb2xkZXIgMi9QSwMEFAAAAAAAK5f1UnRus3UOAAAADgAAABoAAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weXByaW50KCdoZWxsbycpUEsDBBQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAcmVzdWx0cy9oZWxsby50eHRoZWxsbyB3b3JsZFBLAQIUABQAAAAAAC+X9VIAAAAAAAAAAAAAAAARAAAAAAAAAAAAEAAAAAAAAAByZXN1bHRzL2ZvbGRlciAyL1BLAQIUABQAAAAAACuX9VJ0brN1DgAAAA4AAAAaAAAAAAAAAAEAIAAAAC8AAAByZXN1bHRzL2ZvbGRlciAyL3B5dGhvbi5weVBLAQIUABQAAAAAABSX9VKFEUoNCwAAAAsAAAARAAAAAAAAAAEAIAAAAHUAAAByZXN1bHRzL2hlbGxvLnR4dFBLBQYAAAAAAwADAMYAAACvAAAAAAA='})
