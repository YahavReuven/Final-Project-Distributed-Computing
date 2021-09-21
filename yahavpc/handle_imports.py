"""
Module used to handle the imports needed to execute a task.
"""
import importlib


# TODO: maybe change
def validate_builtins(modules: list):
    for module in modules:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError as exc:
            raise exc
