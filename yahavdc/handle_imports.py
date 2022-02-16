"""
Module used to handle the imports needed to execute a task.
"""
import importlib


def validate_builtins(modules: list):
    """
    Validates the modules passed when created a new project.

    Args:
        modules (list): the list containing the modules names.

    """
    for module in modules:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError as exc:
            raise exc
