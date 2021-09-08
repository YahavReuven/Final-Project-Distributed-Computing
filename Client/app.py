
import os


from handle_users_data import UsersDataHandler
from initialize_app import init_user
import consts

ls = []
while True:
    ls.append(init_user())

    # action = int(input('please enter what action to take: '))
    #
    # if action == 1:
    #     switch_user()
    # elif action == 2:
    #     execute task()
