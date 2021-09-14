"""
Module used to define custom errors.
"""


class InvalidIPv4Address(Exception):
    """ Error raised if an invalid IPv4 address is supplied. """


class InvalidPortNumber(Exception):
    """Error raised if an invalid port number is supplied. """
