"""
Module used to define costume errors.
"""

class ParallelFunctionNotFoundError(Exception):
    """A parallel function is not present in the given class."""


class UserNotFoundError(Exception):
    """The user was not found."""


class ResultsBeforeCreationError(Exception):
    """
    Error raised if a get_results method of a project was called
    before the project was initialized.
    """