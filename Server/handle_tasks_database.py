# import os
# import base64
# from fastapi import File, UploadFile, Body
# from pydantic import BaseModel
#
#
# class NewProject(BaseModel):
#     creator_id: int
#     zip_project: str
#     #zip_project: UploadFile
#
#
# class ReturnTasks(BaseModel):
#     worker_id: int
#
# # send request:
# # import base64
# # b64 = base64.b64encode(b'\x54\x43\x65')
# # resp = requests.post('http://127.0.0.1:8000/new_project', json={'creator_id': 1,'zip_project': b64.decode('utf-8')})
#
# #TODO: make it work with UploadFile insted of bytes
# async def create_new_project(new_project: NewProject) -> int:
#     if not os.path.isdir('./projects'):
#         os.mkdir('./projects')
#
#     x = base64.b64decode(new_project.zip_project)
#
#     with open('./projects/file.txt.', 'wb') as file:
#         file.write(x)
#     print(new_project.creator_id, new_project.zip_project)
#     return new_project.creator_id
#
#
# # async def create_new_project(creator_id: int = Body(), somthing: int = Body()) -> int:
# #     print(creator_id)
# #     return somthing
#
# # async def create_new_project(new_project: NewProject) -> int:
# #     print(new_project.creator_id)
# #     return new_project.creator_id
#
# # async def create_new_project(new_project: NewProject, file: UploadFile = File(...)):
# #     #print(new_project.dict())
# #     return True
#
#
#
# async def return_project_results():
#     pass

class ReturnTasks(BaseModel):
    worker_id: int

async def get_new_task():
    pass


async def return_task_results():
    pass