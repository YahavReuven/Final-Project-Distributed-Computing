
import os


from handle_users_data import UsersDataHandler
import consts

os.makedirs(consts.USERS_DIRECTORY)

while True:
    name = input("please enter the users name:")
    a = UsersDataHandler(name)
