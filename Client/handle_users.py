"""
Module used to handle the users.
"""
from handle_users_data import UsersDataHandler


def switch_user() -> UsersDataHandler:
    """
    Switches the user to another one and returns it.
    """
    user_name = input('please enter the user name: ')
    return get_user(user_name)


def get_user(user_name: str) -> UsersDataHandler:
    """
    Returns the user with the specified user name.
    """
    return UsersDataHandler(user_name)
