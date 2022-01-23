"""
The main module of the client application.
"""
from initialize_app import init_user, init_task_storage
from handle_users import switch_user
from worker import task_menu


def welcome():
    """
    Displays the welcome message.
    """
    print(""" /$$$$$$$   /$$$$$$        /$$                                 /$$              
| $$__  $$ /$$__  $$      /$$/                                | $$              
| $$  \ $$| $$  \__/     /$$/   /$$$$$$  /$$$$$$$   /$$$$$$  /$$$$$$    /$$$$$$ 
| $$  | $$| $$          /$$/   /$$__  $$| $$__  $$ |____  $$|_  $$_/   /$$__  $$
| $$  | $$| $$         /$$/   | $$  \ $$| $$  \ $$  /$$$$$$$  | $$    | $$$$$$$$
| $$  | $$| $$    $$  /$$/    | $$  | $$| $$  | $$ /$$__  $$  | $$ /$$| $$_____/
| $$$$$$$/|  $$$$$$/ /$$/     |  $$$$$$/| $$  | $$|  $$$$$$$  |  $$$$/|  $$$$$$$
|_______/  \______/ |__/       \______/ |__/  |__/ \_______/   \___/   \_______/""")
    print('\n\nWelcome, and thank you for using "DC/onate".\n\n')


def help_menu():
    """
    Displays the main menu.
    """
    print("""Possible actions currently supported by this application:
    user - Switches or creates a new user.
    task - Requests new tasks to execute.
    exit - Closes the application.
    """)


welcome()
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
