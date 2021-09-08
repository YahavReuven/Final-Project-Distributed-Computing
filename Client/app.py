
import os


from handle_users_data import UsersDataHandler
from initialize_app import init_user
import consts
from worker import execute_task

ls = []
while True:
    user = init_user()

    action = int(input('please enter what action to take: '))

    # if action == 1:
    #     switch_user()
    if action == 2:
        execute_task(user)
