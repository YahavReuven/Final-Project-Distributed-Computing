

import requests
import base64
device1 = requests.post('http://127.0.0.1:8000/register_device')
print(device1.text)
device2 = requests.post('http://127.0.0.1:8000/register_device')
print(device2.text)
b64 = base64.b64encode(b'\x54\x43\x65')
project1 = requests.post('http://127.0.0.1:8000/upload_new_project',
                         json={'creator_id': device1.text[1:-1],'zip_project': b64.decode('utf-8')})
task1 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device1.text}')
task2 = requests.get(f'http://127.0.0.1:8000/get_new_task?device_id={device2.text}')

