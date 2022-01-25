"""
The main module of the client application.
"""
from initialize_app import init_user, init_task_storage
from handle_users import switch_user
from worker import task_menu


def help_menu():
    """
    Displays the main menu.
    """
    print("""Possible actions currently supported by this application:
    user - Switches or creates a new user.
    task - Requests new tasks to execute.
    exit - Closes the application.
    """)


user = init_user()
init_task_storage()
while True:
    action = input('please enter what action to take (press \'help\' to see supported actions): ')
    if action == 'help':
        help_menu()
    if action == 'user':
        user = switch_user()
    if action == 'task':
        task_menu(user)
    if action == 'exit':
        break
