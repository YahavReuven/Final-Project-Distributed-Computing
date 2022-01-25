"""
Module used to handle imports when executing a task.
"""
import importlib


# TODO: allow to work with third library
def import_modules(modules: list, *functions):
    """
    Imports the given modules inside the given functions.

    Note:
        cls should only be a parallel class.

    Args:
        modules (list): a list containing the names of the needed modules.
        *functions: the function in which to import the modules.

    """
    for i in modules:
        module = importlib.import_module(i)
        for fn in functions:
            if fn:
                fn.__globals__.update({i: module})
