"""
Module used to handle the special functions of a project
"""
from errors import FunctionNotFoundError, UnsupportedSpecialFunctionsCombination


def validate_special_functions(cls, *, parallel_func, stop_func, only_if_func):
    validate_function_present(cls, parallel_func)
    if len(stop_func) and len(only_if_func):
        raise UnsupportedSpecialFunctionsCombination
    if len(stop_func):
        validate_function_present(cls, stop_func)
    if len(only_if_func):
        validate_function_present(cls, only_if_func)


def validate_function_present(cls, function_name: str):
    function = getattr(cls(), function_name)
    if not callable(function):
        raise FunctionNotFoundError
