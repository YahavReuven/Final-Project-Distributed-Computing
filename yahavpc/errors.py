"""
Module used to define costume errors.
"""


class FunctionNotFoundError(Exception):
    """A function is not present in the given class."""


class ParallelFunctionNotFoundError(FunctionNotFoundError):
    """A parallel function is not present in the given class."""


class UnsupportedSpecialFunctionsCombination(Exception):
    """An unsupported combination of special functions was used."""


class UserNotFoundError(Exception):
    """The user was not found."""


class ResultsBeforeCreationError(Exception):
    """
    Error raised if a get_results method of a project was called
    before the project was initialized.
    """