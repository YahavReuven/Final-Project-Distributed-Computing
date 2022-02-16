"""
Module used to handle the special functions of a project.
"""
from errors import FunctionNotFoundError, UnsupportedSpecialFunctionsCombination


def validate_special_functions(cls, *, parallel_func: str, stop_func: str,
                               only_if_func: str):
    """
    Checks if all the special functions are present in the class and are
        in supported combinations.

    Args:
        cls: the class to check in.
        parallel_func (str):  the name of the special function 'parallel_func'.
        stop_func (str): the name of the special function 'stop_func'.
        only_if_func (str) : the name of the special function 'only_if_func'.

    Raises:
        UnsupportedSpecialFunctionsCombination: if the class has an
            unsupported combination of the special functions.

    """
    validate_function_present(cls, parallel_func)
    if len(stop_func) and len(only_if_func):
        raise UnsupportedSpecialFunctionsCombination
    if len(stop_func):
        validate_function_present(cls, stop_func)
    if len(only_if_func):
        validate_function_present(cls, only_if_func)


def validate_function_present(cls, function_name: str):
    """
    Check if a function with a given name is present in the class.

    Args:
        cls: the class to search in.
        function_name (str): the name of the function.

    Raises:
        FunctionNotFoundError: if the given name is not a function in the class.

    """
    function = getattr(cls(), function_name)
    if not callable(function):
        raise FunctionNotFoundError
